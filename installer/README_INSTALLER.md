# EZ-CorridorKey Installer

This installer (`EZ-CorridorKey-Installer.exe`) is a "one-click" tool designed to set up the EZ-CorridorKey project on your computer without any manual configuration.

## What this does

### Automatic Updates
The installer uses Git to download the project. If you run the installer again in the same folder later, it will automatically download any new updates from GitHub for you.

### Simple Model Selection
You can use the check-boxes in the installer to choose which AI models you want to download.
*   **CorridorKey Base Model**: The main model needed for the program to work (Required).
*   **VideoMaMa Alpha Generator**: Used for video-based green screening (High VRAM required).
*   **GVM Alpha Generator**: Used for high-resolution green screening.

### Automated Setup
The installer handles all the technical background work:
*   Installs "uv" (a fast package manager) to handle dependencies.
*   Creates a private Python environment (.venv) so it doesn't mess with your global computer settings.
*   Automatically configures PyTorch and CUDA so your graphics card works with the AI.

### Integrated Uninstaller
The installer creates a styled `Uninstall_EZ-CorridorKey.exe` inside your installation folder. Running this will safely close any active project tasks, remove the desktop shortcut, and delete the project folder to free up space.

## How to use it

1.  **Install**: Open `EZ-CorridorKey-Installer.exe`, choose a folder, and click **INSTALL NOW**.
2.  **Run**: Double-click the "EZ-CorridorKey" shortcut that appears on your desktop.
3.  **Uninstall**: Go to your installation folder and run `Uninstall_EZ-CorridorKey.exe`.

## Credits and Collaboration

This installer was developed as a collaborative effort to improve the accessibility of the EZ-CorridorKey project.

*   **Project Concept**: Based on the EZ-CorridorKey project by edenaion.
*   **Development**: Created through a collaborative session between the User and the Antigravity AI assistant.

---
*Maintained for the CorridorKey Community*
