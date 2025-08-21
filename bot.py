import os
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import FSInputFile
import asyncio

API_TOKEN = "8018745950:AAHLjt6FCovlKj8WLb1nYF57zVlOB6NkA4g"   # Telegram bot token
ACCESS_TOKEN = "EAAXsb7JPQ1cBPBnqoec00Tk0fc5g1O7RZAYYaE700ZBZAw9ZBrFFUIe17HwC42kZCsWJJmQmTUjFu56Ft0h5KDBJcONddbKRlfcZBFJ6jUx05oWZA3IGFkKKPSGZBfPz7Q7QBS67GmRMF6tCRVAYOW7GoDYZC9QZA6Cl3r04ZA6DIGmp0Vn8kA8FM0RSn9qW5ZCl7goJBzmUsPUGmi0xmQDBNfsZCRXsnFTZBHclbCgHEQM6eHeu0P65LZB74PNXgU1gbELAQZDZD"  # Graph API uchun
BUSINESS_ID = "1988579362071935"  # Instagram business ID

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_instagram_media(url: str):
    """
    Instagram Business API orqali rasm/video olish
    """
    shortcode = url.split("/")[-2]

    # 1. Media ID olish
    media_info_url = f"https://graph.facebook.com/v18.0/ig_shortcode/{shortcode}?fields=id&access_token={ACCESS_TOKEN}"
    media_info = requests.get(media_info_url).json()

    if "id" not in media_info:
        return None, "Media ID olinmadi"

    media_id = media_info["id"]

    # 2. Media URL olish
    media_url = f"https://graph.facebook.com/v18.0/{media_id}?fields=media_type,media_url,caption&access_token={ACCESS_TOKEN}"
    media_data = requests.get(media_url).json()

    if "media_url" not in media_data:
        return None, "Media URL olinmadi"

    return media_data, None


@dp.message(F.text)
async def handle_message(message: types.Message):
    if "instagram.com" in message.text:
        await message.answer("⏳ Instagram media yuklanmoqda...")

        media_data, error = get_instagram_media(message.text.strip())

        if error:
            await message.answer(f"⚠️ Xatolik: {error}")
            return

        media_url = media_data["media_url"]
        media_type = media_data["media_type"]

        # Rasm
        if media_type == "IMAGE":
            await message.answer_photo(media_url, caption=media_data.get("caption", ""))

        # Video
        elif media_type == "VIDEO":
            await message.answer_video(media_url, caption=media_data.get("caption", ""))

        # Carousel (bir nechta media)
        elif media_type == "CAROUSEL_ALBUM":
            await message.answer("📂 Bu postda bir nechta rasm/video bor. Hozircha faqat bitta yuklab olinadi.")
            await message.answer_photo(media_url)

    else:
        await message.answer("Instagram linkini yuboring 🔗")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())



