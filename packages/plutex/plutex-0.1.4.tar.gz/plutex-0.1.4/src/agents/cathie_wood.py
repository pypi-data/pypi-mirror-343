import json
from typing import Any, Dict  # Remove unused List, Optional

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing_extensions import Literal

from src.graph.state import AgentState, show_agent_reasoning
from src.tools.api import get_financial_metrics, get_market_cap, search_line_items
from src.utils.llm import call_llm
from src.utils.progress import progress


class CathieWoodSignal(BaseModel):
    signal: Literal["bullish", "bearish", "neutral"]
    confidence: float
    reasoning: str


def cathie_wood_agent(state: AgentState):
    """
    Analyzes stocks using Cathie Wood's investing principles and LLM reasoning.
    1. Prioritizes companies with breakthrough technologies or business models
    2. Focuses on industries with rapid adoption curves and massive TAM (Total Addressable Market).
    3. Invests mostly in AI, robotics, genomic sequencing, fintech, and blockchain.
    4. Willing to endure short-term volatility for long-term gains.
    """
    data = state["data"]
    end_date = data["end_date"]
    tickers = data["tickers"]

    analysis_data = {}
    cw_analysis = {}

    for ticker in tickers:
        progress.update_status(
            "cathie_wood_agent", ticker, "Fetching financial metrics"
        )
        metrics = get_financial_metrics(ticker, end_date, period="annual", limit=5)

        progress.update_status(
            "cathie_wood_agent", ticker, "Gathering financial line items"
        )
        financial_line_items = search_line_items(
            ticker,
            [
                "revenue",
                "gross_margin",
                "operating_margin",
                "debt_to_equity",
                "free_cash_flow",
                "total_assets",
                "total_liabilities",
                "dividends_and_other_cash_distributions",
                "outstanding_shares",
                "research_and_development",
                "capital_expenditure",
                "operating_expense",
            ],
            end_date,
            period="annual",
            limit=5,
        )

        progress.update_status("cathie_wood_agent", ticker, "Getting market cap")
        market_cap = get_market_cap(ticker, end_date)

        progress.update_status(
            "cathie_wood_agent", ticker, "Analyzing disruptive potential"
        )
        disruptive_analysis = analyze_disruptive_potential(
            metrics, financial_line_items
        )

        progress.update_status(
            "cathie_wood_agent", ticker, "Analyzing innovation-driven growth"
        )
        innovation_analysis = analyze_innovation_growth(metrics, financial_line_items)

        progress.update_status(
            "cathie_wood_agent", ticker, "Calculating valuation & high-growth scenario"
        )
        if market_cap is not None:
            valuation_analysis = analyze_cathie_wood_valuation(
                financial_line_items, market_cap
            )
        else:
            valuation_analysis = {
                "score": 0.0,
                "details": "Market cap data unavailable for valuation",
            }
            progress.update_status(
                "cathie_wood_agent", ticker, "Failed: Market cap unavailable"
            )

        total_score = (
            float(disruptive_analysis.get("score", 0.0))
            + float(innovation_analysis.get("score", 0.0))
            + float(valuation_analysis.get("score", 0.0))
        )
        max_possible_score = 15.0

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
            "disruptive_analysis": disruptive_analysis,
            "innovation_analysis": innovation_analysis,
            "valuation_analysis": valuation_analysis,
        }

        progress.update_status(
            "cathie_wood_agent", ticker, "Generating Cathie Wood analysis"
        )
        # Ensure analysis_data[ticker] is passed correctly
        cw_output = generate_cathie_wood_output(
            ticker=ticker,
            analysis_data=analysis_data[ticker],
            model_name=state["metadata"]["model_name"],
            model_provider=state["metadata"]["model_provider"],
        )

        cw_analysis[ticker] = {
            "signal": cw_output.signal,
            "confidence": cw_output.confidence,
            "reasoning": cw_output.reasoning,
        }
        progress.update_status("cathie_wood_agent", ticker, "Done")

    message = HumanMessage(content=json.dumps(cw_analysis), name="cathie_wood_agent")

    if state["metadata"].get("show_reasoning"):
        show_agent_reasoning(cw_analysis, "Cathie Wood Agent")

    state["data"]["analyst_signals"]["cathie_wood_agent"] = cw_analysis

    # Ensure messages are combined as lists
    return {"messages": list(state["messages"]) + [message], "data": state["data"]}


