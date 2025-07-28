from typing import List


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
