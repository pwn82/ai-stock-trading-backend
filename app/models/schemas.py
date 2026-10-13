from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class StockAnalysisRequest(BaseModel):
    stock_symbol: str = Field(..., min_length=1)
    capital: float = Field(..., gt=0)

    risk_tolerance: str = Field(
        default="moderate"
    )

    strategy_preference: str = Field(
        default="trend following"
    )

    news_impact_consideration: bool = True

    user_question: Optional[str] = None


class CsvFileInfo(BaseModel):
    file_name: str
    full_path: str
    size_mb: float
    modified_time: str
    columns: List[str] = []


class CsvSearchRequest(BaseModel):
    stock_symbol: str
    question: Optional[str] = None


class ChatRequest(BaseModel):
    question: str
    stock_symbol: Optional[str] = None


class AgentResult(BaseModel):
    agent: str
    output: str


class AnalysisResponse(BaseModel):
    stock_symbol: str

    selected_files: List[Dict[str, Any]]

    market_data: Dict[str, Any]

    data_analysis: str

    trading_strategy: str

    execution_plan: str

    risk_report: str

    final_recommendation: str

    agents: List[AgentResult]