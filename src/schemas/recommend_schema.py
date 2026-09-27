from pydantic import BaseModel
from ..models.favorite_artist import FavoriteArtist

class RecommendRequest(BaseModel):
    artist_ids: list[str]

class RecommendResponse(BaseModel):
    id_artist: str
    artist_name: str

class RecommendListResponse(BaseModel):
    favorite_artists: list[RecommendResponse]