# import time
# import random
# import json
# from typing import Dict
# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup


# def get_driver() -> uc.Chrome:
#     options = uc.ChromeOptions()
#     options.add_argument('--headless=new')  # Remove if you want to watch browser
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#     options.add_argument('--window-size=1920,1080')
#     options.add_argument('--disable-blink-features=AutomationControlled')
#     options.add_argument('--disable-gpu')
#     return uc.Chrome(options=options)


# def safe_get_text(element, default='') -> str:
#     try:
#         return element.text.strip() if element else default
#     except:
#         return default


# def scrape_agent_profile_selenium(url: str) -> Dict:
#     driver = get_driver()
#     try:
#         # Step through pages to mimic human behavior
#         pages = [
#             "https://www.realestate.com.au/",
#             "https://www.realestate.com.au/find-agent/adelaide---greater-region-sa",
#             "https://www.realestate.com.au/find-agent/adelaide---greater-region-sa?page=2",
#             url
#         ]
#         for page in pages:
#             driver.get(page)
#             print(f"Visiting: {page}")
#             print(driver.page_source)
#             time.sleep(random.uniform(3, 5))  # Mimic human delay

#         soup = BeautifulSoup(driver.page_source, 'html.parser')

#         div_first = soup.find('div', id='argonaut-wrapper')
#         if not div_first:
#             print("Could not find 'argonaut-wrapper'")
#             return {}

#         header_div = div_first.find('header', class_='styles__Header-sc-1ifcqm-0')
#         if not header_div:
#             print("Could not find 'header'")
#             return {}

#         profile_section = soup.find('div', class_='styles__Grid-sc-1ifcqm-1')
#         if not profile_section:
#             print("Could not find profile section")
#             return {}

#         photo_elem = profile_section.find('img', class_='Avatar__StyledImage-sc-1vvicio-0')
#         photo_url = photo_elem.get('src', '') if photo_elem else ''

#         name_elem = profile_section.find('h1', class_='Text__Typography-sc-1103tao-0')
#         full_name = safe_get_text(name_elem)
#         name_parts = full_name.split()
#         first_name = name_parts[0] if name_parts else ''
#         last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''

#         job_elem = profile_section.find('p', attrs={'data-testid': 'job-description'})
#         job_text = safe_get_text(job_elem)
#         job_title, company_name, company_url = '', '', ''

#         if job_text:
#             parts = job_text.split(' at ')
#             if len(parts) == 2:
#                 job_title = parts[0]
#                 company_link = profile_section.find('a', class_='LinkBase-sc-1ba0r3r-0')
#                 if company_link:
#                     company_name = safe_get_text(company_link)
#                     company_url = company_link.get('href', '')

#         experience_elem = profile_section.find('span', class_='Text__Typography-sc-1103tao-0')
#         experience = safe_get_text(experience_elem)

#         rating_elem = profile_section.find('p', class_='Text__Typography-sc-1103tao-0')
#         rating_text = safe_get_text(rating_elem)
#         rating = rating_text.split()[0] if rating_text else ''

#         reviews_elem = profile_section.find('a', class_='LinkBase-sc-1ba0r3r-0')
#         reviews_count = safe_get_text(reviews_elem).strip('()') if reviews_elem else ''

#         compliments = []
#         badges = profile_section.find_all('div', class_='styles__Badge-sc-1jpq4vo-0')
#         for badge in badges:
#             compliment = safe_get_text(badge.find('p', class_='Text__Typography-sc-1103tao-0'))
#             if compliment:
#                 compliments.append(compliment)

#         phone_elem = profile_section.find('a', href=lambda x: x and x.startswith('tel:'))
#         phone = phone_elem.get('href', '').replace('tel:', '') if phone_elem else ''

#         return {
#             'photo_url': photo_url,
#             'first_name': first_name,
#             'last_name': last_name,
#             'job_title': job_title,
#             'company_name': company_name,
#             'company_url': company_url,
#             'experience': experience,
#             'rating': rating,
#             'reviews_count': reviews_count,
#             'compliments': compliments,
#             'phone': phone
#         }

#     finally:
#         driver.quit()


# def main():
#     url = "https://www.realestate.com.au/agent/shaun-roberts-2066698"
#     print(f"\nStarting scrape for URL: {url}")
#     try:
#         data = scrape_agent_profile_selenium(url)
#         with open("agent_one.json", "w", encoding="utf-8") as f:
#             json.dump(data, f, indent=4, ensure_ascii=False)
#         print("Saved to agent_one.json")
#     except Exception as e:
#         print(f"Error in main: {str(e)}")


# if __name__ == "__main__":
#     main()


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import traceback

# Target agent profile URL
url = "https://www.realestate.com.au/agent/matthew-twelftree-1646603?cid=agent-profile-page%3Afind-agents%3Aresults-list%3Aagent-name"

# Setup Chrome options
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-US")
options.add_argument("--disable-logging")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.198 Safari/537.36")

driver = None
try:
    print("[*] Starting undetected Chrome...")
    driver = uc.Chrome(options=options)

    print("[*] Opening URL...")
    driver.get(url)

    # Give time for JS-heavy content to load
    print("[*] Waiting for main profile content...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-testid^='agent-profile']"))
    )

    # Scroll to bottom to load lazy content
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    # Capture debug screenshot
    driver.save_screenshot("agent_profile_debug.png")

    # Get page source
    html = driver.page_source
    print("[*] Successfully retrieved HTML")
    print(html[:3000])  # print partial HTML for console

except Exception as e:
    print("[!] ERROR OCCURRED:")
    traceback.print_exc()
    if driver:
        try:
            driver.save_screenshot("error_debug.png")
            print("[!] Saved error_debug.png for inspection.")
        except:
            pass

finally:
    if driver:
        print("[*] Closing browser...")
        try:
            driver.quit()
        except Exception as quit_err:
            print("[!] Error during driver quit:", quit_err)

