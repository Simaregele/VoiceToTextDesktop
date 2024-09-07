# VoiceToTextDesktop: Installation and Usage Guide

## Application Description
VoiceToTextDesktop is a Windows application that implements voice input as text. It's the simplest way to convert voice to text, allowing you to input information using your voice instead of typing. The application works with any text field in Windows, making it a universal tool for voice input.

Key features:
- Voice input for any text field on Windows
- Automatic saving of converted text to the clipboard
- Use of hotkeys for convenient control
- Perfect solution for those who don't like typing

Important: To open the Windows clipboard to view the saved text, use the key combination Windows + V.

## Contents
1. Cloning the repository
2. System requirements
3. Installing the virtual environment
4. Installing dependencies
5. Creating and configuring the configuration file
6. Creating a shortcut to launch
7. Using the application

## 1. Cloning the repository

1. Open the command prompt (CMD) or terminal.
2. Navigate to the directory where you want to place the project.
3. Execute the command:
   ```
   git clone https://github.com/Simaregele/VoiceToTextDesktop.git
   ```
4. Navigate to the project directory:
   ```
   cd VoiceToTextDesktop
   ```

## 2. System requirements
- Windows 10/11
- Python 3.8 or higher
- Git

## 3. Installing the virtual environment

1. In the project directory, create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```
   .venv\Scripts\activate
   ```

## 4. Installing dependencies

1. Make sure the virtual environment is activated (see step 3.2).

2. Install dependencies from the requirements.txt file:
   ```
   pip install -r requirements.txt
   ```

## 5. Creating and configuring the configuration file

1. In the `app` directory, create a `config.json` file.

2. Open the `app/config.json` file in a text editor.

3. Insert the following configuration template and configure the parameters:
   ```json
   {
     "OPENAI_API_KEY": "Your_OpenAI_API_Key",
     "TEMP_AUDIO_FILE": "temp_audio.wav",
     "HOTKEY": "ctrl+shift+alt+space"
   }
   ```

4. Replace `Your_OpenAI_API_Key` with your actual OpenAI API key. You can also configure hotkeys here.

## 6. Creating a shortcut to launch

1. Locate the `run_app.pyw` file in the project directory.

2. Right-click on `run_app.pyw` and select "Create shortcut".

3. Right-click on the created shortcut and select "Properties".

4. In the properties window, on the "Shortcut" tab, configure the following fields:
   - Target:
     ```
     "C:\Path\To\Your\Project\.venv\Scripts\pythonw.exe" "C:\Path\To\Your\Project\run_app.pyw"
     ```
   - Start in:
     ```
     C:\Path\To\Your\Project
     ```
   - Run: Normal window

5. Click "Apply", then "OK".

To get the exact paths, execute the following commands in the console (in the project's virtual environment):

- To get the path to Python in the virtual environment (which needs to be inserted at the beginning of the "Target" field), enter in the console:
  ```
  python -c "import sys; print(sys.executable)"
  ```

- To get the path to the project's root directory (which should be used for the "Start in" field and the second part of the "Target" field), enter in the console:
  ```
  python -c "import os; print(os.getcwd())"
  ```

## 7. Using the application

1. Launch the application by double-clicking on the created shortcut.

2. The application will start in the system tray.

3. To start recording, press the hotkey combination once (by default CTRL + SHIFT + ALT + space).

4. Speak into the microphone.

5. To stop recording, you have two options:
   - Press the same hotkey combination again (CTRL + SHIFT + ALT + space)
   - Or click on the STOP button that will appear on the screen

6. After stopping the recording, the text will be automatically transcribed, inserted into the active text field, and copied to the clipboard.

7. To open the clipboard and view the saved text, press the key combination Windows + V.

8. After launching, the application appears in the running applications, in the hidden icons (those on the right in the expanding list next to the clock and other information in the Windows taskbar). To exit the application, right-click on the application icon and select "Exit".

Note: When first launched, Windows may request permission to access the microphone. Allow access for the application to work correctly.