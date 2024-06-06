from aiogram import types

from loader import dp


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_file_id_p(message: types.Message):
    await message.reply(message.photo[-1].file_id)


@dp.message_handler(content_types=types.ContentType.VIDEO)
async def get_file_id_video(message: types.Message):
    await message.reply(message.video.file_id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def get_file_id_document(message: types.Message):
    await message.reply(message.document.file_id)


@dp.message_handler(content_types=types.ContentType.ANIMATION)
async def get_file_id_animation(message: types.Message):
    await message.reply(message.animation.file_id)


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
