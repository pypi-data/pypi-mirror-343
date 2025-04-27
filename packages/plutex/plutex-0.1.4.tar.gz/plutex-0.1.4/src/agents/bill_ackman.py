import json
from typing import Any, Dict  # Import Dict

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing_extensions import Literal

from src.graph.state import AgentState, show_agent_reasoning
from src.tools.api import get_financial_metrics, get_market_cap, search_line_items
from src.utils.llm import call_llm
from src.utils.progress import progress


class BillAckmanSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str


def bill_ackman_agent(state: AgentState):
    """
    Analyzes stocks using Bill Ackman's investing principles and LLM reasoning.
    Fetches multiple periods of data so we can analyze long-term trends.
    """
    data = state["data"]
    end_date = data["end_date"]
    tickers = data["tickers"]

    analysis_data: Dict[str, Any] = {}
    ackman_analysis: Dict[str, Dict[str, Any]] = {}

    for ticker in tickers:
        progress.update_status(
            "bill_ackman_agent", ticker, "Fetching financial metrics"
        )
        metrics = get_financial_metrics(ticker, end_date, period="annual", limit=5)

        progress.update_status(
            "bill_ackman_agent", ticker, "Gathering financial line items"
        )
        # Request multiple periods of data (annual or TTM) for a more robust long-term view.
        financial_line_items = search_line_items(
            ticker,
            [
                "revenue",
                "operating_margin",
                "debt_to_equity",
                "free_cash_flow",
                "total_assets",
                "total_liabilities",
                "dividends_and_other_cash_distributions",
                "outstanding_shares",
            ],
            end_date,
            period="annual",  # or "ttm" if you prefer trailing 12 months
            limit=5,  # fetch up to 5 annual periods (or more if needed)
        )

        progress.update_status("bill_ackman_agent", ticker, "Getting market cap")
        market_cap = get_market_cap(ticker, end_date)

        progress.update_status(
            "bill_ackman_agent", ticker, "Analyzing business quality"
        )
        quality_analysis: Dict[str, Any] = analyze_business_quality(
            metrics, financial_line_items
        )

        progress.update_status(
            "bill_ackman_agent", ticker, "Analyzing balance sheet and capital structure"
        )
        balance_sheet_analysis: Dict[str, Any] = analyze_financial_discipline(
            metrics, financial_line_items
        )

        progress.update_status(
            "bill_ackman_agent",
            ticker,
            "Calculating intrinsic value & margin of safety",
        )
        # Add check for market_cap before calling valuation function
        valuation_analysis: Dict[str, Any]
        if market_cap is not None:
            valuation_analysis = analyze_valuation(financial_line_items, market_cap)
        else:
            valuation_analysis = {
                "score": 0.0,
                "details": "Market cap data unavailable for valuation",
            }
            progress.update_status(
                "bill_ackman_agent", ticker, "Failed: Market cap unavailable"
            )

        # Combine partial scores or signals, casting to float for consistency
        quality_score: float = float(quality_analysis.get("score", 0.0))
        balance_sheet_score: float = float(balance_sheet_analysis.get("score", 0.0))
        valuation_score: float = float(valuation_analysis.get("score", 0.0))

        total_score: float = quality_score + balance_sheet_score + valuation_score
        max_possible_score: float = 15.0  # Use float for consistency

        # Generate a simple buy/hold/sell (bullish/neutral/bearish) signal
        if total_score >= 0.7 * max_possible_score:
            signal = "bullish"
        elif total_score <= 0.3 * max_possible_score:
            signal = "bearish"
        else:
            signal = "neutral"

        analysis_data[ticker] = {
            "signal": signal,
            "score": total_score,
            "max_score": max_possible_score,
            "quality_analysis": quality_analysis,
            "balance_sheet_analysis": balance_sheet_analysis,
            "valuation_analysis": valuation_analysis,
        }

        progress.update_status(
            "bill_ackman_agent", ticker, "Generating Bill Ackman analysis"
        )
        ackman_output = generate_ackman_output(
            ticker=ticker,
            analysis_data=analysis_data,
            model_name=state["metadata"]["model_name"],
            model_provider=state["metadata"]["model_provider"],
        )

        ackman_analysis[ticker] = {
            "signal": ackman_output.signal,
            "confidence": ackman_output.confidence,
            "reasoning": ackman_output.reasoning,
        }

        progress.update_status("bill_ackman_agent", ticker, "Done")

    # Wrap results in a single message for the chain
    message = HumanMessage(
        content=json.dumps(ackman_analysis), name="bill_ackman_agent"
    )

    # Show reasoning if requested
    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(ackman_analysis, "Bill Ackman Agent")

    # Add signals to the overall state
    state["data"]["analyst_signals"]["bill_ackman_agent"] = ackman_analysis

    return {"messages": [message], "data": state["data"]}


