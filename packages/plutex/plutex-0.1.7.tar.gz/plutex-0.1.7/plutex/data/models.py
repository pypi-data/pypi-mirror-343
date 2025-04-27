from pydantic import BaseModel
from typing import Union, List, Dict


class Price(BaseModel):
    open: float
    close: float
    high: float
    low: float
    volume: int
    time: str


class PriceResponse(BaseModel):
    ticker: str
    prices: List[Price]


class FinancialMetrics(BaseModel):
    ticker: str
    report_period: str
    period: str
    currency: str
    market_cap: Union[float, None]
    enterprise_value: Union[float, None]
    price_to_earnings_ratio: Union[float, None]
    price_to_book_ratio: Union[float, None]
    price_to_sales_ratio: Union[float, None]
    enterprise_value_to_ebitda_ratio: Union[float, None]
    enterprise_value_to_revenue_ratio: Union[float, None]
    free_cash_flow_yield: Union[float, None]
    peg_ratio: Union[float, None]
    gross_margin: Union[float, None]
    operating_margin: Union[float, None]
    net_margin: Union[float, None]
    return_on_equity: Union[float, None]
    return_on_assets: Union[float, None]
    return_on_invested_capital: Union[float, None]
    asset_turnover: Union[float, None]
    inventory_turnover: Union[float, None]
    receivables_turnover: Union[float, None]
    days_sales_outstanding: Union[float, None]
    operating_cycle: Union[float, None]
    working_capital_turnover: Union[float, None]
    current_ratio: Union[float, None]
    quick_ratio: Union[float, None]
    cash_ratio: Union[float, None]
    operating_cash_flow_ratio: Union[float, None]
    debt_to_equity: Union[float, None]
    debt_to_assets: Union[float, None]
    interest_coverage: Union[float, None]
    revenue_growth: Union[float, None]
    earnings_growth: Union[float, None]
    book_value_growth: Union[float, None]
    earnings_per_share_growth: Union[float, None]
    free_cash_flow_growth: Union[float, None]
    operating_income_growth: Union[float, None]
    ebitda_growth: Union[float, None]
    payout_ratio: Union[float, None]
    earnings_per_share: Union[float, None]
    book_value_per_share: Union[float, None]
    free_cash_flow_per_share: Union[float, None]


class FinancialMetricsResponse(BaseModel):
    financial_metrics: List[FinancialMetrics]


class LineItem(BaseModel):
    ticker: str
    report_period: str
    period: str
    currency: str

    # Allow additional fields dynamically
    model_config = {"extra": "allow"}


class LineItemResponse(BaseModel):
    search_results: List[LineItem]


class InsiderTrade(BaseModel):
    ticker: str
    issuer: Union[str, None]
    name: Union[str, None]
    title: Union[str, None]
    is_board_director: Union[bool, None]
    transaction_date: Union[str, None]
    transaction_shares: Union[float, None]
    transaction_price_per_share: Union[float, None]
    transaction_value: Union[float, None]
    shares_owned_before_transaction: Union[float, None]
    shares_owned_after_transaction: Union[float, None]
    security_title: Union[str, None]
    filing_date: str


class InsiderTradeResponse(BaseModel):
    insider_trades: List[InsiderTrade]


class CompanyNews(BaseModel):
    ticker: str
    title: str
    author: str
    source: str
    date: str
    url: str
    sentiment: Union[str, None] = None


class CompanyNewsResponse(BaseModel):
    news: List[CompanyNews]


class Position(BaseModel):
    cash: float = 0.0
    shares: int = 0
    ticker: str


class Portfolio(BaseModel):
    positions: Dict[str, Position]  # ticker -> Position mapping
    total_cash: float = 0.0


class AnalystSignal(BaseModel):
    signal: Union[str, None] = None
    confidence: Union[float, None] = None
    reasoning: Union[Dict, str, None] = (
        None  # Note: dict | Union[str, None] becomes Union[Dict, str, None]
    )
    max_position_size: Union[float, None] = None  # For risk management signals


class TickerAnalysis(BaseModel):
    ticker: str
    analyst_signals: Dict[str, AnalystSignal]  # agent_name -> signal mapping


class AgentStateData(BaseModel):
    tickers: List[str]
    portfolio: Portfolio
    start_date: str
    end_date: str
    ticker_analyses: Dict[str, TickerAnalysis]  # ticker -> analysis mapping


class AgentStateMetadata(BaseModel):
    show_reasoning: bool = False
    model_config = {"extra": "allow"}
