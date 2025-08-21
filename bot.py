import instaloader
import os
import shutil
from aiogram import Bot, Dispatcher, types
import asyncio

API_TOKEN = "8018745950:AAHLjt6FCovlKj8WLb1nYF57zVlOB6NkA4g"  # o'z tokeningizni qo'ying
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

L = instaloader.Instaloader()

DOWNLOADS_DIR = "downloads"

async def clear_downloads():
    """downloads papkasini tozalash"""
    if os.path.exists(DOWNLOADS_DIR):
        shutil.rmtree(DOWNLOADS_DIR)

async def download_instagram_media(url: str):
    """Instagramdan video yoki rasm yuklab olish"""
    shortcode = url.split("/")[-2]  # linkdan post ID olish
    post = instaloader.Post.from_shortcode(L.context, shortcode)

    # avval eski fayllarni tozalaymiz
    await clear_downloads()
    os.mkdir(DOWNLOADS_DIR)

    # yangi postni yuklaymiz
    L.download_post(post, target=DOWNLOADS_DIR)

    # yuklangan fayllarni topamiz
    files = [os.path.join(DOWNLOADS_DIR, f) for f in os.listdir(DOWNLOADS_DIR)]
    media_files = [f for f in files if f.endswith(".mp4") or f.endswith(".jpg")]

    return media_files

@dp.message()
async def handle_message(message: types.Message):
    if "instagram.com" in message.text:
        url = message.text.strip()
        await message.answer("⏳ Media yuklanmoqda, kuting...")

        try:
            files = await download_instagram_media(url)

            if not files:
                await message.answer("❌ Media topilmadi yoki qo'llab-quvvatlanmaydi.")
                return

            for file_path in files:
                if file_path.endswith(".mp4"):
                    await bot.send_video(chat_id=message.chat.id, video=types.FSInputFile(file_path))
                elif file_path.endswith(".jpg"):
                    await bot.send_photo(chat_id=message.chat.id, photo=types.FSInputFile(file_path))

            # yuborilgandan keyin tozalash
            await clear_downloads()

        except Exception as e:
            await message.answer(f"⚠️ Xatolik: {e}")
    else:
        await message.answer("Instagram linkini yuboring 🔗")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
