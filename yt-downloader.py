import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading
import re
from yt_dlp import YoutubeDL

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader Pro")
        self.root.geometry("900x950")
        self.root.configure(bg="#f5f5f5")
        self.download_thread = None
        self.pause_download = False
        self.cancel_download = False
        self.video_list = []

        # Modern styling
        self.style = ttk.Style()
        self.style.configure("TButton", padding=8, font=("Segoe UI", 10), background="#4CAF50")
        self.style.configure("TLabel", background="#f5f5f5", font=("Segoe UI", 10))
        self.style.configure("TEntry", font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground="#2C3E50")
        self.style.configure("Section.TLabel", font=("Segoe UI", 11, "bold"), foreground="#34495E")

        # Main container with better spacing
        main_container = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
        main_container.pack(fill="both", expand=True)

        # Header
        header_frame = tk.Frame(main_container, bg="#f5f5f5")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="YouTube Downloader Pro", 
                font=("Segoe UI", 20, "bold"), bg="#f5f5f5", fg="#2C3E50").pack()
        tk.Label(header_frame, text="Download videos and playlists from YouTube", 
                font=("Segoe UI", 11), bg="#f5f5f5", fg="#7F8C8D").pack()

        # URL Section
        url_frame = tk.LabelFrame(main_container, text=" YouTube URL ", font=("Segoe UI", 11, "bold"), 
                                 bg="#f5f5f5", fg="#34495E", padx=15, pady=10, relief="groove", bd=1)
        url_frame.pack(fill="x", pady=(0, 15))

        tk.Label(url_frame, text="Enter YouTube URL (Video or Playlist):", 
                bg="#f5f5f5", font=("Segoe UI", 10)).pack(anchor="w")
        
        url_input_frame = tk.Frame(url_frame, bg="#f5f5f5")
        url_input_frame.pack(fill="x", pady=(5, 0))
        
        self.url_entry = ttk.Entry(url_input_frame, font=("Segoe UI", 10))
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(url_input_frame, text="Paste", command=self.paste_url, width=8).pack(side="right")

        # Download Options Section
        options_frame = tk.LabelFrame(main_container, text=" Download Options ", font=("Segoe UI", 11, "bold"),
                                     bg="#f5f5f5", fg="#34495E", padx=15, pady=15, relief="groove", bd=1)
        options_frame.pack(fill="x", pady=(0, 15))

        # Create a grid within options frame
        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(2, weight=1)

        # Download Type
        type_frame = tk.Frame(options_frame, bg="#f5f5f5")
        type_frame.grid(row=0, column=0, sticky="w", padx=(0, 20))
        
        tk.Label(type_frame, text="Download Type:", bg="#f5f5f5", 
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        type_radio_frame = tk.Frame(type_frame, bg="#f5f5f5")
        type_radio_frame.pack(anchor="w", pady=(5, 0))
        
        self.download_type = tk.StringVar(value="video")
        ttk.Radiobutton(type_radio_frame, text="Video (MP4)", variable=self.download_type, 
                       value="video").pack(anchor="w")
        ttk.Radiobutton(type_radio_frame, text="Audio", variable=self.download_type, 
                       value="audio").pack(anchor="w")

        # Video Quality (only show when video is selected)
        self.quality_frame = tk.Frame(options_frame, bg="#f5f5f5")
        self.quality_frame.grid(row=0, column=1, sticky="w", padx=(0, 20))
        
        tk.Label(self.quality_frame, text="Video Quality:", bg="#f5f5f5", 
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        self.quality_var = tk.StringVar(value="best")
        qualities = ["Best Available", "1080p", "720p", "480p", "360p"]
        quality_values = ["best", "1080p", "720p", "480p", "360p"]
        self.quality_combo = ttk.Combobox(self.quality_frame, textvariable=self.quality_var, 
                                         values=qualities, state="readonly", width=12)
        self.quality_combo.pack(anchor="w", pady=(5, 0))

        # Audio Options (only show when audio is selected)
        self.audio_frame = tk.Frame(options_frame, bg="#f5f5f5")
        self.audio_frame.grid(row=0, column=2, sticky="w")
        
        tk.Label(self.audio_frame, text="Audio Settings:", bg="#f5f5f5", 
                font=("Segoe UI", 10, "bold")).pack(anchor="w")
        
        audio_settings_frame = tk.Frame(self.audio_frame, bg="#f5f5f5")
        audio_settings_frame.pack(anchor="w", pady=(5, 0))
        
        # Audio Format
        tk.Label(audio_settings_frame, text="Format:", bg="#f5f5f5").grid(row=0, column=0, sticky="w")
        self.audio_format_var = tk.StringVar(value="mp3")
        audio_formats = ["mp3", "m4a", "wav"]
        self.audio_format_combo = ttk.Combobox(audio_settings_frame, textvariable=self.quality_var, 
                                         values=audio_formats, state="readonly", width=8)
        self.audio_format_combo.grid(row=0, column=1, sticky="w", padx=(5, 15))
        
        # Audio Bitrate
        tk.Label(audio_settings_frame, text="Bitrate:", bg="#f5f5f5").grid(row=0, column=2, sticky="w")
        self.bitrate_var = tk.StringVar(value="192")
        bitrates = ["128", "192", "256", "320"]
        self.bitrate_combo = ttk.Combobox(audio_settings_frame, textvariable=self.bitrate_var, 
                                         values=bitrates, state="readonly", width=6)
        self.bitrate_combo.grid(row=0, column=3, sticky="w", padx=(5, 0))
        
        # Initially hide audio options
        self.audio_frame.grid_remove()
        
        # Bind download type change
        self.download_type.trace('w', self.on_download_type_change)

        # Output Location Section
        output_frame = tk.LabelFrame(main_container, text=" Output Location ", font=("Segoe UI", 11, "bold"),
                                    bg="#f5f5f5", fg="#34495E", padx=15, pady=10, relief="groove", bd=1)
        output_frame.pack(fill="x", pady=(0, 15))

        tk.Label(output_frame, text="Select download folder:", bg="#f5f5f5", 
                font=("Segoe UI", 10)).pack(anchor="w")
        
        folder_frame = tk.Frame(output_frame, bg="#f5f5f5")
        folder_frame.pack(fill="x", pady=(5, 0))
        
        self.folder_entry = ttk.Entry(folder_frame, font=("Segoe UI", 10))
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder, width=10).pack(side="right")
        
        # Set default download folder (Downloads folder)
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.folder_entry.insert(0, downloads_path)

        # Video List Section
        list_frame = tk.LabelFrame(main_container, text=" Playlist Videos ", font=("Segoe UI", 11, "bold"),
                                  bg="#f5f5f5", fg="#34495E", padx=15, pady=10, relief="groove", bd=1)
        list_frame.pack(fill="both", expand=True, pady=(0, 15))

        # Add search/filter for large playlists
        search_frame = tk.Frame(list_frame, bg="#f5f5f5")
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(search_frame, text="Search:", bg="#f5f5f5").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side="left", padx=(5, 10))
        search_entry.bind("<KeyRelease>", self.filter_video_list)
        
        tk.Label(search_frame, text="Videos found:", bg="#f5f5f5").pack(side="left", padx=(20, 5))
        self.video_count_label = tk.Label(search_frame, text="0", bg="#f5f5f5", fg="#E74C3C", font=("Segoe UI", 10, "bold"))
        self.video_count_label.pack(side="left")

        # Video list with scrollbar
        list_container = tk.Frame(list_frame, bg="#f5f5f5")
        list_container.pack(fill="both", expand=True)

        self.video_listbox = tk.Listbox(list_container, height=8, font=("Segoe UI", 10), 
                                       selectbackground="#3498DB", selectforeground="white")
        self.video_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.video_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.video_listbox.config(yscrollcommand=scrollbar.set)

        # Control Buttons - Dipindahkan ke ATAS Progress Section
        button_frame = tk.Frame(main_container, bg="#f5f5f5")
        button_frame.pack(fill="x", pady=(0, 15))

        # Left side buttons
        left_buttons = tk.Frame(button_frame, bg="#f5f5f5")
        left_buttons.pack(side="left")

        ttk.Button(left_buttons, text="Start Download", command=self.start_download, 
                style="Accent.TButton").pack(side="left", padx=(0, 10))

        self.pause_button = ttk.Button(left_buttons, text="Pause", command=self.toggle_pause, 
                                    state="disabled")
        self.pause_button.pack(side="left", padx=(0, 10))

        self.cancel_button = ttk.Button(left_buttons, text="Cancel", command=self.cancel, 
                                    state="disabled")
        self.cancel_button.pack(side="left")

        # Right side status
        right_status = tk.Frame(button_frame, bg="#f5f5f5")
        right_status.pack(side="right")

        tk.Label(right_status, text="Status:", bg="#f5f5f5", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.status_label = tk.Label(right_status, text="Ready", bg="#f5f5f5", fg="#27AE60", 
                                font=("Segoe UI", 10, "bold"))
        self.status_label.pack(side="left", padx=(5, 0))

        # Configure accent button style
        self.style.configure("Accent.TButton", background="#3498DB", foreground="black")

        # Progress Section - Fixed height with scrolling (SETELAH buttons)
        progress_frame = tk.LabelFrame(main_container, text=" Download Progress ", font=("Segoe UI", 11, "bold"),
                                    bg="#f5f5f5", fg="#34495E", padx=15, pady=10, relief="groove", bd=1)
        progress_frame.pack(fill="x", pady=(0, 15))

        # Main container with fixed height
        progress_main = tk.Frame(progress_frame, bg="#f5f5f5")
        progress_main.pack(fill="both", expand=True)

        # Canvas for scrolling with fixed height
        canvas = tk.Canvas(progress_main, bg="#f5f5f5", height=180)  # Fixed height
        scrollbar = ttk.Scrollbar(progress_main, orient="vertical", command=canvas.yview)

        # Scrollable frame inside canvas
        self.progress_container = tk.Frame(canvas, bg="#f5f5f5")
        self.progress_window = canvas.create_window((0, 0), window=self.progress_container, anchor="nw")

        # Configure scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def configure_canvas_width(event):
            canvas.itemconfig(self.progress_window, width=event.width)

        self.progress_container.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 2))
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", on_mousewheel)
        self.progress_container.bind("<MouseWheel>", on_mousewheel)

        self.progress_bars = {}

    def paste_url(self):
        try:
            clipboard = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard)
        except:
            messagebox.showwarning("Paste Error", "Could not paste from clipboard")

    def on_download_type_change(self, *args):
        if self.download_type.get() == "video":
            self.quality_frame.grid()
            self.audio_frame.grid_remove()
        else:
            self.quality_frame.grid_remove()
            self.audio_frame.grid()

    def filter_video_list(self, event=None):
        search_term = self.search_var.get().lower()
        self.video_listbox.delete(0, tk.END)
        
        count = 0
        for title, vid_id in self.video_list:
            if search_term in title.lower():
                self.video_listbox.insert(tk.END, title)
                count += 1
                
        self.video_count_label.config(text=str(count))

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def toggle_pause(self):
        self.pause_download = not self.pause_download
        self.pause_button.config(text="Resume" if self.pause_download else "Pause")
        self.status_label.config(text=f"{'Paused' if self.pause_download else 'Resumed'}")

    def cancel(self):
        self.cancel_download = True
        self.cancel_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        self.status_label.config(text="Cancelling...", fg="#E74C3C")

    def start_download(self):
        url = self.url_entry.get().strip()
        download_type = self.download_type.get()
        quality = "best" if self.quality_var.get() == "Best Available" else self.quality_var.get()
        audio_format = self.audio_format_var.get()
        bitrate = self.bitrate_var.get()
        output_folder = self.folder_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if not output_folder or not os.path.exists(output_folder):
            messagebox.showerror("Error", "Please select a valid output folder")
            return

        # Reset UI
        self.video_listbox.delete(0, tk.END)
        for widget in self.progress_container.winfo_children():
            widget.destroy()
        self.progress_bars = {}
        self.cancel_download = False
        self.pause_download = False
        self.pause_button.config(text="Pause", state="normal")
        self.cancel_button.config(state="normal")
        self.status_label.config(text="Fetching info...", fg="#F39C12")

        # Start download thread
        self.download_thread = threading.Thread(
            target=self.download,
            args=(url, download_type, quality, audio_format, bitrate, output_folder),
            daemon=True
        )
        self.download_thread.start()

    def progress_hook(self, d):
        if self.cancel_download:
            raise Exception("Download cancelled")

        video_id = d.get("info_dict", {}).get("id", "")
        title = d.get("info_dict", {}).get("title", "Unknown")

        if video_id not in self.progress_bars:
            # Create progress bar for new video
            item_frame = tk.Frame(self.progress_container, bg="#f5f5f5")
            item_frame.pack(fill="x", pady=2)
            
            label = tk.Label(item_frame, text=f"{title[:50]}...", bg="#f5f5f5", 
                           font=("Segoe UI", 9), anchor="w")
            label.pack(fill="x")
            
            progress = ttk.Progressbar(item_frame, length=400, mode="determinate")
            progress.pack(fill="x", pady=(2, 0))
            
            self.progress_bars[video_id] = {"frame": item_frame, "label": label, "progress": progress}

        if d["status"] == "downloading":
            percent_str = d.get("_percent_str", "0%")
            percent = float(re.sub(r"[^\d.]", "", percent_str))
            self.progress_bars[video_id]["progress"]["value"] = percent
            self.progress_bars[video_id]["label"].config(text=f"{title[:50]}... {percent:.1f}%")
            self.status_label.config(text=f"Downloading {title[:30]}... {percent:.1f}%")
            self.root.update()

            # Handle pause
            while self.pause_download and not self.cancel_download:
                threading.Event().wait(0.1)

        elif d["status"] == "finished":
            self.progress_bars[video_id]["progress"]["value"] = 100
            self.progress_bars[video_id]["label"].config(text=f"✓ {title[:50]}... Completed", fg="#27AE60")

    def fetch_playlist_info(self, url):
        ydl_opts = {"extract_flat": True, "quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if "entries" in info:
                return [(entry["title"], entry["id"]) for entry in info["entries"]]
            return [(info.get("title", "Unknown"), info.get("id", ""))]

    def download(self, url, download_type, quality, audio_format, bitrate, output_folder):
        try:
            # Fetch playlist info
            self.video_list = self.fetch_playlist_info(url)
            self.root.after(0, self.update_video_list)
            
            # Output template
            output_template = os.path.join(output_folder, "%(playlist_title)s" if "playlist" in url else "", "%(title)s.%(ext)s")

            # yt-dlp options
            ydl_opts = {
                "outtmpl": output_template,
                "progress_hooks": [self.progress_hook],
                "noplaylist": False,
            }

            # Download type
            if download_type == "audio":
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": audio_format,
                        "preferredquality": bitrate,
                    }],
                })
            else:
                ydl_opts.update({
                    "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best" if quality != "best" else "bestvideo+bestaudio/best",
                    "merge_output_format": "mp4",
                })

            # Download
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            if not self.cancel_download:
                self.root.after(0, lambda: self.status_label.config(text="Completed!", fg="#27AE60"))
                self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully!"))
            else:
                self.root.after(0, lambda: self.status_label.config(text="Cancelled", fg="#E74C3C"))

        except Exception as e:
            if not self.cancel_download:
                self.root.after(0, lambda: self.status_label.config(text="Error", fg="#E74C3C"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            else:
                self.root.after(0, lambda: self.status_label.config(text="Cancelled", fg="#E74C3C"))

        finally:
            self.root.after(0, lambda: self.pause_button.config(state="disabled"))
            self.root.after(0, lambda: self.cancel_button.config(state="disabled"))

    def update_video_list(self):
        self.video_listbox.delete(0, tk.END)
        for title, _ in self.video_list:
            self.video_listbox.insert(tk.END, title)
        self.video_count_label.config(text=str(len(self.video_list)))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()