from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from questions import questions
from utils import load_stats, save_stats

router = Router()


class Quiz(StatesGroup):
    Q = State()


def main_menu_text():
    return "Доступные команды:\n/quiz — начать викторину\n/stats — показать статистику\n/exit — выйти из викторины"


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Напиши /quiz, чтобы начать викторину.\n" + main_menu_text())


@router.message(Command("quiz"))
async def cmd_quiz(message: Message, state: FSMContext):
    await state.set_state(Quiz.Q)
    await state.update_data(current=0, answers=[])
    await ask_question(message, state)


@router.message(Command("exit"))
async def cmd_exit(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == Quiz.Q.state:
        await finish_quiz(message, state, early_exit=True)
    else:
        await message.answer("Вы сейчас не проходите викторину.")


async def ask_question(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data['current']

    if index >= len(questions):
        await finish_quiz(message, state)
        return

    q = questions[index]
    keyboard = [[KeyboardButton(text=option)] for option in q['options']]
    markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

    await message.answer(q['question'], reply_markup=markup)


@router.message(Quiz.Q)
async def quiz_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data['current']
    answers = data['answers']
    answers.append(message.text)
    await state.update_data(current=index + 1, answers=answers)

    await message.answer(f"Вы выбрали: {message.text}", reply_markup=ReplyKeyboardRemove())
    await ask_question(message, state)


async def finish_quiz(message: Message, state: FSMContext, early_exit=False):
    data = await state.get_data()
    answers = data['answers']
    user_id = str(message.from_user.id)

    # Подсчёт очков
    score = 0
    for i, ans in enumerate(answers):
        if i < len(questions) and ans.strip().lower() == questions[i]['correct'].strip().lower():
            score += 1

    stats = load_stats()
    stats[user_id] = {"answers": answers, "score": score}
    save_stats(stats)

    await state.clear()
    if early_exit:
        await message.answer(
            f"Вы вышли из викторины. Ваши ответы сохранены. Очки: {score}/{len(questions)}.\n\n" + main_menu_text())
    else:
        await message.answer(f"Квиз завершён! Вы набрали {score} из {len(questions)}.\n\n" + main_menu_text())


@router.message(Command("stats"))
async def show_stats(message: Message):
    stats = load_stats()
    user_id = str(message.from_user.id)
    user_data = stats.get(user_id)

    if user_data:
        answers = user_data["answers"]
        score = user_data["score"]
        await message.answer(
            f"Последние ответы: {', '.join(answers)}\n"
            f"Правильных ответов: {score} из {len(questions)}"
        )
    else:
        await message.answer("Статистика не найдена.\n" + main_menu_text())