def analyze_disruptive_potential(
    metrics: list, financial_line_items: list
) -> Dict[str, Any]:
    score = 0.0
    details = []
    if not metrics or not financial_line_items:
        return {"score": 0.0, "details": "Insufficient data"}

    revenues = [getattr(item, "revenue", None) for item in financial_line_items]
    # Keep None for indexing alignment, but check carefully before use
    if len(revenues) >= 3:
        growth_rates = []
        for i in range(len(revenues) - 1):
            rev_i = revenues[i]
            rev_i_plus_1 = revenues[i + 1]
            # Add explicit None checks before operations
            if rev_i is not None and rev_i_plus_1 is not None:
                # Add asserts to help Mypy understand types after check
                assert rev_i is not None
                assert rev_i_plus_1 is not None
                denominator = abs(rev_i)
                if denominator > 1e-9:
                    growth_rate = (rev_i_plus_1 - rev_i) / denominator
                    growth_rates.append(growth_rate)
                else:
                    growth_rates.append(0.0)  # Handle zero denominator
            else:
                growth_rates.append(0.0)  # Handle None values
        if len(growth_rates) >= 2 and growth_rates[-1] > growth_rates[0]:
            score += 2.0
            details.append(
                f"Revenue growth accelerating: {growth_rates[-1] * 100:.1f}% vs {growth_rates[0] * 100:.1f}%"
            )
        latest_growth = growth_rates[-1] if growth_rates else 0.0
        if latest_growth > 1.0:
            score += 3.0
            details.append(f"Exceptional revenue growth: {latest_growth * 100:.1f}%")
        elif latest_growth > 0.5:
            score += 2.0
            details.append(f"Strong revenue growth: {latest_growth * 100:.1f}%")
        elif latest_growth > 0.2:
            score += 1.0
            details.append(f"Moderate revenue growth: {latest_growth * 100:.1f}%")
    else:
        details.append("Insufficient revenue data")

    gross_margins = [
        getattr(item, "gross_margin", None) for item in financial_line_items
    ]
    gross_margins_filtered = [
        gm for gm in gross_margins if gm is not None
    ]  # Filter None values
    if len(gross_margins_filtered) >= 2:
        gm_first = gross_margins_filtered[0]
        gm_last = gross_margins_filtered[-1]
        # Add asserts even after filtering, to be extra sure for Mypy
        assert gm_first is not None
        assert gm_last is not None
        margin_trend = gm_last - gm_first
        if margin_trend > 0.05:
            score += 2.0
            details.append(f"Expanding gross margins: +{margin_trend * 100:.1f}%")
        elif margin_trend > 0:
            score += 1.0
            details.append(
                f"Slightly improving gross margins: +{margin_trend * 100:.1f}%"
            )
        # Add assert for the comparison
        assert gm_last is not None
        if gm_last > 0.50:
            score += 2.0
            details.append(f"High gross margin: {gm_last * 100:.1f}%")
    else:
        details.append("Insufficient gross margin data")

    operating_expenses = [
        getattr(item, "operating_expense", None) for item in financial_line_items
    ]
    # Keep None for indexing alignment, check carefully before use
    if len(revenues) >= 2 and len(operating_expenses) >= 2:
        rev_0 = revenues[0]
        opex_0 = operating_expenses[0]
        rev_last = revenues[-1]
        opex_last = operating_expenses[-1]
        # Add explicit None checks before operations
        if (
            rev_0 is not None
            and opex_0 is not None
            and rev_last is not None
            and opex_last is not None
        ):
            # Add asserts to help Mypy
            assert rev_0 is not None
            assert opex_0 is not None
            assert rev_last is not None
            assert opex_last is not None
            rev_denom = abs(rev_0)
            opex_denom = abs(opex_0)
            if rev_denom > 1e-9 and opex_denom > 1e-9:
                rev_growth = (rev_last - rev_0) / rev_denom
                opex_growth = (opex_last - opex_0) / opex_denom
                if rev_growth > opex_growth:
                    score += 2.0
                    details.append("Positive operating leverage")
            else:
                details.append(
                    "Cannot calculate operating leverage due to zero denominator"
                )
        else:
            details.append("Cannot calculate operating leverage")
    else:
        details.append("Insufficient data for operating leverage")

    rd_expenses = [
        getattr(item, "research_and_development", None) for item in financial_line_items
    ]
    # rd_expenses = [rd for rd in rd_expenses if rd is not None] # Keep None
    # Check lengths and last elements for None before proceeding
    if (
        len(rd_expenses) > 0
        and len(revenues) > 0
        and revenues[-1] is not None
        and rd_expenses[-1] is not None
    ):
        rev_last = revenues[-1]
        rd_last = rd_expenses[-1]
        if abs(rev_last) > 1e-9:  # Check denominator
            rd_intensity = rd_last / rev_last
            if rd_intensity > 0.15:
                score += 3.0
                details.append(f"High R&D investment: {rd_intensity * 100:.1f}%")
            elif rd_intensity > 0.08:
                score += 2.0
                details.append(f"Moderate R&D investment: {rd_intensity * 100:.1f}%")
            elif rd_intensity > 0.05:
                score += 1.0
                details.append(f"Some R&D investment: {rd_intensity * 100:.1f}%")
        else:
            details.append("Missing recent R&D expense")
    else:
        details.append("No R&D data or revenue is zero/missing")

    max_possible_score = 12.0
    normalized_score = (
        (score / max_possible_score) * 5.0 if max_possible_score > 0 else 0.0
    )
    return {
        "score": normalized_score,
        "details": "; ".join(details),
        "raw_score": score,
        "max_score": max_possible_score,
    }


