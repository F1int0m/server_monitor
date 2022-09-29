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

    bytes_sent, bytes_recv = get_total_network_load()

    upload_speed = bytes_sent - job_data.old_upload_bytes
    download_speed = bytes_recv - job_data.old_received_bytes

    total_upload = convert_to_human_readable_size(bytes_sent)
    total_download = convert_to_human_readable_size(bytes_recv)
    current_upload = convert_to_human_readable_size(upload_speed / job_data.update_interval)
    current_download = convert_to_human_readable_size(download_speed / job_data.update_interval)

    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=format_monitoring_message(
            total_upload=total_upload,
            total_download=total_download,
            current_upload=current_upload,
            current_download=current_download
        )
    )

    job_data.old_received_bytes = bytes_recv
    job_data.old_upload_bytes = bytes_sent


async def start_monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    repeat_interval = context.args[0] if len(context.args) != 0 else config.DEFAULT_UPDATE_INTERVAL
    job_data = JobData(update_interval=repeat_interval)

    await context.bot.send_message(chat_id=chat_id, text='Начал мониторинг для этого чата')

    context.job_queue.run_repeating(
        callback=monitoring_job,
        interval=job_data.update_interval,
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
