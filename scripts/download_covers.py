import pandas as pd
import aiohttp
import asyncio
import os
from PIL import Image, ImageOps, ImageDraw
from concurrent.futures import ThreadPoolExecutor

# Function to download an image from a given URL
async def download_image(session, url, filename):
    async with session.get(url) as response:
        if response.status == 200:
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            return True
        else:
            print(f"Failed to download: {filename}")
            return False

# Function to convert an image into a circular image with transparent background using CPU
def convert_to_circle(image):
    size = min(image.size)
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, *image.size), fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(image, mask=mask)
    result = result.resize((size, size), Image.ANTIALIAS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    result.putalpha(mask)
    return result

# Specify the path to the Excel file and the column names containing the URLs
excel_file = "tracks_with_streaming_info.xlsx"
album_cover_column = "Album Cover URL"
artist_photo_column = "Artist Photo URL"

# Read the Excel file
df = pd.read_excel(excel_file)

# Create a directory to save the downloaded images
output_directory = "covers"
os.makedirs(output_directory, exist_ok=True)

# Create an event loop and a session for asynchronous requests
loop = asyncio.get_event_loop()
session = aiohttp.ClientSession(loop=loop)

# Define the async function to handle the download and conversion process
async def download_and_convert_images():
    tasks = []
    for _, row in df.iterrows():
        for column in [album_cover_column, artist_photo_column]:
            image_url = row[column]
            image_id = image_url.split("/")[-1]  # Extract the ID from the URL
            image_filename = os.path.join(output_directory, f"{image_id}.png")
            task_download = asyncio.ensure_future(download_image(session, image_url, image_filename))
            tasks.append(task_download)

    # Wait for all download tasks to complete
    await asyncio.gather(*tasks)

    # Close the session
    await session.close()

    # Convert the downloaded images to circular images with transparent background
    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(output_directory):
            if filename.endswith(".png"):
                image_path = os.path.join(output_directory, filename)
                future = executor.submit(convert_to_circle, Image.open(image_path))
                futures.append((filename, future))

        # Save the converted images
        for filename, future in futures:
            image = future.result()
            image.save(os.path.join(output_directory, filename), format="PNG")

# Run the async download and conversion function
loop.run_until_complete(download_and_convert_images())
