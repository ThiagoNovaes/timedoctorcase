import json
import requests
import os
import imdb

# Function to download the banner image
def download_banner(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    print("Banner downloaded successfully!")

def url_clean(url):
    base, ext = os.path.splitext(url)
    i = url.count('@')
    s2 = url.split('@')[0]
    url = s2 + '@' * i + ext
    return url

# Read JSON file
with open('netflix.json') as file:
    data = json.load(file)

# Check if any movies are available in the viewedItems
if 'viewedItems' in data and len(data['viewedItems']) > 0:
    # Iterate through each movie in viewedItems
    for movie in data['viewedItems']:
        # Check if the movie has a title or seriesTitle
        if 'title' in movie:
            movie_name = movie['title']
        if 'seriesTitle' in movie:
            movie_name = movie['seriesTitle']

        print(f"Movie name: {movie_name}")

        # Create an instance of the IMDb class
        ia = imdb.IMDb()

        # Search for the movie based on its name
        movies = ia.search_movie(movie_name)

        # Check if any movie matches the search
        if len(movies) > 0:
            # Get the first movie from the search results
            found_movie = movies[0]
            ia.update(found_movie)

            # Check if the movie has a banner URL
            if 'cover url' in found_movie.keys():
                banner_url = url_clean(found_movie['cover url'])
                print(banner_url)
                file_name = f"netflixcover/{movie['topNodeId']}.jpg"

                # Download the banner image
                download_banner(banner_url, file_name)
            else:
                print("No banner available for this movie.")
        else:
            print("Movie not found.")
else:
    print("No movies found in the JSON data.")