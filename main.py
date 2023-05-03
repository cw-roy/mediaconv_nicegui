#!/usr/bin/env python

"""Using Nicegui front end for FFMpeg file conversion"""

import asyncio
import os
import shutil
import subprocess

from nicegui import app, events, ui


def convert(source: str):
    """FFMpeg command "ffmpeg -i <infile> -q:v 0 <outfile>"""
    output_filename = os.path.splitext(source)[0] + "_converted.mp4"
    subprocess.call(["ffmpeg", "-i", source, "-q:v", "0", output_filename])


async def handle_upload(args: events.UploadEventArguments):
    """Select the file, perform naming operations"""
    if args.type.startswith("video/"):
        video_exts = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"]
        file_ext = os.path.splitext(args.name)[1].lower()
        if file_ext in video_exts:
            shutil.rmtree("data", ignore_errors=True)
            os.makedirs("data", exist_ok=True)
            os.chdir("data")
            with open(args.name, "wb") as f:
                f.write(args.content.read())
            await asyncio.to_thread(convert, args.name)
            with results:
                ui.video(
                    f"/data/{os.path.splitext(args.name)[0]}_converted.mp4"
                ).classes("w-96 drop-shadow-md rounded")
            os.chdir("..")
            # ui.label("Conversion Complete.")
        else:
            ui.notify(
                "Please upload a video file in a supported format: "
                + ", ".join(video_exts)
            )
    else:
        ui.notify("Please upload a video file")
    upload.run_method("reset")


def handle_clear():
    """Clear the previous results and reset the upload component"""
    results.clear()
    upload.run_method("reset")


os.makedirs("data", exist_ok=True)
app.add_static_files("/data", "data")

with ui.column().classes("w-full items-center"):
    ui.label("Convert video to MP4 format").classes("text-3xl m-3")
    upload = ui.upload(
        label="Pick a video file", auto_upload=True, on_upload=handle_upload
    )
    results = ui.row().classes("w-full justify-center mt-6")
    clear_button = ui.button("Clear Results", on_click=handle_clear).classes("mt-3")

ui.run()
