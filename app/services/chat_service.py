import re

from crewai import LLM
import pandas as pd

from app.core.config import get_settings
from app.services.csv_file_service import csv_file_service


class ChatService:

    def __init__(self):

        settings = get_settings()

        self.llm = LLM(
            model=f"groq/{settings.groq_model_name}",
            api_key=settings.groq_api_key,
            temperature=0.1,
            max_completion_tokens=4096,
        )

    def _answer_growth_threshold(
        self,
        question: str,
        stock_symbol: str | None,
        datasets: list[dict]
    ):

        if "growth" not in question.lower():
            return None

        threshold_match = re.search(
            r"(?:greater\s+than|more\s+than|above|over|exceeds?|>)\s*(\d+(?:\.\d+)?)\s*%?",
            question.lower()
        )

        if not threshold_match:
            return None

        threshold = float(threshold_match.group(1))
        matches = {}
        source_files = set()

        for dataset in datasets:

            file_info = dataset["file"]
            frame = csv_file_service.read_file(
                file_info["full_path"],
                stock_symbol or ""
            )

            growth_column = next(
                (
                    column
                    for column in frame.columns
                    if "growth" in str(column).lower()
                ),
                None
            )

            if growth_column is None:
                continue

            growth_values = pd.to_numeric(
                frame[growth_column],
                errors="coerce"
            )
            qualifying_rows = frame[growth_values > threshold]

            for _, row in qualifying_rows.iterrows():

                ticker_column = next(
                    (
                        column
                        for column in frame.columns
                        if str(column).lower()
                        in ["symbol", "ticker", "stock", "stock_symbol"]
                    ),
                    None
                )
                company_column = next(
                    (
                        column
                        for column in frame.columns
                        if str(column).lower() in ["company", "company name"]
                    ),
                    None
                )
                ticker = (
                    str(row[ticker_column])
                    if ticker_column is not None
                    else str(row[company_column])
                    if company_column is not None
                    else str(row.name)
                )
                growth = float(row[growth_column])
                matches[(ticker, growth)] = {
                    "ticker": ticker,
                    "company": (
                        str(row[company_column])
                        if company_column is not None
                        else ""
                    ),
                    "growth": growth
                }
                source_files.add(file_info["file_name"])

        if not matches:
            return (
                f"No stocks with growth above {threshold:g}% were found "
                f"in the {len(datasets)} matching CSV file(s)."
            )

        result_lines = [
            f"Stocks with growth above {threshold:g}%:"
        ]

        for match in sorted(
            matches.values(),
            key=lambda item: item["growth"],
            reverse=True
        ):
            company = (
                f" ({match['company']})"
                if match["company"] and match["company"] != match["ticker"]
                else ""
            )
            result_lines.append(
                f"- {match['ticker']}{company}: {match['growth']:g}%"
            )

        result_lines.append(
            "Source CSVs: " + ", ".join(sorted(source_files))
        )

        return "\n".join(result_lines)

    def ask(
        self,
        question: str,
        stock_symbol: str | None = None
    ):

        datasets = (
            csv_file_service
            .get_relevant_data(
                stock_symbol or "",
                question
            )
        )

        growth_answer = self._answer_growth_threshold(
            question,
            stock_symbol,
            datasets
        )

        if growth_answer is not None:
            return growth_answer

        context = str(datasets[:5])

        prompt = f"""
You are an AI stock-data assistant.

This is an educational paper-trading system.

User question:
{question}

Stock:
{stock_symbol}

Local CSV data discovered:
{context}

Rules:

1. Use supplied data when available.
2. Never invent missing values.
3. Explain when data is unavailable.
4. Identify the source CSV file when possible.
5. If calculating values, explain the calculation.
6. Do not claim guaranteed returns.
7. Do not place orders.
"""

        result = self.llm.call(
            prompt
        )

        return str(result)


chat_service = ChatService()