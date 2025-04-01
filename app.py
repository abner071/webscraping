import csv
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    try:
        url = "https://www.nytimes.com/international/section/us"

        driver = webdriver.Chrome(options=get_chrome_options())
        driver.get(url)

        total_pages = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#stream-panel > div > div > span > strong:nth-of-type(2)")
        )).get_attribute("innerText")

        button_last_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"#stream-panel a[aria-label='Go to page {total_pages}']")
        ))
        driver.execute_script("arguments[0].click();", button_last_page)

        news_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#stream-panel > div > ol")
        ))
        news_list_items = WebDriverWait(news_list, 10).until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, 'li')
        ))

        posts = []
        for item in news_list_items:
            post_title = item.find_element(By.CSS_SELECTOR, 'a > h3').get_attribute("innerText")
            post_date = item.find_element(By.CSS_SELECTOR, "span[data-testid='todays-date']").get_attribute("innerText")
            post_paragraphs = item.find_elements(By.CSS_SELECTOR, 'article > p')
            post_content = post_paragraphs[0].get_attribute("innerText") if len(post_paragraphs) > 0 else ''
            post_owner = post_paragraphs[1].get_attribute("innerText") if len(post_paragraphs) > 1 else ''

            posts.append({
                'title': clean_text(post_title),
                'content': clean_text(post_content),
                'owner': clean_text(post_owner),
                'date': clean_text(post_date)
            })

        driver.quit()

        if len(posts) > 0:
            return generate_csv(posts)

    except Exception as e:
        print(f"Falha na coleta de posts: {e} - {traceback.format_exc()}")

    return False


def get_chrome_options() -> Options:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--remote-debugging-port=9222")

    return chrome_options


def clean_text(text):
    replacements = {
        "‘": "'", "’": "'",
        "“": '"', "”": '"',
        "–": "-", "—": "-",
        "…": "..."
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def generate_csv(posts: list) -> None:
    try:
        with open('./posts.csv', 'w') as csvfile:
            csv.writer(csvfile, delimiter=',')
            csv.writer(csvfile, delimiter=',').writerow(posts[0].keys())

            for post in posts:
                csv.writer(csvfile, delimiter=',').writerow(post.values())

        print(f"Arquivo CSV gerado com sucesso!")
        return True

    except Exception as e:
        print(f"Falha ao gerar arquivo CSV: {e} - {traceback.format_exc()}")

    return False


if __name__ == "__main__":
    main()
