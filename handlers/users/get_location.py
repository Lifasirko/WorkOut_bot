import json
import time
import urllib.error
import urllib.parse
import urllib.request

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from data.config import GOOGLE_API_KEY, TIMEZONE_BASE_URL
from handlers.users.options import options_keyboard
from keyboards.default import location_button
from keyboards.inline.callback_datas import change_user_timezone_callback
from loader import dp
from utils.db_api import quick_commands as commands


@dp.callback_query_handler(change_user_timezone_callback.filter())
# @dp.message_handler(Command("get_location"))
async def share_loc(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_reply_markup()
    updating_user_id = int(callback_data.get("updating_user_id"))

    await call.message.answer(f"Для коректної та своєчасної роботи нагадувань відправте свою локацію:",
                              reply_markup=location_button.keyboard)
    await state.set_state("location")
    await state.set_data(updating_user_id)


@dp.message_handler(content_types=types.ContentType.LOCATION, state="location")
async def get_contact(message: types.Message, state: FSMContext):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    tz = await timezone(lat=latitude, lng=longitude, timestamp=1331161200)
    # timezone_info(lat=latitude, lng=longitude, timestamp=1331161200)
    updating_user_id = await state.get_data("updating_user_id")
    await commands.update_timezone(telegram_id=updating_user_id, timezone=tz)
    await state.finish()
    await message.answer("Дякую, ваш часовий пояс змінено на:\n"
                         f"{tz}", reply_markup=ReplyKeyboardRemove())
    await options_keyboard(message=message)


async def timezone(lat, lng, timestamp):  # TODO: сделать асинхронным
    # Join the parts of the URL together into one string.
    params = urllib.parse.urlencode(
        {"location": f"{lat},{lng}", "timestamp": timestamp, "key": GOOGLE_API_KEY, }
    )
    url = f"{TIMEZONE_BASE_URL}?{params}"

    current_delay = 0.1  # Set the initial retry delay to 100ms.
    max_delay = 5  # Set the maximum retry delay to 5 seconds.

    while True:
        try:
            # Get the API response.
            response = urllib.request.urlopen(url)
        except urllib.error.URLError:
            pass  # Fall through to the retry loop.
        else:
            # If we didn't get an IOError then parse the result.
            result = json.load(response)

            if result["status"] == "OK":
                return result["timeZoneId"]
            elif result["status"] != "UNKNOWN_ERROR":
                # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                # ZERO_RESULTS. There is no point retrying these requests.
                raise Exception(result["error_message"])

        if current_delay > max_delay:
            raise Exception("Too many retry attempts.")

        print("Waiting", current_delay, "seconds before retrying.")

        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.
