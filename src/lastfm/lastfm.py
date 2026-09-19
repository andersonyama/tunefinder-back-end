import requests

from ..config import LASTFM_API_URL

import os
import logging
import requests
from requests.adapters import HTTPAdapter, Retry

logger = logging.getLogger(__name__)


class LastFmApiError(Exception):
    """Base exception for Last.fm API failures."""


class LastFmClient:
    def __init__(self, api_key: str, base_url: str = LASTFM_API_URL):
        self.api_key = api_key
        self.base_url = base_url

        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        self.session.mount("https://", HTTPAdapter(max_retries=retries))

    def _get(self, params: dict, timeout: float = 5.0) -> dict:
        params = {**params, "api_key": self.api_key, "format": "json"}
        try:
            response = self.session.get(self.base_url, params=params, timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout as e:
            raise LastFmApiError("Request timed out") from e
        except requests.exceptions.HTTPError as e:
            raise LastFmApiError(f"HTTP error: {e}") from e
        except requests.exceptions.RequestException as e:
            raise LastFmApiError(f"Request failed: {e}") from e

        try:
            data = response.json()
        except ValueError as e:
            raise LastFmApiError("Invalid JSON in response") from e

        if "error" in data:
            raise LastFmApiError(f"API error {data['error']}: {data.get('message')}")

        return data

    def artist_search(self, artist: str) -> dict:
        return self._get({"method": "artist.search", "artist": artist})

    def artist_similar(self, artist_mbid: str) -> dict:
        return self._get({"method": "artist.getsimilar", "mbid": artist_mbid})