def analyze_business_quality(
    metrics: list, financial_line_items: list
) -> Dict[str, Any]:
    """
    Analyze whether the company has a high-quality business with stable or growing cash flows,
    durable competitive advantages, and potential for long-term growth.
    """
    score: float = 0.0
    details = []

    if not metrics or not financial_line_items:
        return {"score": 0, "details": "Insufficient data to analyze business quality"}

    # 1. Multi-period revenue growth analysis
    revenues = [
        item.revenue for item in financial_line_items if item.revenue is not None
    ]
    if len(revenues) >= 2:
        # Check if overall revenue grew from first to last
        initial, final = revenues[0], revenues[-1]
        if initial and final and final > initial:
            # Simple growth rate
            growth_rate = (final - initial) / abs(initial)
            if growth_rate > 0.5:  # e.g., 50% growth over the available time
                score += 2.0
                details.append(
                    f"Revenue grew by {(growth_rate * 100):.1f}% over the full period."
                )
            else:
                score += 1.0
                details.append(
                    f"Revenue growth is positive but under 50% cumulatively ({(growth_rate * 100):.1f}%)."
                )
        else:
            details.append("Revenue did not grow significantly or data insufficient.")
    else:
        details.append("Not enough revenue data for multi-period trend.")

    # 2. Operating margin and free cash flow consistency
    # We'll check if operating_margin or free_cash_flow are consistently positive/improving
    fcf_vals = [
        item.free_cash_flow
        for item in financial_line_items
        if item.free_cash_flow is not None
    ]
    op_margin_vals = [
        item.operating_margin
        for item in financial_line_items
        if item.operating_margin is not None
    ]

    if op_margin_vals:
        # Check if the majority of operating margins are > 15%
        above_15 = sum(1 for m in op_margin_vals if m > 0.15)
        if above_15 >= (len(op_margin_vals) // 2 + 1):
            score += 2.0
            details.append("Operating margins have often exceeded 15%.")
        else:
            details.append("Operating margin not consistently above 15%.")
    else:
        details.append("No operating margin data across periods.")

    if fcf_vals:
        # Check if free cash flow is positive in most periods
        positive_fcf_count = sum(1 for f in fcf_vals if f > 0)
        if positive_fcf_count >= (len(fcf_vals) // 2 + 1):
            score += 1.0
            details.append("Majority of periods show positive free cash flow.")
        else:
            details.append("Free cash flow not consistently positive.")
    else:
        details.append("No free cash flow data across periods.")

    # 3. Return on Equity (ROE) check from the latest metrics
    # (If you want multi-period ROE, you'd need that in financial_line_items as well.)
    latest_metrics = metrics[0]
    if latest_metrics.return_on_equity and latest_metrics.return_on_equity > 0.15:
        score += 2.0
        details.append(
            f"High ROE of {latest_metrics.return_on_equity:.1%}, indicating potential moat."
        )
    elif latest_metrics.return_on_equity:
        details.append(
            f"ROE of {latest_metrics.return_on_equity:.1%} is not indicative of a strong moat."
        )
    else:
        details.append("ROE data not available in metrics.")

    return {"score": score, "details": "; ".join(details)}


def analyze_financial_discipline(
    metrics: list, financial_line_items: list
) -> Dict[str, Any]:
    """
    Evaluate the company's balance sheet over multiple periods:
    - Debt ratio trends
    - Capital returns to shareholders over time (dividends, buybacks)
    """
    score: float = 0.0
    details = []

    if not metrics or not financial_line_items:
        return {
            "score": 0,
            "details": "Insufficient data to analyze financial discipline",
        }

    # 1. Multi-period debt ratio or debt_to_equity
    # Check if the company's leverage is stable or improving
    debt_to_equity_vals = [
        item.debt_to_equity
        for item in financial_line_items
        if item.debt_to_equity is not None
    ]

    # If we have multi-year data, see if D/E ratio has gone down or stayed <1 across most periods
    if debt_to_equity_vals:
        below_one_count = sum(1 for d in debt_to_equity_vals if d < 1.0)
        if below_one_count >= (len(debt_to_equity_vals) // 2 + 1):
            score += 2.0
            details.append("Debt-to-equity < 1.0 for the majority of periods.")
        else:
            details.append("Debt-to-equity >= 1.0 in many periods.")
    else:
        # Fallback to total_liabilities/total_assets if D/E not available
        liab_to_assets = []
        for item in financial_line_items:
            if item.total_liabilities and item.total_assets and item.total_assets > 0:
                liab_to_assets.append(item.total_liabilities / item.total_assets)

        if liab_to_assets:
            below_50pct_count = sum(1 for ratio in liab_to_assets if ratio < 0.5)
            if below_50pct_count >= (len(liab_to_assets) // 2 + 1):
                score += 2.0
                details.append("Liabilities-to-assets < 50% for majority of periods.")
            else:
                details.append("Liabilities-to-assets >= 50% in many periods.")
        else:
            details.append("No consistent leverage ratio data available.")

    # 2. Capital allocation approach (dividends + share counts)
    # If the company paid dividends or reduced share count over time, it may reflect discipline
    dividends_list = [
        item.dividends_and_other_cash_distributions
        for item in financial_line_items
        if item.dividends_and_other_cash_distributions is not None
    ]
    if dividends_list:
        # Check if dividends were paid (i.e., negative outflows to shareholders) in most periods
        paying_dividends_count = sum(1 for d in dividends_list if d < 0)
        if paying_dividends_count >= (len(dividends_list) // 2 + 1):
            score += 1.0
            details.append(
                "Company has a history of returning capital to shareholders (dividends)."
            )
        else:
            details.append("Dividends not consistently paid or no data.")
    else:
        details.append("No dividend data found across periods.")

    # Check for decreasing share count (simple approach):
    # We can compare first vs last if we have at least two data points
    shares = [
        item.outstanding_shares
        for item in financial_line_items
        if item.outstanding_shares is not None
    ]
    if len(shares) >= 2:
        if shares[-1] < shares[0]:
            score += 1.0
            details.append(
                "Outstanding shares have decreased over time (possible buybacks)."
            )
        else:
            details.append(
                "Outstanding shares have not decreased over the available periods."
            )
    else:
        details.append("No multi-period share count data to assess buybacks.")

    return {"score": score, "details": "; ".join(details)}


def analyze_valuation(financial_line_items: list, market_cap: float) -> Dict[str, Any]:
    """
    Ackman invests in companies trading at a discount to intrinsic value.
    We can do a simplified DCF or an FCF-based approach.
    This function currently uses the latest free cash flow only,
    but you could expand it to use an average or multi-year FCF approach.
    """
    if not financial_line_items or market_cap is None:
        return {
            "score": 0.0,  # Ensure float consistency
            "details": "Insufficient data (financial_line_items or market_cap) to perform valuation",
        }

    # Example: use the most recent item for FCF, safely accessing the attribute
    latest_item = financial_line_items[-1] if financial_line_items else None
    fcf_raw = getattr(latest_item, "free_cash_flow", None) if latest_item else None

    # Ensure fcf is a positive float before proceeding
    if fcf_raw is None or not isinstance(fcf_raw, (int, float)) or fcf_raw <= 0:
        return {
            "score": 0.0,  # Ensure float consistency
            "details": f"No positive FCF available for valuation; FCF value: {fcf_raw}",
            "intrinsic_value": None,
        }

    # Now we know fcf_raw is a positive number. Use float(fcf_raw) directly in calculations below.

    # For demonstration, let's do a naive approach:
    growth_rate: float = 0.06
    discount_rate: float = 0.10
    terminal_multiple: float = 15.0  # Ensure float
    projection_years: int = 5  # Keep as int for range()

    # The check for fcf <= 0 is now handled above before assignment

    present_value: float = 0.0  # Initialize as float
    # Use integer projection_years for range
    for year in range(1, projection_years + 1):
        # Ensure exponentiation uses floats where appropriate, though Python handles int exponents
        # Use float(fcf_raw) directly
        future_fcf = float(fcf_raw) * ((1.0 + growth_rate) ** float(year))
        pv = future_fcf / ((1.0 + discount_rate) ** float(year))
        present_value += pv

    # Terminal Value - ensure all components are float before division
    # Use float(fcf_raw) directly
    terminal_fcf_component = float(fcf_raw) * (
        (1.0 + growth_rate) ** float(projection_years)
    )
    terminal_value_numerator = (
        terminal_fcf_component * terminal_multiple
    )  # float * float
    terminal_value_denominator = (1.0 + discount_rate) ** float(
        projection_years
    )  # float ** float

    # Avoid division by zero, though discount_rate > 0 should prevent this
    if terminal_value_denominator == 0:
        terminal_value = 0.0  # Or handle as error
    else:
        terminal_value = terminal_value_numerator / terminal_value_denominator

    intrinsic_value: float = present_value + terminal_value  # float + float

    # Compare with market cap => margin of safety
    margin_of_safety = (intrinsic_value - market_cap) / market_cap

    valuation_score: float = 0.0  # Rename variable to avoid potential scope conflicts
    if margin_of_safety > 0.3:
        valuation_score += 3.0
    elif margin_of_safety > 0.1:
        valuation_score += 1.0

    details = [
        f"Calculated intrinsic value: ~{intrinsic_value:,.2f}",
        f"Market cap: ~{market_cap:,.2f}",
        f"Margin of safety: {margin_of_safety:.2%}",
    ]

    return {
        "score": valuation_score,  # Return the renamed variable
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety,
    }


def generate_ackman_output(
    ticker: str,
    analysis_data: dict[str, Any],
    model_name: str,
    model_provider: str,
) -> BillAckmanSignal:
    """
    Generates investment decisions in the style of Bill Ackman.
    """
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a Bill Ackman AI agent, making investment decisions using his principles:

            1. Seek high-quality businesses with durable competitive advantages (moats).
            2. Prioritize consistent free cash flow and growth potential.
            3. Advocate for strong financial discipline (reasonable leverage, efficient capital allocation).
            4. Valuation matters: target intrinsic value and margin of safety.
            5. Invest with high conviction in a concentrated portfolio for the long term.
            6. Potential activist approach if management or operational improvements can unlock value.


            Rules:
            - Evaluate brand strength, market position, or other moats.
            - Check free cash flow generation, stable or growing earnings.
            - Analyze balance sheet health (reasonable debt, good ROE).
            - Buy at a discount to intrinsic value; higher discount => stronger conviction.
            - Engage if management is suboptimal or if there's a path for strategic improvements.
            - Provide a rational, data-driven recommendation (bullish, bearish, or neutral).

            When providing your reasoning, be thorough and specific by:
            1. Explaining the quality of the business and its competitive advantages in detail
            2. Highlighting the specific financial metrics that most influenced your decision (FCF, margins, leverage)
            3. Discussing any potential for operational improvements or management changes
            4. Providing a clear valuation assessment with numerical evidence
            5. Identifying specific catalysts that could unlock value
            6. Using Bill Ackman's confident, analytical, and sometimes confrontational style

            For example, if bullish: "This business generates exceptional free cash flow with a 15% margin and has a dominant market position that competitors can't easily replicate. Trading at only 12x FCF, there's a 40% discount to intrinsic value, and management's recent capital allocation decisions suggest..."
            For example, if bearish: "Despite decent market position, FCF margins have deteriorated from 12% to 8% over three years. Management continues to make poor capital allocation decisions by pursuing low-ROIC acquisitions. Current valuation at 18x FCF provides no margin of safety given the operational challenges..."
            """,
            ),
            (
                "human",
                """Based on the following analysis, create an Ackman-style investment signal.

            Analysis Data for {ticker}:
            {analysis_data}

            Return the trading signal in this JSON format:
            {{
              "signal": "bullish/bearish/neutral",
              "confidence": float (0-100),
              "reasoning": "string"
            }}
            """,
            ),
        ]
    )

    prompt = template.invoke(
        {"analysis_data": json.dumps(analysis_data, indent=2), "ticker": ticker}
    )

    def create_default_bill_ackman_signal():
        return BillAckmanSignal(
            signal="neutral",
            confidence=0.0,
            reasoning="Error in analysis, defaulting to neutral",
        )

    return call_llm(
        prompt=prompt,
        model_name=model_name,
        model_provider=model_provider,
        pydantic_model=BillAckmanSignal,
        agent_name="bill_ackman_agent",
        default_factory=create_default_bill_ackman_signal,
    )
