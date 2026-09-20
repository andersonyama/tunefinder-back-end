def list_recommendation(data_json):
    artists = []
    for artist in data_json.get('similarartists', {}).get('artist', []):
        name = artist.get('name')
        mbid = artist.get('mbid')
        match_value = artist.get('match')
        
        if not name or not mbid:
            continue

        artists.append({
            'name': name, 
            'mbid': mbid,
            'match': match_value
            })
    return artists