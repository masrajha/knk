import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import threading
from pathlib import Path
import re
import tempfile
import shutil

class AudioConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Converter - Fixed Path Handling")
        self.root.geometry("700x550")
        self.root.resizable(True, True)
        
        # Variables
        self.input_files = []  # This will store full paths
        self.output_format = tk.StringVar(value="mp3")
        self.quality = tk.StringVar(value="320k")
        self.output_dir = tk.StringVar(value="")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Audio File Converter", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 15))
        
        # Input files section
        ttk.Label(main_frame, text="Input Files (Full Path):").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.file_listbox = tk.Listbox(main_frame, height=8, selectmode=tk.EXTENDED)
        self.file_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S), pady=(0, 10))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(button_frame, text="Add Files", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Remove Selected", command=self.remove_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear All", command=self.clear_files).pack(side=tk.LEFT)
        
        # Output format section
        format_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="5")
        format_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(format_frame, text="Format:").grid(row=0, column=0, sticky=tk.W)
        
        format_combo = ttk.Combobox(format_frame, textvariable=self.output_format, 
                                   values=["mp3", "wav", "aac", "m4a", "flac", "ogg"], 
                                   state="readonly", width=10)
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 20))
        
        ttk.Label(format_frame, text="Quality:").grid(row=0, column=2, sticky=tk.W)
        
        quality_combo = ttk.Combobox(format_frame, textvariable=self.quality,
                                    values=["320k", "256k", "192k", "128k", "96k", "64k"],
                                    state="readonly", width=10)
        quality_combo.grid(row=0, column=3, sticky=tk.W, padx=(5, 0))
        
        # Output directory section
        ttk.Label(format_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        
        output_entry = ttk.Entry(format_frame, textvariable=self.output_dir, width=40)
        output_entry.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=(5, 5), pady=(10, 0))
        
        ttk.Button(format_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=3, pady=(10, 0))
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Conversion Progress", padding="5")
        progress_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=(5, 0))
        
        self.current_file_label = ttk.Label(progress_frame, text="")
        self.current_file_label.grid(row=2, column=0, columnspan=4, sticky=tk.W, pady=(2, 0))
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Conversion Log", padding="5")
        log_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.log_text = tk.Text(log_frame, height=6, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=7, column=0, columnspan=4, pady=(10, 0))
        
        ttk.Button(control_frame, text="Start Conversion", command=self.start_conversion).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(6, weight=1)
        format_frame.columnconfigure(1, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def clean_filename(self, filename):
        """Clean filename by removing or replacing problematic characters"""
        # Remove invalid characters for Windows filenames
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        
        # Replace multiple spaces with single space
        filename = re.sub(r'\s+', ' ', filename)
        
        # Limit filename length
        if len(filename) > 150:
            name, ext = os.path.splitext(filename)
            filename = name[:150-len(ext)] + ext
            
        return filename.strip()
    
    def safe_convert(self, input_file, output_path):
        """Convert file with error handling for problematic filenames"""
        try:
            # Log the full paths being used
            self.log_message(f"  Input: {input_file}")
            self.log_message(f"  Output: {output_path}")
            
            # First try direct conversion
            cmd = ['ffmpeg', '-i', input_file, '-b:a', self.quality.get(), '-y', output_path]
            self.log_message(f"  Command: ffmpeg -i [input] -b:a {self.quality.get()} -y [output]")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                return True, "Success"
            else:
                # If direct conversion fails, try with temporary file
                self.log_message(f"  Direct conversion failed, trying temporary file method...")
                
                # Create temporary file with safe name
                with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                try:
                    # Copy original file to temporary location
                    self.log_message(f"  Copying to temporary file: {temp_path}")
                    shutil.copy2(input_file, temp_path)
                    
                    # Convert from temporary file
                    cmd = ['ffmpeg', '-i', temp_path, '-b:a', self.quality.get(), '-y', output_path]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        return True, "Success (via temp file)"
                    else:
                        error_msg = f"FFmpeg error: {result.stderr[:200]}"
                        self.log_message(f"  Temp file conversion failed: {error_msg}")
                        return False, error_msg
                        
                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                        self.log_message("  Temporary file cleaned up")
                        
        except Exception as e:
            error_msg = f"Conversion error: {str(e)}"
            self.log_message(f"  Exception: {error_msg}")
            return False, error_msg
    
    def log_message(self, message):
        """Add message to log with thread-safe GUI update"""
        def update_log():
            self.log_text.insert(tk.END, f"{message}\n")
            self.log_text.see(tk.END)
            self.root.update_idletasks()
        
        self.root.after(0, update_log)
    
    def clear_log(self):
        """Clear the log text"""
        self.log_text.delete(1.0, tk.END)
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.aac *.m4a *.flac *.ogg *.webm *.opus *.wma"),
                ("All Files", "*.*")
            ]
        )
        if files:
            # Store full paths
            self.input_files.extend(files)
            self.update_file_listbox()
            self.log_message(f"Added {len(files)} file(s)")
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Audio Files")
        if folder:
            audio_extensions = ('.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg', '.webm', '.opus', '.wma')
            for file_path in Path(folder).rglob('*'):
                if file_path.suffix.lower() in audio_extensions:
                    # Store full path
                    self.input_files.append(str(file_path))
            self.update_file_listbox()
            self.log_message(f"Added folder: {folder}")
    
    def remove_files(self):
        selected_indices = self.file_listbox.curselection()
        removed_count = 0
        for index in reversed(selected_indices):
            if 0 <= index < len(self.input_files):
                removed_file = self.input_files.pop(index)
                removed_count += 1
                self.log_message(f"Removed: {os.path.basename(removed_file)}")
        self.update_file_listbox()
        if removed_count > 0:
            self.log_message(f"Removed {removed_count} file(s)")
    
    def clear_files(self):
        self.input_files.clear()
        self.update_file_listbox()
        self.log_message("Cleared all files")
    
    def update_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.input_files:
            # Show both filename and partial path for clarity
            display_text = f"{os.path.basename(file_path)} | {os.path.dirname(file_path)[-30:] if len(os.path.dirname(file_path)) > 30 else os.path.dirname(file_path)}"
            self.file_listbox.insert(tk.END, display_text)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            self.log_message(f"Output directory set to: {directory}")
    
    def start_conversion(self):
        if not self.input_files:
            messagebox.showwarning("Warning", "Please select at least one file to convert.")
            return
        
        # Verify all files exist before starting
        missing_files = []
        for file_path in self.input_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
        
        if missing_files:
            error_msg = f"{len(missing_files)} file(s) not found:\n" + "\n".join(missing_files[:3])
            if len(missing_files) > 3:
                error_msg += f"\n... and {len(missing_files) - 3} more"
            messagebox.showerror("File Not Found", error_msg)
            return
        
        # Start conversion in separate thread to avoid freezing GUI
        thread = threading.Thread(target=self.convert_files)
        thread.daemon = True
        thread.start()
    
    def convert_files(self):
        total_files = len(self.input_files)
        successful = 0
        failed = []
        
        # Determine output directory
        output_dir = self.output_dir.get()
        if not output_dir:
            output_dir = os.getcwd()  # Use current directory if none specified
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        self.progress_bar['maximum'] = total_files
        self.progress_bar['value'] = 0
        
        self.log_message(f"Starting conversion of {total_files} files...")
        self.log_message(f"Output directory: {output_dir}")
        
        for i, input_file in enumerate(self.input_files):
            try:
                # Update GUI
                filename = os.path.basename(input_file)
                self.current_file_label.config(text=f"Converting: {filename}")
                self.status_label.config(text=f"Processing {i+1}/{total_files}")
                
                # Double-check file exists
                if not os.path.exists(input_file):
                    error_msg = f"Input file not found: {input_file}"
                    self.log_message(f"  ERROR: {error_msg}")
                    failed.append((filename, error_msg))
                    continue
                
                # Generate safe output filename
                input_filename = os.path.basename(input_file)
                clean_name = self.clean_filename(os.path.splitext(input_filename)[0]) + '.' + self.output_format.get()
                output_path = os.path.join(output_dir, clean_name)
                
                self.log_message(f"Converting: {filename}")
                
                # Perform conversion with error handling
                success, message = self.safe_convert(input_file, output_path)
                
                if success:
                    successful += 1
                    self.log_message(f"  ✓ Success: {clean_name}")
                else:
                    failed.append((filename, message))
                    self.log_message(f"  ✗ Failed: {message}")
                
                # Update progress
                self.progress_bar['value'] = i + 1
                self.root.update_idletasks()
                
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                failed.append((filename, error_msg))
                self.log_message(f"  ✗ Unexpected error: {str(e)}")
        
        # Show results
        self.current_file_label.config(text="")
        self.status_label.config(text=f"Completed: {successful}/{total_files} successful")
        
        result_msg = f"Conversion completed!\nSuccessful: {successful}\nFailed: {len(failed)}"
        
        if failed:
            # Show detailed error report
            error_details = "Failed files:\n" + "\n".join([f"- {f[0]}: {f[1][:100]}..." for f in failed[:5]])
            if len(failed) > 5:
                error_details += f"\n... and {len(failed) - 5} more files"
            
            messagebox.showerror("Conversion Complete with Errors", 
                               f"{result_msg}\n\n{error_details}")
        else:
            messagebox.showinfo("Conversion Complete", 
                              f"{result_msg}\n\nAll files converted successfully!")
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

def main():
    root = tk.Tk()
    app = AudioConverterGUI(root)
    
    # Check FFmpeg availability
    if not app.check_ffmpeg():
        messagebox.showerror("FFmpeg Not Found", 
                           "FFmpeg is not installed or not in system PATH.\n\n"
                           "Please install FFmpeg and ensure it's accessible from command line.")
        return
    
    root.mainloop()

if __name__ == "__main__":
    main()