import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import subprocess
import yt_dlp


class YouTubeToMP3:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("540x460")
        self.root.resizable(False, False)
        
        self.download_path = os.path.expanduser("~/Music/YouTube Downloads")
        os.makedirs(self.download_path, exist_ok=True)
        self.download_format = "mp3"
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="YouTube Downloader", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="Video URL:").pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame, font=("Segoe UI", 10))
        self.url_entry.pack(fill=tk.X, pady=(5, 0))
        self.url_entry.bind("<Return>", lambda e: self.start_download())
        
        path_frame = ttk.Frame(main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(path_frame, text="Save to:").pack(anchor=tk.W)
        path_row = ttk.Frame(path_frame)
        path_row.pack(fill=tk.X, pady=(5, 0))
        
        self.path_var = tk.StringVar(value=self.download_path)
        ttk.Entry(path_row, textvariable=self.path_var, state="readonly").pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(path_row, text="Browse", command=self.browse_path).pack(side=tk.LEFT, padx=(5, 0))
        
        format_frame = ttk.LabelFrame(main_frame, text="Format", padding="10")
        format_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.format_var = tk.StringVar(value="mp3")
        ttk.Radiobutton(format_frame, text="MP3 (Audio only, 192kbps)", variable=self.format_var, value="mp3", command=self.on_format_change).pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="MP4 (Video + Audio, best quality)", variable=self.format_var, value="mp4", command=self.on_format_change).pack(anchor=tk.W, pady=(5, 0))
        
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(10, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        self.download_btn = ttk.Button(btn_frame, text="Download MP3", command=self.start_download, style="Accent.TButton")
        self.download_btn.pack(side=tk.LEFT, ipadx=25, ipady=8)
        
        ttk.Button(btn_frame, text="Open Folder", command=self.open_folder).pack(side=tk.RIGHT, ipadx=20, ipady=8)
        
    def on_format_change(self):
        fmt = self.format_var.get()
        self.download_format = fmt
        self.download_btn.config(text=f"Download {fmt.upper()}")
        
    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.download_path)
        if path:
            self.download_path = path
            self.path_var.set(path)
            
    def open_folder(self):
        if sys.platform == "win32":
            os.startfile(self.download_path)
        elif sys.platform == "darwin":
            subprocess.run(["open", self.download_path])
        else:
            subprocess.run(["xdg-open", self.download_path])
            
    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "Please enter a YouTube URL")
            return
            
        self.download_btn.config(state=tk.DISABLED)
        self.progress.start(10)
        self.status_var.set("Downloading...")
        self.url_entry.delete(0, tk.END)
        
        thread = threading.Thread(target=self.download_worker, args=(url,), daemon=True)
        thread.start()
        
    def download_worker(self, url):
        try:
            if self.download_format == "mp3":
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }],
                    "quiet": True,
                    "no_warnings": True,
                }
            else:
                ydl_opts = {
                    "format": "bestvideo+bestaudio/best",
                    "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
                    "merge_output_format": "mp4",
                    "quiet": True,
                    "no_warnings": True,
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.root.after(0, self.on_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_error(str(e)))
            
    def on_success(self):
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Done! Saved to {self.download_path}")
        messagebox.showinfo("Success", f"{self.download_format.upper()} downloaded successfully!")
        
    def on_error(self, error):
        self.progress.stop()
        self.download_btn.config(state=tk.NORMAL)
        self.status_var.set("Error occurred")
        messagebox.showerror("Error", f"Download failed:\n{error}")


def check_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    if not check_ffmpeg():
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "FFmpeg Required",
            "FFmpeg is not installed or not in PATH.\n\n"
            "Please install FFmpeg:\n"
            "• Windows: Download from https://ffmpeg.org/download.html\n"
            "• macOS: brew install ffmpeg\n"
            "• Linux: sudo apt install ffmpeg\n\n"
            "Then restart this app."
        )
        return
        
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("vista" if sys.platform == "win32" else "clam")
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
    
    app = YouTubeToMP3(root)
    root.mainloop()


if __name__ == "__main__":
    main()