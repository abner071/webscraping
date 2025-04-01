import argparse
import csv
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main(**kwargs):
    """
    Esse script realiza um webscraping no site do New York Times buscando os posts relacionados aos Estados Unidos.
    Salva os posts coletados em um arquivo CSV com as colunas separadas por vírgula.
    
    Args:
        initial-page (int): Página inicial em que começará a busca por posts.
        last-page (int): Página final em que terminará a busca por posts.
        all-pages (bool): Define se buscará todas as páginas. Esse parametro sobescreve o last-page.
    
    Returns:
        bool: Retorna um booleano informando se criou o arquivo csv com sucesso ou não.
    """

    try:
        print(f"Buscando com parametros: {kwargs}")

        url = "https://www.nytimes.com/international/section/us"

        driver = webdriver.Chrome(options=get_chrome_options())
        driver.get(url)

        if kwargs['all_pages'] or kwargs['last_page']:
            total_pages = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#stream-panel > div > div > span > strong:nth-of-type(2)")
            )).get_attribute("innerText")

            if int(kwargs['last_page']) > 0:
                target_page = kwargs['last_page']
                
            if int(kwargs['last_page']) > int(total_pages):
                target_page = total_pages
                print(f"Página {kwargs['last_page']} não existe, buscando até a página {total_pages}")

            if kwargs['all_pages']:
                target_page = total_pages
        
            button_last_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"#stream-panel a[aria-label='Go to page {target_page}']")
            ))
            driver.execute_script("arguments[0].click();", button_last_page)

        initial_page_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"#stream-panel  div#page-{kwargs['initial_page']}")
        ))

        news_list_items = WebDriverWait(initial_page_element, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, 'following-sibling::li')
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
    parser = argparse.ArgumentParser(description="Webscraping com Selenium")
    parser.add_argument("--initial-page", type=int, default=1, help="Página inicial em que começará a busca")
    parser.add_argument("--last-page", type=int, default=0, help="Página final em que terminará a busca")
    parser.add_argument("--all-pages", action="store_true", help="Define se buscará todas as páginas")

    args = vars(parser.parse_args())
    main(**args)
