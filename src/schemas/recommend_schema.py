from pydantic import BaseModel
from ..models.favorite_artist import FavoriteArtist

class RecommendRequest(BaseModel):
    id_artist: str

class RecommendResponse(BaseModel):
    id_artist: str

class RecommendListResponse(BaseModel):
    favorite_artists: list[RecommendResponse]