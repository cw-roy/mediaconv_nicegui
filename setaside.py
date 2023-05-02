#!/usr/bin/env python3

import asyncio
import os
import shutil
import subprocess

from nicegui import app, events, ui

# create data directory
os.makedirs("data", exist_ok=True)


# FFMpeg conversion command with option switch to keep quality at original
def convert(source: str):
    output_filename = os.path.splitext(source)[0] + "_converted.mp4"
    subprocess.call(["ffmpeg", "-i", source, "-q:v", "0", output_filename])


async def handle_upload(args: events.UploadEventArguments):
    os.chdir(
        os.path.dirname(os.path.abspath(__file__))
    )  # sets path to current directory
    if args.type.startswith("video/"):
        video_exts = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mkv"]
        file_ext = os.path.splitext(args.name)[1].lower()
        if file_ext in video_exts:
            shutil.rmtree("data", ignore_errors=True)
            os.makedirs("data", exist_ok=True)
            os.chdir("data")
            with open(args.name, "wb") as f:
                f.write(args.content.read())
            with ui.spinner("dots", size="xl"):
                await asyncio.to_thread(convert, args.name)
            results.clear()
            with results:
                ui.video(
                    f"/data/{os.path.splitext(args.name)[0]}_converted.mp4"
                ).classes("w-96 drop-shadow-md rounded")
                ui.button(
                    "Download Converted File",
                    url=f"/data/{os.path.splitext(args.name)[0]}_converted.mp4",
                    download=f"{os.path.splitext(args.name)[0]}_converted.mp4",
                )
                ui.label("Conversion complete.")
            os.chdir("..")
        else:
            ui.notify(
                "Please upload a video file in a supported format: "
                + ", ".join(video_exts)
            )
    else:
        ui.notify("Please upload a video file")
    upload.run_method("reset")


os.makedirs("data", exist_ok=True)
app.add_static_files("/data", "data")

with ui.column().classes("w-full items-center"):
    ui.label("Convert video to MP4 format").classes("text-3xl m-3")
    upload = ui.upload(
        label="pick a video file", auto_upload=True, on_upload=handle_upload
    )
    results = ui.row().classes("w-full justify-center mt-6")

ui.run()
