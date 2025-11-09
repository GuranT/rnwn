from aiogram import Router, types
from aiogram.filters import Text
from database.user_context import user_manager
from ai.message_processor import message_processor
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Text(text="привет", ignore_case=True))
async def handle_hello(message: types.Message):
    await message.answer("Привет! 👋 Я DeepSeek AI помощник. Чем могу помочь?")

@router.message()
async def handle_all_messages(message: types.Message):
    user_id = message.from_user.id
    user_text = message.text
    
    # Игнорируем команды
    if user_text.startswith('/'):
        return
    
    # Показываем индикатор набора
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    # Получаем режим пользователя
    user = user_manager.get_user(user_id)
    user_manager.increment_message_count(user_id)
    
    try:
        # Обрабатываем сообщение
        response = await message_processor.process_message(
            user_id, 
            user_text, 
            user.current_mode
        )
        
        # Отправляем ответ
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")
        await message.answer("❌ Произошла ошибка при обработке сообщения. Попробуйте еще раз.")
