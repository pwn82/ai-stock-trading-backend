import os
import requests

from app.core.config import get_settings


class NewsService:

    def __init__(self):

        self.settings = get_settings()

    def search_news(
        self,
        stock_symbol: str
    ):

        api_key = self.settings.serper_api_key

        if not api_key:

            return {
                "enabled": False,
                "articles": []
            }

        url = "https://google.serper.dev/news"

        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "q": f"{stock_symbol} stock news"
        }

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            articles = data.get(
                "news",
                []
            )[:10]

            return {
                "enabled": True,
                "articles": articles
            }

        except Exception as exc:

            return {
                "enabled": False,
                "articles": [],
                "error": str(exc)
            }


news_service = NewsService()