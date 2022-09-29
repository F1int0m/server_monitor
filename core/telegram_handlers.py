import datetime

from telegram import Update
from telegram.ext import ContextTypes

import config
from common.models.monitoring_models import JobData
from common.utils import convert_to_human_readable_size, format_monitoring_message
from core.system_motitoring import get_total_network_load


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет. Я Мониторю сервак Миши и Никиты')


async def monitoring_job(context: ContextTypes.DEFAULT_TYPE):
    job_data: JobData = context.job.data
    chat_id = context.job.chat_id

    bytes_sent, bytes_recv = get_total_network_load()

    upload_bytes = bytes_sent - job_data.old_upload_bytes
    download_bytes = bytes_recv - job_data.old_received_bytes

    current_uploaded = convert_to_human_readable_size(job_data.current_upload_bytes)
    current_downloaded = convert_to_human_readable_size(job_data.current_received_bytes)

    current_upload = convert_to_human_readable_size(upload_bytes / job_data.update_interval)
    current_download = convert_to_human_readable_size(download_bytes / job_data.update_interval)

    message_text = format_monitoring_message(
        uploaded=current_uploaded,
        downloaded=current_downloaded,
        current_upload=current_upload,
        current_download=current_download,
        job_data=job_data,
    )

    if not job_data.message_id:
        message = await context.bot.send_message(
            chat_id=chat_id,
            text='Жду начала'
        )
        job_data.message_id = message.id

    await context.bot.edit_message_text(
        text=message_text,
        chat_id=chat_id,
        message_id=job_data.message_id,
    )

    job_data.old_received_bytes = bytes_recv
    job_data.old_upload_bytes = bytes_sent

    job_data.current_received_bytes += download_bytes
    job_data.current_upload_bytes += upload_bytes

    job_data.last_update = datetime.datetime.utcnow()


async def start_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if context.job_queue.get_jobs_by_name(str(chat_id)):
        await context.bot.send_message(chat_id=chat_id, text='Уже мониторю этот чат')
        return

    repeat_interval = context.args[0] if len(context.args) != 0 else config.DEFAULT_UPDATE_INTERVAL
    bytes_sent, bytes_recv = get_total_network_load()

    job_data = JobData(update_interval=repeat_interval, old_received_bytes=bytes_recv, old_upload_bytes=bytes_sent)

    await context.bot.send_message(chat_id=chat_id, text='Начал мониторинг для этого чата')

    context.job_queue.run_repeating(
        callback=monitoring_job,
        interval=job_data.update_interval,
        first=0,
        chat_id=chat_id,
        data=job_data,
        name=str(chat_id),
    )


async def stop_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
    if current_jobs:
        for job in current_jobs:
            job.schedule_removal()

    await context.bot.send_message(chat_id=chat_id, text='Выключил мониторинг для этого чата')


async def total_network_load(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    bytes_sent, bytes_recv = get_total_network_load()

    total_upload = convert_to_human_readable_size(bytes_sent)
    total_download = convert_to_human_readable_size(bytes_recv)

    await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f'Всего загружено: {total_download}\n'
            f'Всего отдано: {total_upload}'
        )
    )
