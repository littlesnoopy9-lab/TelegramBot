from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    main_menu = State()
    quiz = State()
    
    # Quiz steps
    step1_who = State()      # Кто вы?
    step2_what = State()     # Что хотите получить?
    step3_where = State()   # Где нужен бот?
    step4_funcs = State()   # Какие функции?
    step5_budget = State()  # Бюджет
    step6_when = State()     # Когда нужен запуск?
    step7_contact = State()  # Как связаться?
    step_done = State()


# Multiple choice states for step 4
class FuncChoiceStates(StatesGroup):
    selecting = State()


# Booking demo states
class BookingState(StatesGroup):
    choosing_service = State()
    choosing_date = State()
    choosing_time = State()
    confirming = State()