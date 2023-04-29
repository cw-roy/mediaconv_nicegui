#!/usr/bin/env python3

"""Modified Nicegui ffmpeg_extract_images example to convert videos"""

import asyncio
import os
import pathlib
import shlex
import shutil
import subprocess
from pyffmpeg import FFmpeg
from nicegui import app, events, ui

def convert(source: str, destination: str):
    ff = FFmpeg()
    options_string = f"-i {source} -q:v 0 {destination}"
    ff.options(options_string.split())

def get_output_filename(input_filename: str) -> str:
    """Returns the output filename with .mp4 extension"""
    if not input_filename.lower().endswith(".mp4"):
        return f"{input_filename}.mp4"
    else:
        return input_filename

async def handle_upload(args: events.UploadEventArguments):
    if "video" in args.type:
        shutil.rmtree("data", ignore_errors=True)
        os.makedirs("data", exist_ok=True)
        os.chdir("data")
        input_filename = args.name
        output_filename = get_output_filename(input_filename)
        with open(input_filename, "wb") as f:
            f.write(args.content.read())
            results.clear()
            with results:
                ui.spinner("dots", size="xl")
            await asyncio.to_thread(convert, input_filename, output_filename)
            os.remove(input_filename)
            results.clear()
            message = f"File {input_filename} converted to {output_filename}"
            ui.label(message).classes("text-lg")
            with results:
                ui.button("Download", link=f"/data/{output_filename}")
        os.chdir("..")
    else:
        ui.notify("Please upload a video file")
    upload.run_method("reset")

os.makedirs("data", exist_ok=True)
app.add_static_files("/data", "data")

with ui.column().classes("w-full items-center"):
    ui.label("Convert video").classes("text-3xl m-3")
    upload = ui.upload(
        label="pick a video file", auto_upload=True, on_upload=handle_upload
    )
    results = ui.row().classes("w-full justify-center mt-6")

ui.run()