def analyze_innovation_growth(
    metrics: list, financial_line_items: list
) -> Dict[str, Any]:
    score = 0.0
    details = []
    if not metrics or not financial_line_items:
        return {"score": 0.0, "details": "Insufficient data"}

    rd_expenses = [
        getattr(item, "research_and_development", None) for item in financial_line_items
    ]
    rd_expenses = [rd for rd in rd_expenses if rd is not None]
    revenues = [getattr(item, "revenue", None) for item in financial_line_items]
    revenues = [r for r in revenues if r is not None]
    if rd_expenses and revenues and len(rd_expenses) >= 2 and len(revenues) >= 2:
        if (
            rd_expenses[0] is not None
            and abs(rd_expenses[0]) > 1e-9
            and rd_expenses[-1] is not None
        ):
            rd_growth = (rd_expenses[-1] - rd_expenses[0]) / abs(rd_expenses[0])
            if rd_growth > 0.5:
                score += 3.0
                details.append(f"Strong R&D growth: +{rd_growth * 100:.1f}%")
            elif rd_growth > 0.2:
                score += 2.0
                details.append(f"Moderate R&D growth: +{rd_growth * 100:.1f}%")
        else:
            details.append("Cannot calculate R&D growth")
        if (
            revenues[0] is not None
            and abs(revenues[0]) > 1e-9
            and revenues[-1] is not None
            and abs(revenues[-1]) > 1e-9
            and rd_expenses[0] is not None
            and rd_expenses[-1] is not None
        ):
            rd_intensity_start = rd_expenses[0] / revenues[0]
            rd_intensity_end = rd_expenses[-1] / revenues[-1]
            if rd_intensity_end > rd_intensity_start:
                score += 2.0
                details.append(
                    f"Increasing R&D intensity: {rd_intensity_end * 100:.1f}% vs {rd_intensity_start * 100:.1f}%"
                )
        else:
            details.append("Cannot calculate R&D intensity trend")
    else:
        details.append("Insufficient R&D/revenue data")

    fcf_vals = [getattr(item, "free_cash_flow", None) for item in financial_line_items]
    # fcf_vals = [fcf for fcf in fcf_vals if fcf is not None] # Keep None
    if len(fcf_vals) >= 2:
        fcf_growth = 0.0  # Default
        # Add explicit None checks before operations
        if fcf_vals[0] is not None and fcf_vals[-1] is not None:
            fcf_denom = abs(fcf_vals[0])
            if fcf_denom > 1e-9:
                fcf_growth = (fcf_vals[-1] - fcf_vals[0]) / fcf_denom
            else:
                details.append("Cannot calculate FCF growth (zero denominator)")
        else:
            details.append("Cannot calculate FCF growth (missing data)")

        # Filter out None before sum/len comparison
        # Ensure the generator yields bools implicitly for sum, check f > 0 only if not None
        positive_fcf_count = sum(1 for f in fcf_vals if f is not None and f > 0)
        valid_fcf_count = sum(
            1 for f in fcf_vals if f is not None
        )  # Count non-None values

        # Check if valid_fcf_count is zero before comparing percentages
        if valid_fcf_count > 0:
            if fcf_growth > 0.3 and positive_fcf_count == valid_fcf_count:
                score += 3.0
                details.append("Strong & consistent FCF growth")
            elif positive_fcf_count >= valid_fcf_count * 0.75:
                score += 2.0
                details.append("Consistent positive FCF")
            elif positive_fcf_count > valid_fcf_count * 0.5:
                score += 1.0
                details.append("Moderately consistent FCF")
        else:
            details.append("No valid FCF data points to calculate consistency")
    else:
        details.append("Insufficient FCF data")

    op_margin_vals = [
        getattr(item, "operating_margin", None) for item in financial_line_items
    ]
    # Keep None for indexing alignment, check carefully before use
    if len(op_margin_vals) >= 2:
        op_margin_0 = op_margin_vals[0]
        op_margin_last = op_margin_vals[-1]
        # Add explicit None checks before operations
        if op_margin_0 is not None and op_margin_last is not None:
            # Add asserts to help Mypy
            assert op_margin_0 is not None
            assert op_margin_last is not None
            margin_trend = op_margin_last - op_margin_0
            latest_margin = op_margin_last
            if latest_margin > 0.15 and margin_trend > 0:
                score += 3.0
                details.append(
                    f"Strong & improving op margin: {latest_margin * 100:.1f}%"
                )
            elif latest_margin > 0.10:
                score += 2.0
                details.append(f"Healthy op margin: {latest_margin * 100:.1f}%")
            elif margin_trend > 0:
                score += 1.0
                details.append("Improving operating efficiency")
        else:
            details.append("Cannot calculate op margin trend (missing data)")
    else:
        details.append("Insufficient op margin data")

    capex = [
        getattr(item, "capital_expenditure", None) for item in financial_line_items
    ]
    # capex = [c for c in capex if c is not None] # Keep None
    if len(capex) >= 2 and len(revenues) >= 2:
        capex_intensity = 0.0  # Default
        capex_growth = 0.0  # Default
        # Add explicit None checks before operations
        if revenues[-1] is not None and capex[-1] is not None:
            rev_last = revenues[-1]
            capex_last = capex[-1]
            if abs(rev_last) > 1e-9:
                capex_intensity = abs(capex_last) / rev_last
            else:
                details.append("Cannot calculate CAPEX intensity (zero revenue)")

        if capex[0] is not None and capex[-1] is not None:
            capex_first = capex[0]
            capex_last = capex[-1]
            capex_denom = abs(capex_first)
            if capex_denom > 1e-9:
                capex_growth = (abs(capex_last) - abs(capex_first)) / capex_denom
            else:
                details.append("Cannot calculate CAPEX growth (zero denominator)")

        if capex_intensity > 0.10 and capex_growth > 0.2:
            score += 2.0
            details.append("Strong growth investment")
        elif capex_intensity > 0.05:
            score += 1.0
            details.append("Moderate growth investment")
    else:
        details.append("Insufficient CAPEX/revenue data")

    dividends = [
        getattr(item, "dividends_and_other_cash_distributions", None)
        for item in financial_line_items
    ]
    # dividends = [d for d in dividends if d is not None] # Keep None
    # Need to re-fetch fcf_vals with Nones kept
    fcf_vals_with_none = [
        getattr(item, "free_cash_flow", None) for item in financial_line_items
    ]
    if len(dividends) > 0 and len(fcf_vals_with_none) > 0:
        fcf_last = fcf_vals_with_none[-1]
        div_last = dividends[-1]
        # Add explicit None checks before operations
        if fcf_last is not None and div_last is not None:
            if abs(fcf_last) > 1e-9:
                latest_payout_ratio = div_last / fcf_last
                if latest_payout_ratio < 0.2:
                    score += 2.0
                    details.append("Strong reinvestment focus")
                elif latest_payout_ratio < 0.4:
                    score += 1.0
                    details.append("Moderate reinvestment focus")
            else:
                details.append("Missing recent dividend data")
        else:
            details.append("Cannot calculate payout ratio (FCF zero)")
    else:
        details.append("Insufficient dividend/FCF data")

    max_possible_score = 15.0
    normalized_score = (
        (score / max_possible_score) * 5.0 if max_possible_score > 0 else 0.0
    )
    return {
        "score": normalized_score,
        "details": "; ".join(details),
        "raw_score": score,
        "max_score": max_possible_score,
    }


def analyze_cathie_wood_valuation(
    financial_line_items: list, market_cap: float
) -> Dict[str, Any]:
    if not financial_line_items or market_cap is None:
        return {"score": 0.0, "details": "Insufficient data"}

    latest = financial_line_items[-1]
    fcf = getattr(latest, "free_cash_flow", 0.0) or 0.0
    if fcf <= 0:
        return {
            "score": 0.0,
            "details": f"No positive FCF ({fcf})",
            "intrinsic_value": None,
        }

    growth_rate = 0.20
    discount_rate = 0.15
    terminal_multiple = 25
    projection_years = 5
    present_value = 0.0
    for year in range(1, projection_years + 1):
        future_fcf = fcf * (1 + growth_rate) ** year
        pv = future_fcf / ((1 + discount_rate) ** year)
        present_value += pv
    terminal_value = (
        fcf * (1 + growth_rate) ** projection_years * terminal_multiple
    ) / ((1 + discount_rate) ** projection_years)
    intrinsic_value = present_value + terminal_value
    margin_of_safety = (intrinsic_value - market_cap) / market_cap

    score = 0.0  # Initialize score as float
    if margin_of_safety > 0.5:
        score += 3.0
    elif margin_of_safety > 0.2:
        score += 1.0  # Ensure float increment

    details = [
        f"Intrinsic Value: ~{intrinsic_value:,.2f}",
        f"Market Cap: ~{market_cap:,.2f}",
        f"Margin of Safety: {margin_of_safety:.2%}",
    ]
    # Ensure score is returned as float
    return {
        "score": float(score),
        "details": "; ".join(details),
        "intrinsic_value": intrinsic_value,
        "margin_of_safety": margin_of_safety,
    }


def generate_cathie_wood_output(
    ticker: str,
    analysis_data: dict[str, Any],  # Change any to Any
    model_name: str,
    model_provider: str,
) -> CathieWoodSignal:
    template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a Cathie Wood AI agent... [System prompt content omitted for brevity]""",
            ),
            (
                "human",
                """Based on the following analysis, create a Cathie Wood-style investment signal.
            Analysis Data for {ticker}: {analysis_data}
            Return the trading signal in this JSON format: {{ "signal": "bullish/bearish/neutral", "confidence": float (0-100), "reasoning": "string" }}""",
            ),
        ]
    )
    prompt = template.invoke(
        {"analysis_data": json.dumps(analysis_data, indent=2), "ticker": ticker}
    )

    def create_default_cathie_wood_signal():
        return CathieWoodSignal(
            signal="neutral", confidence=0.0, reasoning="Error in analysis"
        )

    return call_llm(
        prompt=prompt,
        model_name=model_name,
        model_provider=model_provider,
        pydantic_model=CathieWoodSignal,
        agent_name="cathie_wood_agent",
        default_factory=create_default_cathie_wood_signal,
    )


# source: https://ark-invest.com
