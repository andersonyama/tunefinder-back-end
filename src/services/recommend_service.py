import logging
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from dataclasses import dataclass

from ..clients.lastfm_client import lastfm_client

logger = logging.getLogger(__name__)

def list_recommendation(data_json):
    artists = []
    for artist in data_json.get('similarartists', {}).get('artist', []):
        name = artist.get('name')
        mbid = artist.get('mbid')
        match_value = float(artist.get('match'))
        
        if not name or not mbid:
            continue

        artists.append({
            'name': name, 
            'mbid': mbid,
            'match': match_value
            })
    return artists

class AllRequestsFailed(Exception):
    """Every request to the external service failed, so no score can be computed."""

@dataclass(frozen=True)
class Suggestion:
    mbid: str
    name: str
    score: float  # average match score across the input artists whose requests succeeded
    matches: dict[str, float] # input MBID -> raw score 

@dataclass(frozen=True)
class SuggestionResult:
    suggestions: list[Suggestion]
    failed: list[str]  # input MBIDs whose request failed (excluded from the average)

def suggest_artists(
    artists: list[str],
    min_score: float = 0.0,
    limit: int | None = None,
    max_workers: int = 8,
) -> SuggestionResult:
    # Deduplicate input, preserving order
    inputs = list(dict.fromkeys(a.strip().lower() for a in artists))
    if not inputs:
        return SuggestionResult([], [])
    input_set = set(inputs)
 
    def try_fetch(mbid: str) -> dict[str, float] | None:
        try:
            return dict(lastfm_client.artist_similar(mbid))
            # return dict(test_result)
        except Exception:  # narrow this to your client's exception types
            logger.warning("Similarity request failed for %s", mbid, exc_info=True)
            return None
 
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        responses = list(pool.map(try_fetch, inputs))
 
    succeeded = [(m, list_recommendation(r)) for m, r in zip(inputs, responses) if r is not None]
    failed = [m for m, r in zip(inputs, responses) if r is None]
    if not succeeded:
        raise AllRequestsFailed(f"All {len(inputs)} similarity requests failed")
 
    totals: dict[str, float] = defaultdict(float)
    names: dict[str, str] = {}
    matches: dict[str, dict[str, float]] = defaultdict(dict)
 
    for source, similarArtists in succeeded:
        # Collapse duplicates within one response (keep the best score)
        best: dict[str, float] = {}
        for similarArtist in similarArtists:
            mbid = similarArtist['mbid'].strip().lower()
            if mbid in input_set:  # disconsiders artists from the input
                continue
            names.setdefault(mbid, similarArtist['name'])
            best[mbid] = max(best.get(mbid, 0.0), similarArtist['match'])
 
        for mbid, score in best.items():
            totals[mbid] += score
            matches[mbid][source] = score
 
    # divide by successful requests only.
    n = len(succeeded)
    results = [Suggestion(m, names[m], t / n, matches[m]) for m, t in totals.items()]
 
    results = [s for s in results if s.score >= min_score]
    results.sort(key=lambda s: (-s.score, s.mbid))
    return SuggestionResult(results[:limit] if limit else results, failed)