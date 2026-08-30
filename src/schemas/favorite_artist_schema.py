from pydantic import BaseModel
from ..models.favorite_artist import FavoriteArtist

class FavoriteArtistCreateRequest(BaseModel):
    id_user: int
    id_artist: str

class FavoriteArtistDeleteRequest(BaseModel):
    id_user: int
    id_artist: str

class FavoriteArtistResponse(BaseModel):
    id_artist: str

class FavoriteArtistListResponse(BaseModel):
    favorite_artists: list[FavoriteArtistResponse]

def favorite_artist_to_response(favorite_artist: FavoriteArtist):
    return {
        "id_artist": favorite_artist.id_artist
    }

def favorite_artists_to_list_response(favorite_artists: list[FavoriteArtist]):
    return {
        "favorite_artists": [favorite_artist_to_response(favorite_artist) for favorite_artist in favorite_artists]
    }