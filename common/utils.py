import math

SIZE_NAMES = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')


def convert_to_human_readable_size(size: int):
    """
    Конвертирует из байтов в человекочитаемые сокращения размеров.

    :param size: Размер чего-то в байтах.
    :return: Строка с человеческим сокращением размера
    """
    if size == 0:
        return '0B'

    size_index = int(math.floor(math.log(size, 1024)))

    p = math.pow(1024, size_index)
    real_size = round(size / p, 2)

    return f'{real_size} {SIZE_NAMES[size_index]}'


def format_monitoring_message(total_upload: str, total_download: str, current_upload: str, current_download: str):
    message_text = (
        f'Upload: {total_upload}\n'
        f'Download: {total_download}\n'
        f'Upload Speed: {current_upload}/s\n'
        f'Download Speed: {current_download}/s\n'
    )

    return message_text
