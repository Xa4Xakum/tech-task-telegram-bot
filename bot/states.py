from aiogram.fsm.state import StatesGroup, State


class Other(StatesGroup):
    write_to_manager = State()
    get_order_id = State()
    upload_files = State()
    rate = State()
    get_language = State()
    init_user = State()


class Mail(StatesGroup):
    get_msg_ru = State()
    get_msg_uz = State()
    check1 = State()
    check2 = State()


class GetPrice(StatesGroup):
    get_start_data = State()
    get_file = State()
    get_size = State()
    get_usage = State()
    get_temperature = State()
    get_environment = State()
    get_color = State()
    get_count = State()
    get_comment = State()
    check = State()


class CompanyInfo(StatesGroup):
    info = State()
