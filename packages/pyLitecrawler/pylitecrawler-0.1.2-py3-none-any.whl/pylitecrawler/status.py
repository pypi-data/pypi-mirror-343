import httpx
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

async def check_url_status(url: str):
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            response = await client.get(url, headers=HEADERS)
            status_ok = 200 <= response.status_code < 400
            return JSONResponse(content={"url": url, "status": status_ok, "status_code": response.status_code})
    except Exception as e:
        return JSONResponse(content={"url": url, "status": False, "error": str(e)})
# Path added to change the default location of the ChromeDriver executable
def check_js_rendered(url: str, wait_time: int = 10,path: str = "D:\\Programs\\chrome\\chromedriver.exe"):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(path)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        WebDriverWait(driver, wait_time).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#navGrp"), "About")
        )

        driver.quit()
        return JSONResponse(content={"url": url, "javascript_rendered": True})
    except Exception as e:
        return JSONResponse(content={"url": url, "javascript_rendered": False, "error": str(e)})
