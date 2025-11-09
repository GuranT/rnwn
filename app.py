import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import commands, chat, admin
from config.settings import settings

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def main():
    if not settings.BOT_TOKEN:
        logger.error("BOT_TOKEN не установлен!")
        return
    
    if not settings.DEEPSEEK_API_KEY:
        logger.warning("DEEPSEEK_API_KEY не установлен! Бот будет работать в режиме заглушки")
    
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(commands.router)
    dp.include_router(chat.router)
    dp.include_router(admin.router)
    
    logger.info("Бот запущен!")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
