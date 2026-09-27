from pydantic import BaseModel

class ArtistSearchRequest(BaseModel):
    artist: str