import json
from statistics import median

from langchain_core.messages import HumanMessage

from src.graph.state import AgentState, show_agent_reasoning
from src.tools.api import get_financial_metrics, get_market_cap, search_line_items
from src.utils.progress import progress


##### Valuation Agent #####
def valuation_agent(state: AgentState):
    """Performs detailed valuation analysis using multiple methodologies for multiple tickers."""
    data = state["data"]
    end_date = data["end_date"]
    tickers = data["tickers"]

    # Initialize valuation analysis for each ticker
    valuation_analysis = {}

    for ticker in tickers:
        progress.update_status("valuation_agent", ticker, "Fetching financial data")

        # Fetch the financial metrics
        financial_metrics = get_financial_metrics(
            ticker=ticker,
            end_date=end_date,
            period="ttm",
            limit=8,  # Fetch 8 periods for median EV/EBITDA
        )

        # Add safety check for financial metrics
        if not financial_metrics:
            progress.update_status(
                "valuation_agent", ticker, "Failed: No financial metrics found"
            )
            continue

        metrics = financial_metrics[0]

        progress.update_status("valuation_agent", ticker, "Gathering line items")
        # Fetch the specific line_items that we need for valuation purposes
        financial_line_items = search_line_items(
            ticker=ticker,
            line_items=[
                "free_cash_flow",
                "net_income",
                "depreciation_and_amortization",
                "capital_expenditure",
                "working_capital",
            ],
            end_date=end_date,
            period="ttm",
            limit=2,
        )

        # Add safety check for financial line items
        if len(financial_line_items) < 2:
            progress.update_status(
                "valuation_agent", ticker, "Failed: Insufficient financial line items"
            )
            continue

        # Pull the current and previous financial line items
        current_financial_line_item = financial_line_items[0]
        previous_financial_line_item = financial_line_items[1]

        progress.update_status("valuation_agent", ticker, "Calculating owner earnings")
        # Safely access dynamic attributes using getattr with default 0.0
        current_wc = getattr(current_financial_line_item, "working_capital", 0.0)
        previous_wc = getattr(previous_financial_line_item, "working_capital", 0.0)
        current_ni = getattr(current_financial_line_item, "net_income", 0.0)
        current_da = getattr(
            current_financial_line_item, "depreciation_and_amortization", 0.0
        )
        current_ce = getattr(current_financial_line_item, "capital_expenditure", 0.0)
        current_fcf = getattr(current_financial_line_item, "free_cash_flow", 0.0)

        # Calculate working capital change, handle potential None from getattr
        working_capital_change = (current_wc or 0.0) - (previous_wc or 0.0)

        # Provide default growth rate if None
        growth_rate = (
            metrics.earnings_growth if metrics.earnings_growth is not None else 0.0
        )

        # Owner Earnings Valuation (Buffett Method)
        owner_earnings_value = calculate_owner_earnings_value(
            net_income=(current_ni or 0.0),
            depreciation=(current_da or 0.0),
            capex=(current_ce or 0.0),
            working_capital_change=working_capital_change,
            growth_rate=growth_rate,
            required_return=0.15,
            margin_of_safety=0.25,
        )

        progress.update_status("valuation_agent", ticker, "Calculating DCF value")
        # DCF Valuation
        dcf_value = calculate_intrinsic_value(
            free_cash_flow=(current_fcf or 0.0),
            growth_rate=growth_rate,
            discount_rate=0.10,
            terminal_growth_rate=0.03,
            num_years=5,
        )

        progress.update_status("valuation_agent", ticker, "Calculating EV/EBITDA value")
        # Implied Equity Value
        ev_ebitda_value = calculate_ev_ebitda_value(financial_metrics)

        progress.update_status(
            "valuation_agent", ticker, "Calculating Residual Income value"
        )
        # Residual Income Model
        rim_value = calculate_residual_income_value(
            market_cap=metrics.market_cap,
            net_income=current_ni,
            price_to_book_ratio=metrics.price_to_book_ratio,
            book_value_growth=metrics.book_value_growth or 0.03,
        )

        progress.update_status("valuation_agent", ticker, "Aggregating valuations")
        # Get the market cap
        market_cap = get_market_cap(ticker=ticker, end_date=end_date)

        # Check if market_cap is valid before calculating gaps
        if market_cap is None or market_cap <= 0:
            progress.update_status(
                "valuation_agent", ticker, "Failed: Invalid market cap for valuation"
            )
            continue  # Skip to next ticker if market cap is invalid

        # Define valuation methods, their values, and weights
        method_values = {
            "dcf": {"value": dcf_value, "weight": 0.35},
            "owner_earnings": {"value": owner_earnings_value, "weight": 0.35},
            "ev_ebitda": {"value": ev_ebitda_value, "weight": 0.20},
            "residual_income": {"value": rim_value, "weight": 0.10},
        }

        # Calculate total weight of valid (non-zero) methods
        total_weight = sum(
            v["weight"]
            for v in method_values.values()
            if v["value"] is not None and v["value"] > 0
        )
        if total_weight == 0:
            progress.update_status(
                "valuation_agent",
                ticker,
                "Failed: All valuation methods zero or invalid",
            )
            continue  # Skip if no valid methods

        # Calculate gap for each method
        for v in method_values.values():
            if v["value"] is not None and v["value"] > 0:
                v["gap"] = (v["value"] - market_cap) / market_cap
            else:
                v["gap"] = None  # Assign None if value is invalid or zero

        # Calculate weighted gap, considering only valid methods
        weighted_gap = (
            sum(
                v["weight"] * v["gap"]
                for v in method_values.values()
                if v["gap"] is not None
            )
            / total_weight
        )

        # Determine overall signal based on weighted gap
        signal = (
            "bullish"
            if weighted_gap > 0.15
            else "bearish"
            if weighted_gap < -0.15
            else "neutral"
        )
        confidence = round(
            min(abs(weighted_gap) / 0.30 * 100, 100)
        )  # Normalize confidence

        # Create detailed reasoning for each method
        reasoning = {}
        for method_name, vals in method_values.items():
            if (
                vals["value"] is not None
                and vals["value"] > 0
                and vals["gap"] is not None
            ):
                method_signal = (
                    "bullish"
                    if vals["gap"] > 0.15
                    else "bearish"
                    if vals["gap"] < -0.15
                    else "neutral"
                )
                details = (
                    f"Value: ${vals['value']:,.2f}, Market Cap: ${market_cap:,.2f}, "
                    f"Gap: {vals['gap']:.1%}, Weight: {vals['weight'] * 100:.0f}%"
                )
                reasoning[f"{method_name}_analysis"] = {
                    "signal": method_signal,
                    "details": details,
                }
            elif (
                vals["value"] is not None
            ):  # Handle cases where value exists but gap couldn't be calculated (e.g., zero market cap) or value is zero
                reasoning[f"{method_name}_analysis"] = {
                    "signal": "neutral",  # Or indicate invalid? Neutral seems safer.
                    "details": f"Value: ${vals['value']:,.2f}, Market Cap: ${market_cap:,.2f}, Gap: N/A, Weight: {vals['weight'] * 100:.0f}% (Method resulted in zero or invalid value)",
                }

        valuation_analysis[ticker] = {
            "signal": signal,
            "confidence": confidence,
            "reasoning": reasoning,
        }

        progress.update_status("valuation_agent", ticker, "Done")

    message = HumanMessage(
        content=json.dumps(valuation_analysis),
        name="valuation_agent",
    )

    # Print the reasoning if the flag is set
    if state["metadata"]["show_reasoning"]:
        show_agent_reasoning(valuation_analysis, "Valuation Analysis Agent")

    # Add the signal to the analyst_signals list
    state["data"]["analyst_signals"]["valuation_agent"] = valuation_analysis

    return {
        "messages": [message],
        "data": data,
    }


