import openpyxl
from bs4 import BeautifulSoup

# Read HTML from file
with open('amazon_prime.html', 'r') as file:
    html = file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find all list items with class "RdNoU_"
list_items = soup.find_all('li', class_='RdNoU_')

# Create a new Excel workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Iterate over list items
for item in list_items:
    # Find the date
    date = item.find('div').text.strip()

    # Find all movies watched on the current date
    movies = item.find_all('a', class_='_1NNx6V')

    # Write the date and movies to the Excel sheet
    sheet.append([date, 'Movies Watched:'])
    for movie in movies:
        sheet.append(['', movie.text])

# Save the Excel workbook
workbook.save('movies_watched.xlsx')