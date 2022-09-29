import math

from common.const import Emoji
from common.models.monitoring_models import JobData

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


def format_monitoring_message(
        uploaded: str,
        downloaded: str,
        current_upload: str,
        current_download: str,
        job_data: JobData,
):
    message_text = (
        f'{Emoji.up_graph} Upload:' + '\t' * 23 + f'{uploaded}\n' +
        f'{Emoji.down_graph} Download:' + '\t' * 18 + f'{downloaded}\n' +
        '\n'
        f'{Emoji.up_arrow} Upload Speed:' + '\t' * 11 + f'{current_upload}/s\n' +
        f'{Emoji.down_arrow} Download Speed:' + '\t' * 6 + f'{current_download}/s\n' +
        f'\n'
        f'{Emoji.calendar} Monitoring start at {job_data.start_date}\n'
        f'{Emoji.clock} Last update at {job_data.last_update}\n'
    )

    return message_text
