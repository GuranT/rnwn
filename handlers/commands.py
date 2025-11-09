from aiogram import Router, types
from aiogram.filters import Command
from database.user_context import UserManager

router = Router()
user_manager = UserManager()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = user_manager.get_user(message.from_user.id)
    
    welcome_text = """
🤖 **DeepSeek AI Assistant**

Добро пожаловать! Я ваш AI помощник на основе DeepSeek.

**Основные команды:**
/chat - Начать диалог с AI
/mode - Сменить режим работы
/clear - Очистить историю
/stats - Статистика
/help - Помощь

Просто напишите сообщение, и я отвечу!
    """
    
    await message.answer(welcome_text)

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
📖 **Помощь по боту**

**Команды:**
/start - Начало работы
/chat - Чат с AI
/mode <режим> - Сменить режим
/clear - Очистить контекст
/stats - Ваша статистика

**Режимы работы:**
• assistant - Общий ассистент
• developer - Помощь с кодом  
• creative - Креативные задачи
• quick - Краткие ответы

**Пример:**
/mode developer
    """
    await message.answer(help_text)

@router.message(Command("mode"))
async def cmd_mode(message: types.Message):
    args = message.text.split()
    available_modes = ["assistant", "developer", "creative", "quick"]
    
    if len(args) < 2:
        modes_text = "\n".join([f"• {mode}" for mode in available_modes])
        await message.answer(f"**Доступные режимы:**\n{modes_text}\n\nИспользование: `/mode developer`")
        return
    
    new_mode = args[1].lower()
    if new_mode not in available_modes:
        await message.answer("❌ Неверный режим. Используйте: assistant, developer, creative, quick")
        return
    
    user_manager.update_user_mode(message.from_user.id, new_mode)
    await message.answer(f"✅ Режим изменен на: **{new_mode}**")

@router.message(Command("clear"))
async def cmd_clear(message: types.Message):
    from ai.message_processor import message_processor
    message_processor.clear_user_history(message.from_user.id)
    user_manager.clear_user_data(message.from_user.id)
    await message.answer("✅ История диалога очищена!")

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user = user_manager.get_user(message.from_user.id)
    stats_text = f"""
📊 **Ваша статистика:**

• ID: {user.user_id}
• Режим: {user.current_mode}
• Сообщений: {user.message_count}
• Статус: {'Активен' if user.is_active else 'Неактивен'}
    """
    await message.answer(stats_text)
