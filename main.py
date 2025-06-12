import tkinter
import customtkinter
from customtkinter import filedialog 
# from pytubefix import YouTube, Playlist
import re
import subprocess
import threading


def reset_ui_tab1():
    # Clear the video URL entry
    url_variable.set("")
    playlist_variable.set("")
    # Reset progress bar and percentage
    progper_tab1.configure(text="0%")
    progper_tab2.configure(text="0%")
    progressBar_tab1.set(0)
    progressBar_tab2.set(0)
    # Clear finished label
    finishlabel_tab1.configure(text="")
    finishlabel_tab2.configure(text="")
    # Optionally clear the folder path
    folder_path_tab1.set("")
    folder_path_tab2.set("")
    # Reset title label
    title_1.configure(text="Insert Youtube Video URL", text_color="white")   
    title_2.configure(text="Insert Youtube Playlist URL", text_color="white")     
    

def get_video_title(ytlink):
    command = [
        "yt-dlp",
        "--get-title",
        ytlink
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    print (result.stdout)
    return result.stdout.strip() if result.returncode == 0 else "Error retrieving title"    
        
        
def download_with_ytdlp() :
    try:
        # Build the yt-dlp command
        ytLink=Link_video.get()
        print(ytLink)
        videotitle=get_video_title(ytLink)
        download_path=folder_path_tab1.get()
        print("Video Title:", videotitle)
        title_1.configure(text=videotitle,text_color="white")
        
        
        
        command = [
            "yt-dlp",
            "--no-mtime",  # Add this option
            "-P", download_path,
            "-f", "bestvideo+bestaudio",
            ytLink
        ]
        # Run the command
        # result = subprocess.run(command, capture_output=True, text=True)
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in result.stdout:
            print(line, end="")  # For debugging
            # Look for progress percentage in the output
            if "%" in line:
                match = re.search(r'(\d{1,3}\.\d)%', line)
                if match:
                    percent = float(match.group(1))
                    progper_tab1.configure(text=f"{int(percent)}%")
                    progressBar_tab1.set(percent / 100)
        result.wait()
        if result.returncode == 0:
            print("Download completed successfully.")
            finishlabel_tab1.configure(text="Downloaded Video")
            app.after(5000, reset_ui_tab1)
            
        else:
            print("Error during download:", result.stderr)
    except Exception as e:
        print("Exception occurred:", e)
        finishlabel_tab1.configure(text="Downloaded Error",text_color="red")
    
def download_with_ytdlp_threaded():
    threading.Thread(target=download_with_ytdlp).start()
    
def download_playlist_with_ytdlp_threaded():
    threading.Thread(target=startDownloadplaylist).start()
    
  
def startDownloadplaylist():
    try:
        ytLink=Link_playlist.get()
        print(ytLink)
        videotitle=get_video_title(ytLink)
        download_path=folder_path_tab2.get()
        print("Playlit  Title:", videotitle)
        title_2.configure(text=videotitle,text_color="white")
        
        
        
        command = [
            "yt-dlp",
            "--no-mtime",  # Add this option
            "-P", download_path,
            "-f", "bestvideo+bestaudio",
            ytLink
        ]
        # Run the command
        # result = subprocess.run(command, capture_output=True, text=True)
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in result.stdout:
            print(line, end="")  # For debugging
            # Look for progress percentage in the output
            if "%" in line:
                match = re.search(r'(\d{1,3}\.\d)%', line)
                if match:
                    percent = float(match.group(1))
                    progper_tab2.configure(text=f"{int(percent)}%")
                    progressBar_tab2.set(percent / 100)
        result.wait()
        if result.returncode == 0:
            print("Download completed successfully.")
            finishlabel_tab2.configure(text="Downloaded playlist")
            app.after(5000, reset_ui_tab1)
            
        else:
            print("Error during download:", result.stderr)
    except Exception as e:
        print("Exception occurred:", e)
        finishlabel_tab2.configure(text="Downloaded Error",text_color="red")
        
def on_progress_tab1(stream,chunk,bytes_remaining):
    total_size=stream.filesize
    bytes_downloaded=total_size - bytes_remaining
    percentage_completed=bytes_downloaded / total_size * 100  
    per=str(int(percentage_completed))
    progper_tab1.configure(text=per+"%")
    progper_tab1.update()
    
    progressBar_tab1.set(float(percentage_completed)/100)
    
def on_progress_tab2(stream,chunk,bytes_remaining):
    total_size=stream.filesize
    bytes_downloaded=total_size - bytes_remaining
    percentage_completed=bytes_downloaded / total_size * 100  
    per=str(int(percentage_completed))
    progper_tab2.configure(text=per+"%")
    progper_tab2.update()
    
    progressBar_tab2.set(float(percentage_completed)/100)


customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")

def switch_event_tab1():
    if switch_var_tab1.get() == "off":
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")
        switch_text_var_tab1.set("Light Mode")
        
    else:
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")
        switch_text_var_tab1.set("Dark Mode")
def switch_event_tab2():
    if switch_var_tab2.get() == "off":
        customtkinter.set_appearance_mode("Light")
        customtkinter.set_default_color_theme("blue")
        switch_text_var_tab2.set("Light Mode")
        
    else:
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")
        switch_text_var_tab2.set("Dark Mode")
        

        
        
       
def browse_button_tab1():
    filename = filedialog.askdirectory()
    folder_path_tab1.set(filename)
def browse_button_tab2():
    filename = filedialog.askdirectory()
    folder_path_tab2.set(filename)

#Our application frame

app = customtkinter.CTk()
app.geometry("1080x720")
app.title("Youtube Video Downlaoder")

tabview = customtkinter.CTkTabview(app,width=1000,height=700)
tabview.pack(padx=20, pady=20)
tab_1=tabview.add("Youtube Video")
tab_2=tabview.add("Youtube Playlist")
# appearance mode switching light/Dark

switch_var_tab1= customtkinter.StringVar(value="on")
switch_text_var_tab1=customtkinter.StringVar(value="Dark Mode")
switch_tab1 = customtkinter.CTkSwitch(tab_1,command=switch_event_tab1,
                                 variable=switch_var_tab1, onvalue="on", offvalue="off",button_color="black",textvariable=switch_text_var_tab1)
switch_var_tab2 = customtkinter.StringVar(value="on")
switch_text_var_tab2=customtkinter.StringVar(value="Dark Mode")
switch_tab2 = customtkinter.CTkSwitch(tab_2,command=switch_event_tab2,
                                 variable=switch_var_tab2, onvalue="on", offvalue="off",button_color="black",textvariable=switch_text_var_tab2)

switch_tab1.pack(padx=40,pady=40)
switch_tab2.pack(padx=40,pady=40)

#Adding UI elemets

title_1=customtkinter.CTkLabel(tab_1,text="Insert Youtube Video URL")
title_1.pack(padx=10,pady=10)
title_2=customtkinter.CTkLabel(tab_2,text="Insert Youtube Playlist URL")
title_2.pack(padx=10,pady=10)


url_variable=customtkinter.StringVar()
Link_video = customtkinter.CTkEntry(tab_1,width=450,height=40,textvariable=url_variable)
playlist_variable=customtkinter.StringVar()
Link_playlist = customtkinter.CTkEntry(tab_2,width=450,height=40,textvariable=playlist_variable)
Link_video.pack()
Link_playlist.pack()

#finished downloading
finishlabel_tab1=customtkinter.CTkLabel(tab_1,text="")
finishlabel_tab1.pack()
finishlabel_tab2=customtkinter.CTkLabel(tab_2,text="")
finishlabel_tab2.pack()

# Resolution Options
# option_list=["720p","480p","360p"]
# combobox_var= customtkinter.StringVar()
# combobox = customtkinter.CTkComboBox(app, values=option_list,variable=combobox_var)
# combobox.pack(padx=80,pady=10)

#progress percentage
progper_tab1=customtkinter.CTkLabel(tab_1,text="0%")
progper_tab1.pack()
progressBar_tab1=customtkinter.CTkProgressBar(tab_1,width=600)
progressBar_tab1.set(0)
progressBar_tab1.pack(padx=10,pady=10)

progper_tab2=customtkinter.CTkLabel(tab_2,text="0%")
progper_tab2.pack()
progressBar_tab2=customtkinter.CTkProgressBar(tab_2,width=600)
progressBar_tab2.set(0)
progressBar_tab2.pack(padx=10,pady=10)

#file browse button functionality
folder_path_tab1=customtkinter.StringVar()
file_path_tab1=customtkinter.CTkLabel(tab_1,textvariable=folder_path_tab1)
browse_button_tab_1=customtkinter.CTkButton(tab_1,text="Browse",command=browse_button_tab1)
browse_button_tab_1.pack(padx=10,pady=10)
file_path_tab1.pack(padx=10,pady=10)

folder_path_tab2=customtkinter.StringVar()
file_path_tab2=customtkinter.CTkLabel(tab_2,textvariable=folder_path_tab2)
browse_button_tab_2=customtkinter.CTkButton(tab_2,text="Browse",command=browse_button_tab2)
browse_button_tab_2.pack(padx=10,pady=10)
file_path_tab2.pack(padx=10,pady=10)
#download button
download_tab1 = customtkinter.CTkButton(tab_1,
                                 text="Download",
                                 command=download_with_ytdlp_threaded,
                                 width=200,
                                 height=32,
                                 border_width=0,
                                 corner_radius=32)
download_tab1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
download_tab1.pack(padx=10,pady=10)

download_tab2 = customtkinter.CTkButton(tab_2,
                                 text="Download",
                                 command=download_playlist_with_ytdlp_threaded,
                                 width=200,
                                 height=32,
                                 border_width=0,
                                 corner_radius=32)
download_tab2.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
download_tab2.pack(padx=10,pady=10)

app.mainloop()