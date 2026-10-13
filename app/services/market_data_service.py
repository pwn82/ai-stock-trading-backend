import pandas as pd

from app.services.csv_file_service import csv_file_service

from app.utils.indicators import (
    calculate_indicators
)


class MarketDataService:

    def get_market_data(
        self,
        stock_symbol: str,
        question: str = ""
    ):

        datasets = csv_file_service.get_relevant_data(
            stock_symbol,
            question
        )

        if not datasets:

            return {
                "stock_symbol": stock_symbol,
                "files_found": 0,
                "datasets": [],
                "indicators": {},
                "message":
                    "No matching stock CSV data found."
            }

        all_indicators = []

        for dataset in datasets:

            df = pd.DataFrame(
                dataset["data"]
            )

            indicators = calculate_indicators(
                df
            )

            all_indicators.append({
                "file": dataset["file"]["full_path"],
                "indicators": indicators
            })

        return {
            "stock_symbol": stock_symbol,
            "files_found": len(datasets),
            "datasets": datasets,
            "indicators": all_indicators
        }


market_data_service = MarketDataService()