def calculate_owner_earnings_value(
    net_income: float,
    depreciation: float,
    capex: float,
    working_capital_change: float,
    growth_rate: float = 0.05,
    required_return: float = 0.15,
    margin_of_safety: float = 0.25,
    num_years: int = 5,
) -> float:
    """
    Calculates the intrinsic value using Buffett's Owner Earnings method.

    Owner Earnings = Net Income
                    + Depreciation/Amortization
                    - Capital Expenditures
                    - Working Capital Changes

    Args:
        net_income: Annual net income
        depreciation: Annual depreciation and amortization
        capex: Annual capital expenditures
        working_capital_change: Annual change in working capital
        growth_rate: Expected growth rate
        required_return: Required rate of return (Buffett typically uses 15%)
        margin_of_safety: Margin of safety to apply to final value
        num_years: Number of years to project

    Returns:
        float: Intrinsic value with margin of safety
    """
    if not all(
        [
            isinstance(x, (int, float))
            for x in [net_income, depreciation, capex, working_capital_change]
        ]
    ):
        return 0

    # Calculate initial owner earnings
    owner_earnings = net_income + depreciation - capex - working_capital_change

    if owner_earnings <= 0:
        return 0

    # Project future owner earnings
    future_values = []
    for year in range(1, num_years + 1):
        future_value = owner_earnings * (1 + growth_rate) ** year
        discounted_value = future_value / (1 + required_return) ** year
        future_values.append(discounted_value)

    # Calculate terminal value (using perpetuity growth formula)
    terminal_growth = min(growth_rate, 0.03)  # Cap terminal growth at 3%
    terminal_value = (future_values[-1] * (1 + terminal_growth)) / (
        required_return - terminal_growth
    )
    terminal_value_discounted = terminal_value / (1 + required_return) ** num_years

    # Sum all values and apply margin of safety
    intrinsic_value = sum(future_values) + terminal_value_discounted
    value_with_safety_margin = intrinsic_value * (1 - margin_of_safety)

    return value_with_safety_margin


