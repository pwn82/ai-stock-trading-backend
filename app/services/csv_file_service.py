import fnmatch
import os
import json
from pathlib import Path
from datetime import datetime

import pandas as pd

from app.core.config import get_settings


SKIP_DIRECTORIES = {
    "$Recycle.Bin",
    "System Volume Information",
    "Windows",
    "Program Files",
    "Program Files (x86)",
    "ProgramData",
    "AppData",
    "node_modules",
    ".git",
    ".venv",
    "__pycache__"
}


class CsvFileService:

    def __init__(self):

        self.settings = get_settings()

        self.files = []

    def scan_files(self):

        discovered = []

        pattern = self.settings.csv_file_pattern

        for root in self.settings.get_scan_roots():

            root_path = Path(root)

            if not root_path.exists():

                continue

            for current_root, directories, files in os.walk(
                root_path,
                topdown=True,
                onerror=lambda _: None
            ):

                directories[:] = [
                    d for d in directories
                    if d not in SKIP_DIRECTORIES
                ]

                for file_name in files:

                    if not fnmatch.fnmatch(
                        file_name.lower(),
                        pattern.lower()
                    ):
                        continue

                    full_path = Path(
                        current_root
                    ) / file_name

                    try:

                        stat = full_path.stat()

                        size_mb = (
                            stat.st_size /
                            (1024 * 1024)
                        )

                        if size_mb > self.settings.max_file_size_mb:
                            continue

                        columns = []

                        try:

                            df = pd.read_csv(
                                full_path,
                                nrows=5
                            )

                            columns = [
                                str(c)
                                for c in df.columns
                            ]

                        except Exception:
                            pass

                        discovered.append({
                            "file_name": file_name,
                            "full_path": str(full_path),
                            "size_mb": round(size_mb, 2),
                            "modified_time":
                                datetime.fromtimestamp(
                                    stat.st_mtime
                                ).isoformat(),
                            "columns": columns
                        })

                    except Exception:
                        continue

        self.files = discovered

        return discovered

    def get_files(self):

        return self.files

    def search_files(
        self,
        stock_symbol: str,
        question: str = ""
    ):

        if not self.files:

            self.scan_files()

        symbol = stock_symbol.lower()

        question_words = [
            x.lower()
            for x in question.split()
            if len(x) > 2
        ]

        scored = []

        for file in self.files:

            score = 0

            file_name = file["file_name"].lower()
            path = file["full_path"].lower()
            columns = " ".join(
                file.get("columns", [])
            ).lower()

            if symbol and symbol in file_name:
                score += 100

            if symbol and symbol in path:
                score += 50

            if symbol and symbol in columns:
                score += 30

            for word in question_words:

                if word in file_name:
                    score += 10

                if word in columns:
                    score += 5

            if score > 0:

                scored.append(
                    (score, file)
                )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        if not symbol and not scored:
            return self.files[:10]

        return [
            item[1]
            for item in scored[:10]
        ]

    def read_file(
        self,
        file_path: str,
        stock_symbol: str = ""
    ):

        allowed = any(
            str(file_path).lower().startswith(
                str(root).lower()
            )
            for root in self.settings.get_scan_roots()
        )

        if not allowed:

            raise PermissionError(
                "File is outside configured CSV scan roots."
            )

        df = pd.read_csv(
            file_path
        )

        if stock_symbol:

            symbol_columns = [
                c for c in df.columns
                if str(c).lower()
                in [
                    "symbol",
                    "ticker",
                    "stock",
                    "stock_symbol"
                ]
            ]

            if symbol_columns:

                column = symbol_columns[0]

                filtered = df[
                    df[column]
                    .astype(str)
                    .str.upper()
                    == stock_symbol.upper()
                ]

                if not filtered.empty:
                    df = filtered

        df = df.tail(
            self.settings.max_csv_rows
        )

        return df

    def get_relevant_data(
        self,
        stock_symbol: str,
        question: str = ""
    ):

        files = self.search_files(
            stock_symbol,
            question
        )

        datasets = []

        for file in files:

            try:

                df = self.read_file(
                    file["full_path"],
                    stock_symbol
                )

                if df.empty:
                    continue

                datasets.append({
                    "file": file,
                    "rows": len(df),
                    "columns": [
                        str(c)
                        for c in df.columns
                    ],
                    "data": df.tail(100).to_dict(
                        orient="records"
                    )
                })

            except Exception:
                continue

        return datasets


csv_file_service = CsvFileService()