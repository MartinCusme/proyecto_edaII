import time
from playwright.sync_api import sync_playwright
from TikTokApi import TikTokApi
import asyncio
import os

def obtener_mstoken():
    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        try:
            page.goto(url="https://www.tiktok.com/", timeout=6000)
        except Exception as e:
            message= f"No se pudo navegar. {e}"
            print(message)
            browser.close()

        try:
            cookies = context.cookies()
            for cookie in cookies:
                if cookie["name"] == "msToken":
                    token = cookie
                    mstokenPlano = token["value"]
                    if mstokenPlano:
                        message = "\nSe encontró el token necesario para la automatización"
                        return mstokenPlano
                    
        except Exception as e:
            message= f"No se pudo obtener el token {e}"
            print(message)
        finally:
            browser.close()

async def trending_videos(ms_token, idt = None):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "chromium"), headless=False)
        if idt:
            async for comment in api.video(id=idt).comments(count=10,):
                if len(comment.text) < 200:
                    print(comment.text)
        else:
            async for video in api.trending.videos(count=10):
                try:
                    async for comment in video.comments(count=2):
                        if len(comment.text) < 200:
                            print(comment.text)
                except Exception as e:
                    print(f"Hubo un error con la librería: {e}")

        

if __name__ == "__main__":
    mstokenPlano = obtener_mstoken()
    asyncio.run(trending_videos(mstokenPlano, "7264619262075997445"))


