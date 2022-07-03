import time
import json
from tempfile import mkdtemp
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

## need to add Selenium code
def lambda_handler(event, context):
    
    ## Setup chrome options
    chrome_options = Options()
    chrome_options.binary_location = '/opt/chrome/chrome'
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-first-run')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-client-side-phishing-detection')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-port=9222")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service("/opt/chromedriver")

    # Choose Chrome Browser
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)

    # Get page
    browser.get("https://www.sportsbet.com.au/racing-schedule/today")

    # Extract description from page and print
    trackElements = browser.find_elements(By.XPATH, "//td[contains(@data-automation-id,'horse-racing-section-row') and contains(@class, 'meetingCell')]")
    numOfTracks = len(trackElements)

    tracks = []

    ## Loop through trackElements, selectTrackName and add to tracks array
    for track in trackElements:
        pattern = f"//span[contains(@data-automation-id,'horse-racing-section-row-{trackElements.index(track)+1}-meeting-name')]"
        trackName = browser.find_element(By.XPATH, pattern)

        racePattern =  f"//td[contains(@data-automation-id,'horse-racing-section-row-{trackElements.index(track)+1}-col-')]"
        raceElements = browser.find_elements(By.XPATH, racePattern)
        #print(trackName.text)
        numOfRaces = len(raceElements)
        
        tracks.append({'track':trackName.text, 'races':numOfRaces})

    #print(tracks)
    #jsonOut = json.dumps(tracks)
    #print(jsonOut)

    #Wait for 10 seconds
    time.sleep(1)
    browser.quit()

    return {
        "statusCode": 201,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(tracks)
    }
