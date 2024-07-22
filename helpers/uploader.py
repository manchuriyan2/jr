import asyncio
import os
import time

from __init__ import LOGGER
from bot import LOGCHANNEL, userBot
from config import Config
from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from helpers.display_progress import Progress


async def uploadVideo(
    c: Client,
    cb: CallbackQuery,
    merged_video_path,
    width,
    height,
    duration,
    video_thumbnail,
    file_size,
    upload_mode: bool,
):
    # Report your errors in telegram group (@yo_codes).
    if Config.IS_PREMIUM:
        sent_ = None
        prog = Progress(cb.from_user.id, c, cb.message)
        async with userBot:
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await userBot.send_video(
                    chat_id=int(LOGCHANNEL),
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"""<blockquote><b>{merged_video_path.rsplit('/',1)[-1]}
                    
Merged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>
User's ID: {cb.from_user.id}
Bot: @{Config.BOT_USERNAME}
</b></blockquote>""",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"**Uploading:\n{merged_video_path.rsplit('/',1)[-1]}**",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await userBot.send_document(
                    chat_id=int(LOGCHANNEL),
                    document=merged_video_path,
                    thumb=video_thumbnail,
                    caption=f"""<blockquote><b>{merged_video_path.rsplit('/',1)[-1]}
                    
Merged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>
User's ID: {cb.from_user.id}
Bot: @{Config.BOT_USERNAME}
</b></blockquote>""",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"**Uploading: {merged_video_path.rsplit('/',1)[-1]}**",
                        c_time,
                    ),
                )
            if sent_ is not None:
                await c.copy_message(
                    chat_id=cb.message.chat.id,
                    from_chat_id=sent_.chat.id,
                    message_id=sent_.id,
                    caption=f"""<blockquote><b>{merged_video_path.rsplit('/',1)[-1]}
                    
Merged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>
User's ID: {cb.from_user.id}
Bot: @{Config.BOT_USERNAME}
</b></blockquote>""",
                )
                # await sent_.delete()
    else:
        try:
            sent_ = None
            prog = Progress(cb.from_user.id, c, cb.message)
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await c.send_video(
                    chat_id=cb.message.chat.id,
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"`{merged_video_path.rsplit('/',1)[-1]}`",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"**Uploading:\n{merged_video_path.rsplit('/',1)[-1]}**",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await c.send_document(
                    chat_id=cb.message.chat.id,
                    document=merged_video_path,
                    thumb=video_thumbnail,
                    caption=f"**{merged_video_path.rsplit('/',1)[-1]}**",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"**Uploading:\n{merged_video_path.rsplit('/',1)[-1]}**",
                        c_time,
                    ),
                )
        except Exception as err:
            LOGGER.info(err)
            await cb.message.edit("Failed to upload")
        if sent_ is not None:
            if Config.LOGCHANNEL is not None:
                media = sent_.video or sent_.document
                await sent_.copy(
                    chat_id=int(LOGCHANNEL),
                    caption=f"""<blockquote><b>{media.file_name}
                   
Merged for: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>
User's ID: {cb.from_user.id}
Bot: @{Config.BOT_USERNAME}
</b></blockquote>""",
                )


async def uploadFiles(
    c: Client,
    cb: CallbackQuery,
    up_path,
    n,
    all
):
    try:
        sent_ = None
        prog = Progress(cb.from_user.id, c, cb.message)
        c_time = time.time()
        sent_: Message = await c.send_document(
            chat_id=cb.message.chat.id,
            document=up_path,
            caption=f"**{up_path.rsplit('/',1)[-1]}**",
            progress=prog.progress_for_pyrogram,
            progress_args=(
                f"**Uploading:\n{up_path.rsplit('/',1)[-1]}**",
                c_time,
                f"\n**Uploading: {n}/{all}**"
            ),
        )
        if sent_ is not None:
            if Config.LOGCHANNEL is not None:
                media = sent_.video or sent_.document
                await sent_.copy(
                    chat_id=int(LOGCHANNEL),
                    caption=f"""<blockquote><b>{media.file_name}
                    
Extracted by: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>
User's ID: {cb.from_user.id}
Bot: @{Config.BOT_USERNAME}
</b></blockquote>""",
                )
    except:
        1    
    1