def calculate_intrinsic_value(
    free_cash_flow: float,
    growth_rate: float = 0.05,
    discount_rate: float = 0.10,
    terminal_growth_rate: float = 0.02,
    num_years: int = 5,
) -> float:
    """
    Computes the discounted cash flow (DCF) for a given company based on the current free cash flow.
    Use this function to calculate the intrinsic value of a stock.
    """
    # Estimate the future cash flows based on the growth rate
    cash_flows = [free_cash_flow * (1 + growth_rate) ** i for i in range(num_years)]

    # Calculate the present value of projected cash flows
    present_values = []
    for i in range(num_years):
        present_value = cash_flows[i] / (1 + discount_rate) ** (i + 1)
        present_values.append(present_value)

    # Calculate the terminal value
    terminal_value = (
        cash_flows[-1]
        * (1 + terminal_growth_rate)
        / (discount_rate - terminal_growth_rate)
    )
    terminal_present_value = terminal_value / (1 + discount_rate) ** num_years

    # Sum up the present values and terminal value
    dcf_value = sum(present_values) + terminal_present_value

    return dcf_value


def calculate_working_capital_change(
    current_working_capital: float,
    previous_working_capital: float,
) -> float:
    """
    Calculate the absolute change in working capital between two periods.
    A positive change means more capital is tied up in working capital (cash outflow).
    A negative change means less capital is tied up (cash inflow).

    Args:
        current_working_capital: Current period's working capital
        previous_working_capital: Previous period's working capital

    Returns:
        float: Change in working capital (current - previous)
    """
    return current_working_capital - previous_working_capital


def calculate_ev_ebitda_value(financial_metrics: list):
    """Implied equity value via median EV/EBITDA multiple."""
    if not financial_metrics:
        return 0
    m0 = financial_metrics[0]
    # Ensure required metrics are present and valid
    if not (
        m0.enterprise_value
        and m0.enterprise_value_to_ebitda_ratio
        and m0.enterprise_value_to_ebitda_ratio != 0
    ):
        return 0

    ebitda_now = m0.enterprise_value / m0.enterprise_value_to_ebitda_ratio
    # Calculate median safely, filtering None or zero values
    valid_ratios = [
        m.enterprise_value_to_ebitda_ratio
        for m in financial_metrics
        if m.enterprise_value_to_ebitda_ratio is not None
        and m.enterprise_value_to_ebitda_ratio != 0
    ]
    if not valid_ratios:
        return 0  # Return 0 if no valid ratios found
    med_mult = median(valid_ratios)

    ev_implied = med_mult * ebitda_now
    # Calculate net debt safely, handling potential None values
    net_debt = (m0.enterprise_value or 0) - (m0.market_cap or 0)
    return max(ev_implied - net_debt, 0)


def calculate_residual_income_value(
    market_cap: float | None,
    net_income: float | None,
    price_to_book_ratio: float | None,
    book_value_growth: float = 0.03,
    cost_of_equity: float = 0.10,
    terminal_growth_rate: float = 0.03,
    num_years: int = 5,
):
    """Residual Income Model (Edwards‑Bell‑Ohlson)."""
    # Ensure all required inputs are valid numbers and price_to_book_ratio is positive
    if not (
        market_cap
        and net_income
        and price_to_book_ratio
        and price_to_book_ratio > 0
        and isinstance(market_cap, (int, float))
        and isinstance(net_income, (int, float))
        and isinstance(price_to_book_ratio, (int, float))
    ):
        return 0

    book_val = market_cap / price_to_book_ratio
    ri0 = net_income - cost_of_equity * book_val
    # Residual income must be positive to proceed
    if ri0 <= 0:
        return 0

    pv_ri = 0.0
    # Calculate present value of future residual incomes
    for yr in range(1, num_years + 1):
        ri_t = ri0 * (1 + book_value_growth) ** yr
        pv_ri += ri_t / (1 + cost_of_equity) ** yr

    # Calculate terminal residual income and its present value
    # Ensure terminal growth rate is less than cost of equity
    if cost_of_equity <= terminal_growth_rate:
        # Handle case where cost of equity is not greater than terminal growth rate
        # Option 1: Return current book value + PV of RI (conservative)
        # Option 2: Use a modified terminal growth rate (e.g., cost_of_equity - small_epsilon)
        # Option 3: Return 0 or raise an error
        # Choosing Option 1 for conservatism here:
        # return book_val + pv_ri
        # Or let's return 0 to indicate valuation failure in this edge case
        return 0  # Indicate failure if cost_of_equity <= terminal_growth_rate

    term_ri = (
        ri0
        * (1 + book_value_growth) ** (num_years + 1)
        / (cost_of_equity - terminal_growth_rate)
    )
    pv_term = term_ri / (1 + cost_of_equity) ** num_years

    intrinsic = book_val + pv_ri + pv_term
    # Apply a margin of safety (e.g., 20%)
    return intrinsic * 0.8
