import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
import os
import sys
import shutil

class InstallerWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("EZ-CorridorKey Setup")
        self.geometry("600x480")
        self.resizable(False, False)
        
        # Installer state
        self.install_dir = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "EZ-CorridorKey"))
        self.download_base = tk.BooleanVar(value=True)
        self.download_gvm = tk.BooleanVar(value=False)
        self.download_videomama = tk.BooleanVar(value=False)
        self.create_shortcut = tk.BooleanVar(value=True)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure overall style
        style = ttk.Style(self)
        style.theme_use('default')
        
        bg_main = "#141300"
        bg_alt = "#1E1D13"
        bg_dark = "#0E0D00"
        fg_text = "#E0E0E0"
        accent = "#FFF203"
        accent_hover = "#FFFF66"
        border = "#454430"
        
        self.configure(bg=bg_main)
        
        # Override ttk styles
        style.configure("TFrame", background=bg_main)
        style.configure("TCheckbutton", background=bg_main, foreground=fg_text, font=("Segoe UI", 10), indicatorcolor=bg_dark, indicatorbackground=bg_dark)
        style.map("TCheckbutton",
            indicatorcolor=[('selected', accent), ('active', border)],
            background=[('active', bg_main)]
        )
        
        # Header
        header_frame = tk.Frame(self, bg=bg_dark, height=80, highlightbackground="#2A2910", highlightthickness=1)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="EZ-CorridorKey", font=("Segoe UI", 24, "bold"), fg=accent, bg=bg_dark).pack(pady=5)
        tk.Label(header_frame, text="AI Green Screen made simple", font=("Segoe UI", 10), fg="#999980", bg=bg_dark).pack()
        
        # Content frame
        self.content_frame = tk.Frame(self, bg=bg_main, padx=30, pady=20)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Install Location
        tk.Label(self.content_frame, text="Select Installation Folder:", font=("Segoe UI", 10, "bold"), fg=fg_text, bg=bg_main).pack(anchor=tk.W, pady=(0, 5))
        
        loc_frame = tk.Frame(self.content_frame, bg=bg_main)
        loc_frame.pack(fill=tk.X, pady=(0, 20))
        
        entry = tk.Entry(loc_frame, textvariable=self.install_dir, font=("Segoe UI", 10), bg="#1A1900", fg=fg_text, insertbackground=fg_text, relief=tk.FLAT, highlightbackground=border, highlightcolor=accent, highlightthickness=1)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=4)
        
        browse_btn = tk.Button(loc_frame, text="Browse...", command=self.browse_loc, bg="#2A2910", fg=fg_text, font=("Segoe UI", 9, "bold"), relief=tk.FLAT, activebackground="#3A3920", activeforeground=accent)
        browse_btn.pack(side=tk.RIGHT, ipadx=10, ipady=2)
        
        # Models
        tk.Label(self.content_frame, text="Select Models to Download:", font=("Segoe UI", 10, "bold"), fg=fg_text, bg=bg_main).pack(anchor=tk.W, pady=(0, 5))
        models_frame = tk.Frame(self.content_frame, bg=bg_alt, highlightbackground="#2A2910", highlightthickness=1, padx=10, pady=10)
        models_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Checkbutton(models_frame, text="CorridorKey Base Model (Required, 1.5GB)", state=tk.DISABLED, variable=self.download_base).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(models_frame, text="VideoMaMa Alpha Generator (~37GB VRAM Heavy)", variable=self.download_videomama).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(models_frame, text="GVM Alpha Generator (~6GB Local High-Res)", variable=self.download_gvm).pack(anchor=tk.W, pady=2)
        
        # Options
        tk.Label(self.content_frame, text="Additional Options:", font=("Segoe UI", 10, "bold"), fg=fg_text, bg=bg_main).pack(anchor=tk.W, pady=(0, 5))
        ttk.Checkbutton(self.content_frame, text="Create Desktop Shortcut", variable=self.create_shortcut).pack(anchor=tk.W, padx=10)
        
        # Install Button
        self.install_btn = tk.Button(self.content_frame, text="INSTALL NOW", bg=accent, fg="#000000", font=("Segoe UI", 12, "bold"), command=self.start_install, relief=tk.FLAT, activebackground=accent_hover)
        self.install_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0), ipady=10)
        
        # Log Box (Hidden initially)
        self.log_text = tk.Text(self.content_frame, height=10, state=tk.DISABLED, font=("Consolas", 9), bg="#0E0D00", fg="#808070", relief=tk.FLAT, highlightbackground=border, highlightthickness=1)
        
    def browse_loc(self):
        d = filedialog.askdirectory(initialdir=self.install_dir.get())
        if d:
            if not d.replace('\\', '/').rstrip('/').endswith('EZ-CorridorKey'):
                d = os.path.join(d, "EZ-CorridorKey")
            d = os.path.normpath(d)
            self.install_dir.set(d)
            
    def append_log(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.update_idletasks()

    def run_cmd(self, cmd, cwd=None):
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                shell=True, text=True, cwd=cwd
            )
            for line in iter(process.stdout.readline, ''):
                self.append_log(line.strip())
            process.stdout.close()
            process.wait()
            return process.returncode
        except Exception as e:
            self.append_log(f"Error executing command: {str(e)}")
            return 1

    def start_install(self):
        target = self.install_dir.get().strip()
        
        # Ensure it creates an EZ-CorridorKey subfolder so it doesn't dump files straight into a root drive
        if not target.replace('\\', '/').rstrip('/').endswith('EZ-CorridorKey'):
            target = os.path.join(target, "EZ-CorridorKey")
            self.install_dir.set(target)
        
        if not os.path.exists(target):
            try:
                os.makedirs(target)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create directory: {e}")
                return
                
        # Hide standard UI, show logs
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
            
        tk.Label(self.content_frame, text="Installing EZ-CorridorKey...", font=("Segoe UI", 14, "bold"), fg="#FFF203", bg="#141300").pack(pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Start thread so GUI doesn't freeze
        threading.Thread(target=self.install_process, daemon=True).start()
        
    def install_process(self):
        target = self.install_dir.get()
        
        self.append_log(f"Attempting to clone repository into {target}...")
        
        # Make sure git is installed
        res = self.run_cmd("git --version")
        if res != 0:
            self.append_log("FATAL: Git is not installed. Please install Git for Windows.")
            messagebox.showerror("Error", "Git is not installed.")
            self.quit()
            return

        # Clone or pull
        if os.path.exists(os.path.join(target, ".git")):
            self.append_log("Repository exists, pulling latest...")
            self.run_cmd("git pull", cwd=target)
        else:
            self.run_cmd(f'git clone https://github.com/edenaion/EZ-CorridorKey.git "{target}"')

        os.chdir(target)

        # Install uv
        self.append_log("\nLocating/Installing 'uv' package manager...")
        self.run_cmd('powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"')
        
        uv_path = os.path.join(os.environ.get("USERPROFILE"), ".local", "bin")
        os.environ["PATH"] = uv_path + os.pathsep + os.environ["PATH"]
        uv_cmd = "uv" if shutil.which("uv") else os.path.join(uv_path, "uv.exe")

        self.append_log("\nCreating Python Virtual Environment (.venv)...")
        self.run_cmd(f"{uv_cmd} venv .venv")

        self.append_log("\nInstalling Dependencies (this will take a while for PyTorch CUDA)...")
        python_exe = os.path.join(target, ".venv", "Scripts", "python.exe")
        self.run_cmd(f"{uv_cmd} pip install --python {python_exe} --torch-backend=auto -e .")

        self.append_log("\nDownloading Core CorridorKey Model (1.5GB)...")
        self.run_cmd(f'"{python_exe}" scripts/setup_models.py --corridorkey')

        if self.download_gvm.get():
            self.append_log("\nDownloading GVM Optional Alpha Model (6GB)...")
            self.run_cmd(f'"{python_exe}" scripts/setup_models.py --gvm')

        if self.download_videomama.get():
            self.append_log("\nDownloading VideoMaMa Heavy Alpha Model (37GB)...")
            self.run_cmd(f'"{python_exe}" scripts/setup_models.py --videomama')

        if self.create_shortcut.get():
            self.append_log("\nCreating Desktop Shortcut...")
            shortcut_path = os.path.join(os.path.expanduser("~"), "Desktop", "EZ-CorridorKey.lnk")
            target_path = os.path.join(target, ".venv", "Scripts", "pythonw.exe")
            work_dir = target
            icon_path = os.path.join(target, "ui", "theme", "corridorkey.ico")
            
            ps_script = f'''
            $ws = New-Object -ComObject WScript.Shell
            $s = $ws.CreateShortcut("{shortcut_path}")
            $s.TargetPath = "{target_path}"
            $s.Arguments = "main.py"
            $s.WorkingDirectory = "{work_dir}"
            $s.IconLocation = "{icon_path},0"
            $s.Description = "EZ-CorridorKey AI Green Screen"
            $s.Save()
            '''
            cmd = f'powershell -ExecutionPolicy ByPass -Command "{ps_script.strip().replace(chr(10), "; ")}"'
            self.run_cmd(cmd)

        self.append_log("\nInstalling GUI Uninstaller...")
        uninstaller_path = os.path.join(target, "Uninstall_EZ-CorridorKey.exe")
        try:
            shutil.copy2(sys.executable, uninstaller_path)
        except Exception as e:
            self.append_log(f"Warning: Could not copy uninstaller executable: {e}")

        self.append_log("\n=============================================")
        self.append_log("   INSTALLATION COMPLETE")
        self.append_log("=============================================")
        
        messagebox.showinfo("Success", "EZ-CorridorKey installation complete.\nApplication shortcut created on desktop.")
        
        # Change finish button to exit
        btn = tk.Button(self.content_frame, text="EXIT WIZARD", bg="#2CC350", fg="#000000", font=("Segoe UI", 12, "bold"), command=self.quit, relief=tk.FLAT, activebackground="#3DD662")
        btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0), ipady=10)

class UninstallerWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("EZ-CorridorKey Uninstaller")
        self.geometry("600x480")
        self.resizable(False, False)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configure overall style
        bg_main = "#141300"
        bg_dark = "#0E0D00"
        fg_text = "#E0E0E0"
        accent = "#D10000" # Red for uninstall
        accent_hover = "#FF4040"
        border = "#454430"
        
        self.configure(bg=bg_main)
        
        # Header
        header_frame = tk.Frame(self, bg=bg_dark, height=80, highlightbackground="#2A2910", highlightthickness=1)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="EZ-CorridorKey Uninstaller", font=("Segoe UI", 24, "bold"), fg=accent, bg=bg_dark).pack(pady=5)
        tk.Label(header_frame, text="Remove AI Green Screen completely", font=("Segoe UI", 10), fg="#999980", bg=bg_dark).pack()
        
        # Content frame
        self.content_frame = tk.Frame(self, bg=bg_main, padx=30, pady=20)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        try:
            target = os.path.dirname(os.path.abspath(sys.executable))
        except:
            target = "Unknown Location"

        tk.Label(self.content_frame, text="Warning: This action cannot be undone.", font=("Segoe UI", 12, "bold"), fg=accent, bg=bg_main).pack(pady=(20, 10))
        tk.Label(self.content_frame, text=f"This will permanently delete the following folder and all of its contents:\n\n{target}\n\nAny downloaded models and environments will be removed.", justify=tk.CENTER, font=("Segoe UI", 10), fg=fg_text, bg=bg_main).pack(pady=10)
        
        # Uninstall Button
        self.uninstall_btn = tk.Button(self.content_frame, text="UNINSTALL NOW", bg=accent, fg="#FFFFFF", font=("Segoe UI", 12, "bold"), command=self.start_uninstall, relief=tk.FLAT, activebackground=accent_hover)
        self.uninstall_btn.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0), ipady=10)
        
    def start_uninstall(self):
        confirm = messagebox.askyesno("Confirm Uninstall", "Are you absolutely sure you want to permanently delete EZ-CorridorKey?")
        if not confirm:
            return
            
        target = os.path.dirname(os.path.abspath(sys.executable))
        shortcut_path = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop", "EZ-CorridorKey.lnk")
        
        # Spawn cleanup script
        tmp_script = os.path.join(os.environ.get("TEMP", ""), "ez_corridorkey_cleanup.bat")
        
        with open(tmp_script, "w") as f:
            f.write(f"""@echo off
TITLE Removing EZ-CorridorKey...
echo Closing any running processes...
powershell -Command "Get-Process | Where-Object {{ $_.Path -match 'EZ-CorridorKey' }} | Stop-Process -Force -ErrorAction SilentlyContinue"
echo Deleting shortcut...
if exist "{shortcut_path}" del /f /q "{shortcut_path}"
echo Waiting for uninstaller to close...
timeout /t 3 /nobreak >nul
echo Deleting folder...
rmdir /s /q "{target}"
echo Cleanup complete.
del "%~f0"
""")
        
        subprocess.Popen(f'start "" "{tmp_script}"', shell=True)
        self.quit()

if __name__ == "__main__":
    if "uninstall" in os.path.basename(sys.executable).lower() or "--uninstall" in sys.argv:
        app = UninstallerWizard()
    else:
        app = InstallerWizard()
    app.mainloop()
