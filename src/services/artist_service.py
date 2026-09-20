def list_artists(data_json):
    artists = []
    for artist in data_json['results']['artistmatches']['artist']:
        if artist['mbid'] != '':
            artists.append({
                'name': artist['name'], 
                'mbid': artist['mbid'],
                'listeners': artist['listeners']})
    return artists