import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

def download_playlist_mp3(playlist_url, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    try:
        print(f"Downloading playlist: {playlist_url}")
        command = [
            "yt-dlp",
            "--yes-playlist",
            "-x",
            "--audio-format", "mp3",
            "-o", f"{output_folder}/%(playlist_title)s/%(title)s.%(ext)s",
            playlist_url
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if process.returncode == 0:
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
        else:
            messagebox.showerror("Error", f"Error downloading playlist:\n{error.decode()}")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading playlist: {e}")

def browse_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_selected)

def start_download():
    playlist_url = playlist_url_entry.get()
    output_folder = output_folder_entry.get()

    if not playlist_url or not output_folder:
        messagebox.showwarning("Warning", "Please provide both playlist URL and output folder.")
        return

    threading.Thread(target=download_playlist_mp3, args=(playlist_url, output_folder)).start()

app = tk.Tk()
app.title("YouTube Playlist to MP3 Downloader")
app.geometry("500x200")

tk.Label(app, text="Playlist URL:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
playlist_url_entry = tk.Entry(app, width=50)
playlist_url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(app, text="Output Folder:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
output_folder_entry = tk.Entry(app, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = tk.Button(app, text="Browse", command=browse_output_folder)
browse_button.grid(row=1, column=2, padx=10, pady=10)

download_button = tk.Button(app, text="Download", command=start_download)
download_button.grid(row=2, column=1, pady=20)

app.mainloop()
