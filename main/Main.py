from tkinter import filedialog, StringVar
import customtkinter
from pytube import YouTube
import os
import json

customtkinter.FontManager.load_font("Akira Expended Demo.otf")

def startDownload():
    ytLink = link.get()
    if not ytLink:
        finishlabel.configure(text="No link provided", text_color="red")
        finishlabel.place(x=315, y=175)
        return
    ytObject = YouTube(ytLink, on_progress_callback=on_progress)
    selected_resolution = resolution_var.get()
    selected_format = format_var.get()
    if selected_format == "MP4":
        video = ytObject.streams.filter(res=selected_resolution).first()
    elif selected_format == "MP3":
        video = ytObject.streams.filter(only_audio=True).first()

    directory = filedialog.askdirectory()
    if not directory:
        return

    counter = 0
    while os.path.exists(os.path.join(directory, f"download_{counter}.{selected_format.lower()}")):
        counter += 1

    save_path = os.path.join(directory, f"download_{counter}.{selected_format.lower()}")

    title.configure(text=ytObject.title, text_color="white")
    video.download(filename=save_path, output_path=directory)
    finishlabel.configure(text="Downloaded!", text_color="green")
    finishlabel.place(x=330, y=175)

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    progressbar.set(percentage_of_completion)
    pPercentage.configure(text=f"{per}%")

def on_format_change(*args):
    for button in resolution_buttons:
        if button.winfo_exists():
            button.destroy()

    if format_var.get() == "MP4":
        resolution_var.set("1080p")
        resolution_options = ["1080p", "720p", "480p", "144p"]
        for i, res in enumerate(resolution_options):
            button = customtkinter.CTkRadioButton(app, text=res, variable=resolution_var, value=res,)
            button.place(x=210+i*100, y=220)
            resolution_buttons.append(button)

def on_scale_change(*args):
    scale = scale_var.get()
    if scale == "100%":
        app.geometry("720x480")
    elif scale == "150%":
        app.geometry("1080x720")





customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Downloader")


format_var = StringVar()
format_var.set("MP4") 
format_var.trace("w", on_format_change)
format_options = ["MP4", "MP3"]
for i, fmt in enumerate(format_options):
    customtkinter.CTkRadioButton(app, text=fmt, variable=format_var, value=fmt, font=("Akira Expended Demo.otf",20,"bold")).place(x=295+i*80, y=20)  # Centered and spaced out

# Label
title = customtkinter.CTkLabel(app, text="Youtube Link", font=("Akira Expended Demo.otf",15,"bold"))
title.place(x=325, y=60) 

#link input
url_var = StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.place(x=200, y=90) 

#Progress bar
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.place(x=365, y=130)

progressbar = customtkinter.CTkProgressBar(app, width=400)
progressbar.set(0)
progressbar.place(x=175, y=160) 

resolution_var = StringVar()
resolution_buttons = []

on_format_change()

finishlabel = customtkinter.CTkLabel(app, text="")
finishlabel.place(x=300, y=300)  

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.place(x=300, y=260)

scale_var = StringVar()
scale_var.set("100%")  # default value
scale_var.trace("w", on_scale_change)
scale_options = ["100%", "150%"]

scale_label = customtkinter.CTkLabel(app, text="Tab Scale:", font=("Akira Expended Demo.otf",20,"bold"))
scale_label.place(x=10, y=415)  # Bottom left corner

for i, scale in enumerate(scale_options):
    scale_button = customtkinter.CTkRadioButton(app, text=scale, variable=scale_var, value=scale)
    scale_button.place(x=10+i*80, y=445)  # Below the label

app.mainloop()