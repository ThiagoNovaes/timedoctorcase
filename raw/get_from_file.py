import json
import pandas as pd
import requests

# Read the JSON file with track streaming history
with open('StreamingHistory0.json') as file:
    streaming_history = json.load(file)

# Read the JSON file with track information
with open('YourLibrary.json') as file:
    data = json.load(file)

# Access the tracks and streaming history
tracks = data['tracks']

# Create a dictionary to store track streaming information
streaming_info = {}
for item in streaming_history:
    artist = item['artistName']
    track_name = item['trackName']
    ms_played = item['msPlayed']
    end_time = pd.to_datetime(item['endTime']).tz_localize(None)  # Remove timezone information

    # Update streaming information for the track
    if (artist, track_name) not in streaming_info:
        streaming_info[(artist, track_name)] = {
            'times_played': 1,
            'total_time_played_ms': ms_played,
            'last_played': end_time
        }
    else:
        streaming_info[(artist, track_name)]['times_played'] += 1
        streaming_info[(artist, track_name)]['total_time_played_ms'] += ms_played
        if end_time > streaming_info[(artist, track_name)]['last_played']:
            streaming_info[(artist, track_name)]['last_played'] = end_time

# Create a list to store the track information
track_info = []

# Set the maximum number of track URIs per request
max_uris_per_request = 50

# Set the Spotify access token
access_token = 'BQAfFAVw_2iVkX5YA_QdpZaGLKhWlnwG4or9y7E8ZFKHETw3w3cW-XKmorY0Bf6RGPAfjk28cZLSYp2BQm7PRpXNRWBfxhAjKtYObcEq7WrgzB8ZfJWZuNj_27p_I9666e-51d9u50GJgFqamZIT7oAyZiXTMSy3Ky8sNlv-UmzIEEIrE5x1PbA75Yj6qODrUAvCxYb1WkM'

# Iterate over the tracks in batches
for i in range(0, len(tracks), max_uris_per_request):
    # Get a batch of tracks
    track_batch = tracks[i:i + max_uris_per_request]

    # Create a comma-separated string of track URIs
    track_uris = [track['uri'] for track in track_batch]

    # Make a GET request to Spotify API for the current batch of tracks
    headers = {
        'authorization': f'Bearer {access_token}'
    }
    url = 'https://api.spotify.com/v1/tracks'
    params = {
        'ids': ','.join([uri.split(':')[2] for uri in track_uris])
    }
    response = requests.get(url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        tracks_data = response.json()['tracks']

        # Iterate over each track data in the current batch
        for track, track_data in zip(track_batch, tracks_data):
            artist = track['artist']
            album = track['album']
            track_name = track['track']
            uri = track['uri']
            popularity = track_data['popularity']
            duration_ms = track_data['duration_ms']
            explicit = track_data['explicit']

            # Get the streaming information for the track
            streaming_data = streaming_info.get((artist, track_name), {})

            # Calculate total time played in minutes
            total_time_played_min = streaming_data.get('total_time_played_ms', 0) / (1000 * 60)

            # Get the last played timestamp
            last_played = streaming_data.get('last_played', None)

            # Get the URL to the album cover
            album_cover_images = track_data['album'].get('images', [])
            if len(album_cover_images) > 0:
                album_cover_url = album_cover_images[0]['url']
            else:
                album_cover_url = 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'

            # Get the artist ID
            artist_id = track_data['album']['artists'][0]['id']

            # Make a GET request to Spotify API to get artist information
            url = f'https://api.spotify.com/v1/artists/{artist_id}'
            response = requests.get(url, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                artist_data = response.json()

                # Get the artist genres
                genres = artist_data.get('genres', [])

                # Get the artist photo
                artist_photo_images = artist_data.get('images', [])
                if len(artist_photo_images) > 0:
                    artist_photo_url = artist_photo_images[0]['url']
                else:
                    artist_photo_url = 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'
            else:
                genres = []
                artist_photo_url = 'https://i.scdn.co/image/ab67616d00001e02ff9ca10b55ce82ae553c8228'

            # Estimate the times played for tracks with no streaming history
            if not streaming_data:
                times_played = int(popularity / 10) + 1
                total_time_played_min = times_played * (duration_ms / (1000 * 60))
                last_played = None
            else:
                times_played = streaming_data.get('times_played', 0)

            # Append track information to the list
            track_info.append([artist, album, track_name, uri, popularity, duration_ms, explicit,
                               times_played, total_time_played_min, last_played, genres,
                               album_cover_url, artist_photo_url])
    else:
        print(f"Error retrieving track data from Spotify API for batch {i + 1}-{i + max_uris_per_request}")


# Create a DataFrame from the track information
df = pd.DataFrame(track_info, columns=['Artist', 'Album', 'Track', 'URI', 'Popularity', 'Duration (ms)',
                                       'Explicit', 'Times Played', 'Total Time Played (min)', 'Last Played',
                                       'Genres', 'Album Cover URL', 'Artist Photo URL'])

# Write the DataFrame to an Excel file
df.to_excel('tracks_with_streaming_info.xlsx', index=False)
