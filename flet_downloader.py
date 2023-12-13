import flet as ft
from pytube import YouTube

#TODO: make resolution dropdown menu functional

def main(page):
    
    page.title = "YouTube Downloader"
    
    page.window_width = 550
    page.window_height = 350
    page.window_resizable = False  
    
    
    def download(yt_link):

        try:
            yt_link = text_field.value
            page.update()
            yt_object = YouTube(yt_link)
            finish_label.value = yt_object.title
            media = yt_object.streams.get_highest_resolution()
            media.download()
        except:
            print("error")
        page.update()

    text_field = ft.TextField(label="YouTube Link", width=510)
    finish_label = ft.Text("")
    download_button = ft.ElevatedButton("Download", width= 250, on_click=download)
    dropdown_menu = ft.Dropdown(
        width= 250,
        options=[
            ft.dropdown.Option("360p"),
            ft.dropdown.Option("480p"),
            ft.dropdown.Option("720p")
        ]
    )
    
    page.add(
        text_field,
        finish_label,
        ft.Row(controls=[
            download_button,
            dropdown_menu
        ]))
    
    
        


ft.app(target=main)