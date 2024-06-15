import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://directory.goodonyou.eco/brand/zara"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the element with the specified class
    ratings_container = soup.find(class_='id__ContainerRatings-sc-12z6g46-8 OUiGD')
    
    if ratings_container:
        # Extract the text
        ratings_text = ratings_container.get_text()
        
        # Split the text into the required segments
        segments = [
            ratings_text[0:6],
            ratings_text[6:16],
            ratings_text[16:22],
            ratings_text[22:32],
            ratings_text[32:39],
            ratings_text[39:]
        ]
        
        # Print each segment on a new line
        for segment in segments:
            print(segment)
    else:
        print("Ratings container not found.")
else:
    print("Failed to retrieve the webpage.")
