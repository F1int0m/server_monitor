import psutil


def get_total_network_load():
    """
    Возвращает общие полученные байты и общие отправленные.
    :return:
    """
    io = psutil.net_io_counters()

    return io.bytes_recv, io.bytes_sent
