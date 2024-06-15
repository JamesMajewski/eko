from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import concurrent.futures

app = Flask(__name__)

# Initialize the Selenium WebDriver once per session
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)

def fetch_marka_value(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        marka_span = soup.find('span', string='Marka:')
        if marka_span:
            marka_value = marka_span.find_next_sibling(string=True).strip()
            return marka_value
        else:
            return "Marka: element not found"
    except Exception as e:
        print(f"Error fetching marka value: {e}")
        return str(e)

def fetch_good_on_you_data(brand_name):
    try:
        brand_name = brand_name.lower().replace(" ", "-")
        url = f"https://directory.goodonyou.eco/brand/{brand_name}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            ratings_container = soup.find(class_='id__ContainerRatings-sc-12z6g46-8 OUiGD')
            if ratings_container:
                ratings_text = ratings_container.get_text()
                segments = [
                    ratings_text[0:6],
                    ratings_text[6:16],
                    ratings_text[16:22],
                    ratings_text[22:32],
                    ratings_text[32:39],
                    ratings_text[39:]
                ]
                return segments
            else:
                return ["Ratings container not found."]
        else:
            print(f"Failed to retrieve the webpage, status code: {response.status_code}")
            return [f"Failed to retrieve the webpage. Status code: {response.status_code}"]
    except Exception as e:
        print(f"Error fetching Good On You data: {e}")
        return [f"Error: {e}"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-all-data')
def fetch_all_data():
    url = request.args.get('url')
    if url:
        marka_value = fetch_marka_value(url)
        if marka_value and not marka_value.startswith("Error"):
            segments = fetch_good_on_you_data(marka_value)
            return jsonify(marka_value=marka_value, segments=segments)
    return jsonify(marka_value="Invalid URL", segments=[])

if __name__ == '__main__':
    try:
        app.run(debug=True, port=5001)
    finally:
        driver.quit()  # Ensure the driver is quit when the Flask app shuts down
