import os
from time import sleep

import discord
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

screenshots_dir = "Screenshots"
intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def scan_for_items(channel_id):
    # Initialize Selenium WebDriver (Firefox)
    driver = webdriver.Firefox()

    try:
        # Navigate to the website
        driver.get("https://en.gamigo.com/fiesta/en/itemshop")

        # Perform web scraping to find items on sale or permanent items
        # Locate and interact with the search box
        search_input = driver.find_element(By.CSS_SELECTOR, "input[name='search']")
        search_input.send_keys("(Permanent)")

        search_button = driver.find_element(By.CSS_SELECTOR, ".fa.fa-search")
        search_button.click()

        # Wait for the search results to load (you may need to adjust the wait time)
        driver.implicitly_wait(10)

        # Fetch the selectors for each item on the page
        item_elements = driver.find_elements(By.CLASS_NAME, "resultlink")

        # Extract and capture a screenshot for each item
        for idx, item_element in enumerate(item_elements, start=1):
            if not os.path.exists(screenshots_dir):
                os.makedirs(screenshots_dir)

            # Determine the next screenshot filename
            screenshot_path = os.path.join(screenshots_dir, f"item_{idx}.png")

            # Click on the item element to open it in a new tab
            item_element.send_keys(Keys.CONTROL + Keys.RETURN)

            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            sleep(1)

            element_to_capture = driver.find_element(By.CLASS_NAME, "content")
            element_to_capture.screenshot(screenshot_path)

            # Close the current tab and switch back to the previous one
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])

            await upload_single_screenshot(screenshot_path, channel_id)

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()

    finally:
        driver.quit()
        # Clean up: Delete all screenshots from the Screenshots folder
        cleanup_screenshots()


async def upload_single_screenshot(screenshot_path, channel_id):
    # Upload and post a single screenshot to the specified channel
    channel = client.get_channel(channel_id)
    if channel:
        file = discord.File(screenshot_path)
        await channel.send(file=file)


def cleanup_screenshots():
    # Delete all screenshots from the Screenshots folder
    for filename in os.listdir(screenshots_dir):
        file_path = os.path.join(screenshots_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"An error occurred while deleting {file_path}: {e}")