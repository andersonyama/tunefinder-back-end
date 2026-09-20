def list_artists(data_json):
    artists = []
    for artist in data_json.get('results', {}).get('artistmatches', {}).get('artist', []):
            name = artist.get('name')
            mbid = artist.get('mbid')
            listeners = artist.get('listeners')
            
            if not name or not mbid:
                continue
    
            artists.append({
                'name': name, 
                'mbid': mbid,
                'match': listeners
                })
    return artists