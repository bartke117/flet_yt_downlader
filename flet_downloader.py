import flet as ft
import os
from pytube import YouTube
import pytube.exceptions as exceptions

#TODO: make resolution dropdown menu functional

def main(page):
    
    page.title = "YouTube Downloader"
    page.window_width = 550
    page.window_height = 450
    page.window_resizable = False  
    
    def download(yt_link):
        try:
            yt_link = text_field.value
            page.update()
            yt_object = YouTube(yt_link, on_progress_callback=download_progress)
            media_name.value = f"Downloading now: {yt_object.title}..."
            if format_dd.value == "audio":
                print("__audio__")
                media = yt_object.streams.get_audio_only(subtype='mp4')
            elif format_dd.value == "video":
                print("__video__")
                resolution = dropdown_value(quality_dd)
                print("RES",resolution)
                highest_possible_res = yt_object.streams.get_highest_resolution().resolution
                print(f"user res: {resolution}{type(resolution)}\nhighest possible res:{highest_possible_res}{type(highest_possible_res)}")
                if int(resolution[:-1]) > int(highest_possible_res[:-1]): #check if users
                    media = yt_object.streams.get_highest_resolution()
                    print("downloading with highest possible resolution", highest_possible_res)
                    display_snack_bar("orange", highest_possible_res)
                else:
                    media = yt_object.streams.filter(res=resolution).first()
                    print("downloading with user resolution", resolution)
                    display_snack_bar("green")

            media.download()            
            # os.path.join("downloads", f"{media_name.value}.mp4")
            # media.download(output_path="downloads")
        except Exception as e:
            print(e)
            display_snack_bar("red")
        media_name.value = yt_object.title
        page.update()

    def download_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completion_percentage = bytes_downloaded / total_size
        progress_bar.value = completion_percentage
        print(completion_percentage)
        page.update()
        
    def dropdown_value(v):
        return quality_dd.value
    
    def check_format(format):
        if format_dd.value == "audio":
            quality_dd.disabled = True
            quality_dd.value = ""
            page.update()
        else:
            quality_dd.disabled = False
            page.update()
        
    def display_snack_bar(color, res=None):
        if color == "green":
            page.snack_bar = ft.SnackBar(ft.Text("File downloaded!"))
            page.snack_bar.bgcolor = color
            page.snack_bar.open = True
        elif color == "red":
            page.snack_bar = ft.SnackBar(ft.Text("An error occured."))
            page.snack_bar.bgcolor = color
            page.snack_bar.open = True
        else:
            page.snack_bar = ft.SnackBar(ft.Text(f"Downloaded with highest possible resolution - {res}"))
            page.snack_bar.bgcolor = color
            page.snack_bar.open = True
        
    text_field = ft.TextField(label="Paste YouTube link here", width=510)
    download_button = ft.ElevatedButton("Download", width=530, color="amber", on_click=download)
    progress_bar = ft.ProgressBar(width=540, value=0, color="amber")
    media_name = ft.Text("", width=530)
    snack_bar = ft.SnackBar(
        content=ft.Text("")
    )
    
    quality_dd = ft.Dropdown(
        width= 250,
        label="quality",
        on_change=dropdown_value,
        options=[
            ft.dropdown.Option("144p"),
            ft.dropdown.Option("240p"),
            ft.dropdown.Option("360p"),
            ft.dropdown.Option("480p"),
            ft.dropdown.Option("720p"),
            ft.dropdown.Option("1080p")
        ]
    )
    
    format_dd = ft.Dropdown(
        width=250,
        label="format",
        on_change=check_format,
        options=[
            ft.dropdown.Option("audio"),
            ft.dropdown.Option("video")
        ]
    )
    
    page.add(
        text_field,
        ft.Row(controls=[
            quality_dd,
            format_dd
        ]),
        download_button,
        progress_bar,
        media_name,
        snack_bar
        )
ft.app(target=main)