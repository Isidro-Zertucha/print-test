from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Dict
import time

def get_remote_driver() -> WebDriver:
    """Connect to the Selenium standalone container"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Remote(
        command_executor='http://recruiter-dev-selenium:4444/wd/hub',
        options=chrome_options
    )
    return driver

def fetch_realtime_headlines() -> List[Dict[str, str | int]]:
    """Fetch fresh HN stories using Selenium container"""
    driver = None
    all_stories = []
    
    try:
        driver = get_remote_driver()
        
        for page in range(1, 6):  # First 5 pages
            url = f"https://news.ycombinator.com/news?p={page}" if page > 1 else "https://news.ycombinator.com"
            
            driver.get(url)
            time.sleep(2)  # Wait for page load
            
            stories = driver.find_elements(By.CSS_SELECTOR, "tr.athing")
            for story in stories:
                try:
                    title_elem = story.find_element(By.CSS_SELECTOR, ".titleline a")
                    score_elem = story.find_element(By.XPATH, "./following-sibling::tr//span[@class='score']")
                    
                    all_stories.append({
                        "title": title_elem.text,
                        "url": title_elem.get_attribute("href"),
                        "score": int(score_elem.text.split()[0]) if score_elem else 0,
                        "page": page
                    })
                except Exception:
                    continue
            
            time.sleep(1.5)  # Be polite to HN servers
            
    except Exception as e:
        print(f"Error during scraping: {str(e)}")
        raise
    finally:
        if driver:
            driver.quit()
    
    # Return top 30 stories by score
    return sorted(all_stories, key=lambda x: x['score'], reverse=True)[:30]