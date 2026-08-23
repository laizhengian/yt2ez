import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import subprocess
import yt_dlp


def get_ffmpeg_path():
    """Get path to bundled ffmpeg.exe"""
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller EXE
        base_path = sys._MEIPASS
    else:
        # Running as Python script
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, "ffmpeg.exe")


class yt2ez:
    def __init__(self, root):
        self.root = root
        self.root.title("yt2ez")
        self.root.geometry("540x520")
        self.root.resizable(False, False)
        
        self.download_path = os.path.expanduser("~/Music/yt2ez")
        os.makedirs(self.download_path, exist_ok=True)
        self.download_format = "mp3"
        self.available_formats = []
        self.selected_resolution = "best"
        self.ffmpeg_path = get_ffmpeg_path()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="yt2ez", font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))
        
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(url_frame, text="Video URL:").pack(anchor=tk.W)
        url_row = ttk.Frame(url_frame)
        url_row.pack(fill=tk.X, pady=(5, 0))
        
        self.url_entry = ttk.Entry(url_row, font=("Segoe UI", 10))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.url_entry.bind("<Return>", lambda e: self.start_download())
        
        ttk.Button(url_row, text="Fetch Qualities", command=self.fetch_formats).pack(side=tk.LEFT, padx=(5, 0))
        
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
        ttk.Radiobutton(format_frame, text="MP4 (Video + Audio)", variable=self.format_var, value="mp4", command=self.on_format_change).pack(anchor=tk.W, pady=(5, 0))
        
        self.resolution_frame = ttk.LabelFrame(main_frame, text="Video Quality", padding="10")
        
        ttk.Label(self.resolution_frame, text="Resolution:").pack(anchor=tk.W)
        self.resolution_var = tk.StringVar(value="best (auto)")
        self.resolution_combo = ttk.Combobox(self.resolution_frame, textvariable=self.resolution_var, state="readonly", width=30)
        self.resolution_combo.pack(fill=tk.X, pady=(5, 0))
        self.resolution_combo.bind("<<ComboboxSelected>>", self.on_resolution_change)
        self.resolution_combo["values"] = ["best (auto)"]
        
        self.progress = ttk.Progressbar(main_frame, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(10, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var, font=("Segoe UI", 9)).pack(anchor=tk.W)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 10))
        
        self.download_btn = ttk.Button(btn_frame, text="Download MP3", command=self.start_download, style="Accent.TButton")
        self.download_btn.pack(side=tk.LEFT, ipadx=25, ipady=8)
        
        ttk.Button(btn_frame, text="Open Folder", command=self.open_folder).pack(side=tk.RIGHT, ipadx=20, ipady=8)
        
        self.on_format_change()
        
    def on_format_change(self):
        fmt = self.format_var.get()
        self.download_format = fmt
        self.download_btn.config(text=f"Download {fmt.upper()}")
        
        if fmt == "mp4":
            self.resolution_frame.pack(fill=tk.X, pady=(0, 10), before=self.progress)
            self.fetch_formats()
        else:
            self.resolution_frame.pack_forget()
            
    def on_resolution_change(self, event=None):
        self.selected_resolution = self.resolution_var.get()
        
    def fetch_formats(self):
        url = self.url_entry.get().strip()
        if not url or self.format_var.get() != "mp4":
            return
            
        def fetch():
            try:
                ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True, "ffmpeg_location": self.ffmpeg_path}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get("formats", [])
                    
                video_formats = {}
                for f in formats:
                    if f.get("vcodec") != "none" and f.get("height"):
                        height = f["height"]
                        fs = f.get("filesize") or f.get("filesize_approx") or 0
                        existing_fs = video_formats[height].get("filesize") or video_formats[height].get("filesize_approx") or 0 if height in video_formats else 0
                        if height not in video_formats or fs > existing_fs:
                            video_formats[height] = f
                
                resolutions = sorted(video_formats.keys(), reverse=True)
                resolution_options = ["best (auto)"] + [f"{h}p" for h in resolutions]
                
                self.root.after(0, lambda: self.update_resolution_combo(resolution_options))
            except Exception:
                self.root.after(0, lambda: self.update_resolution_combo(["best (auto)"]))
                
        threading.Thread(target=fetch, daemon=True).start()
        
    def update_resolution_combo(self, options):
        self.resolution_combo["values"] = options
        if self.resolution_var.get() not in options:
            self.resolution_var.set(options[0])
        self.selected_resolution = self.resolution_var.get()
        
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
        
        if self.download_format == "mp3":
            thread = threading.Thread(target=self.download_mp3_worker, args=(url,), daemon=True)
        else:
            thread = threading.Thread(target=self.download_mp4_worker, args=(url,), daemon=True)
        thread.start()
        
    def download_mp3_worker(self, url):
        try:
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
                "socket_timeout": 30,
                "retries": 3,
                "ffmpeg_location": self.ffmpeg_path,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.root.after(0, self.on_success)
        except Exception as e:
            self.root.after(0, lambda: self.on_error(f"MP3 download failed:\n{e}"))
            
    def download_mp4_worker(self, url):
        try:
            res = self.selected_resolution
            if res == "best (auto)":
                format_spec = "bestvideo+bestaudio/best"
            else:
                height = res.replace("p", "")
                format_spec = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"
            
            print(f"MP4 format_spec: {format_spec}")  # Debug
            
            ydl_opts = {
                "format": format_spec,
                "outtmpl": os.path.join(self.download_path, "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "quiet": True,
                "no_warnings": True,
                "socket_timeout": 30,
                "retries": 3,
                "ffmpeg_location": self.ffmpeg_path,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.root.after(0, self.on_success)
        except Exception as e:
            print(f"MP4 error: {e}")  # Debug
            self.root.after(0, lambda: self.on_error(f"MP4 download failed:\n{e}"))
            
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


def main():
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("vista" if sys.platform == "win32" else "clam")
    style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
    
    app = yt2ez(root)
    root.mainloop()


if __name__ == "__main__":
    main()