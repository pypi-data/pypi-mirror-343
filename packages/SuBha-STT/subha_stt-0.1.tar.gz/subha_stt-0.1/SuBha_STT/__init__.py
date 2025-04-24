# pip install selenium webdriver-manager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Allow media access (microphone)
chrome_options.add_argument("--headless=new")  # Run headless browser (no UI)

# Initialize the driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Path to the local file you want to test (ensure you have the local HTML page or serve via Flask)
website = "data:text/html,<html><head><meta charset='UTF-8'><title>SpeechToText</title></head><body><h1>SpeechToText</h1><button id='startButton'>Start Listening</button><div id='output'></div><script>const output=document.getElementById('output');const startButton=document.getElementById('startButton');let finalTranscript='';const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;const recognition=new SpeechRecognition();recognition.lang='en-US';recognition.interimResults=true;startButton.addEventListener('click',()=>{finalTranscript='';output.textContent='';recognition.start();startButton.textContent='Listening...';});recognition.addEventListener('result',(e)=>{const transcript=Array.from(e.results).map(result=>result[0].transcript).join('');if(e.results[0].isFinal){finalTranscript=transcript;output.textContent=finalTranscript;}});recognition.addEventListener('end',()=>{startButton.textContent='Start Listening';recognition.start();});document.addEventListener('keydown',(e)=>{if(e.key==='Escape'){recognition.stop();startButton.textContent='Start Listening';}});</script></body></html>"

driver.get(website)

# File path to save speech-to-text output
rec_file = os.path.join(os.getcwd(), "input.text")

def listen():
    try:
        # Wait until the "Start Listening" button is available, then click it
        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")

        output_text = ""
        is_second_click = False

        # Loop to listen for the output text change
        while True:
            # Wait for the output text to appear
            output_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()

            # Handle the second click scenario
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "Listening..." in start_button.text:
                is_second_click = True

            # If the output text has changed, update the file
            if current_text != output_text:
                output_text = current_text
                with open(rec_file, "w") as file:
                    file.write(output_text.lower())  # Write output in lowercase
                print("USER: " + output_text)

            # Optional: Sleep to avoid overloading with too many checks
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e)
    finally:
        # Quit the driver once done
        driver.quit()

# Start listening for speech-to-text
listen()
