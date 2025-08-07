from typing import List

from aiogram.types import Message


def try_to_int(string: str) -> int | List[int] | str:
    '''Пытается преобразовать к числу, вернет результат, либо не преобразованный элемент'''
    try:
        if isinstance(string, list):
            int_list = []
            for i in string:
                as_int = try_to_int(i)
                if isinstance(as_int, str): return as_int
                else: int_list.append(as_int)
            return int_list
        return int(string)
    except:
        return string


def extract_media_info(msg: Message) -> list[dict]:
    result = []

    if msg.photo:
        photo = msg.photo[-1]
        result.append({
            "file_id": photo.file_id,
            "media_type": "photo",
            "caption": msg.caption,
        })

    elif msg.video:
        result.append({
            "file_id": msg.video.file_id,
            "media_type": "video",
            "caption": msg.caption,
        })

    elif msg.document:
        result.append({
            "file_id": msg.document.file_id,
            "media_type": "document",
            "caption": msg.caption,
        })

    elif msg.voice:
        result.append({
            "file_id": msg.voice.file_id,
            "media_type": "voice",
            "caption": msg.caption,
        })

    elif msg.audio:
        result.append({
            "file_id": msg.audio.file_id,
            "media_type": "audio",
            "caption": msg.caption,
        })

    elif msg.animation:
        result.append({
            "file_id": msg.animation.file_id,
            "media_type": "animation",
            "caption": msg.caption,
        })

    return result
