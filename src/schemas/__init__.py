from error_schema import ErrorResponse
from .user_schema import UserCreateRequest, UserDeleteRequest, UserUpdateRequest
from .favorite_artist_schema import FavoriteArtistCreateRequest, FavoriteArtistDeleteRequest, \
                                    FavoriteArtistResponse, FavoriteArtistListResponse, \
                                    favorite_artist_to_response, favorite_artists_to_list_response