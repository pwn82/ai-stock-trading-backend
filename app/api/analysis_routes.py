from fastapi import APIRouter, HTTPException

from app.models.schemas import (
    StockAnalysisRequest
)

from app.services.market_data_service import (
    market_data_service
)

from app.services.news_service import (
    news_service
)

from app.crew.trading_crew import (
    trading_crew
)


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


@router.post("/run")
def run_analysis(
    request: StockAnalysisRequest
):

    try:

        stock_symbol = (
            request.stock_symbol
            .strip()
            .upper()
        )

        user_question = (
            request.user_question
            or
            f"Analyze {stock_symbol}"
        )

        market_data = (
            market_data_service
            .get_market_data(
                stock_symbol,
                user_question
            )
        )

        news_data = {}

        if request.news_impact_consideration:

            news_data = (
                news_service
                .search_news(
                    stock_symbol
                )
            )

        crew_result = trading_crew.run(

            stock_symbol=stock_symbol,

            capital=request.capital,

            risk_tolerance=request.risk_tolerance,

            strategy_preference=(
                request.strategy_preference
            ),

            news_impact=(
                request.news_impact_consideration
            ),

            market_data=market_data,

            news_data=news_data,

            user_question=user_question
        )

        selected_files = []

        for dataset in market_data.get(
            "datasets",
            []
        ):

            selected_files.append(
                dataset["file"]
            )

        tasks = crew_result["tasks"]

        return {

            "stock_symbol": stock_symbol,

            "selected_files": selected_files,

            "market_data": {
                "files_found":
                    market_data.get(
                        "files_found",
                        0
                    ),

                "indicators":
                    market_data.get(
                        "indicators",
                        []
                    )
            },

            "data_analysis":
                tasks[0]["output"],

            "trading_strategy":
                tasks[1]["output"],

            "execution_plan":
                tasks[2]["output"],

            "risk_report":
                tasks[3]["output"],

            "final_recommendation":
                tasks[3]["output"],

            "agents": tasks
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )