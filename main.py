import customtkinter as ctk
import sounddevice as sd
import numpy as np
import requests
import threading
import os
import webbrowser
import subprocess
import urllib.parse
from flask import Flask, request
import speech_recognition as sr
import multiprocessing
from tkinter import filedialog
import time
import pyautogui
import pyperclip

# Try to import psutil, if not available, use alternative methods
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("psutil not available, using alternative methods")

# --- Part 1: The Background Engine Logic ---
def run_background_engine():
    pool = multiprocessing.Pool(processes=1) # Keep it simple for the engine
    app = Flask(__name__)
    @app.route("/transcribe", methods=["POST"])
    def transcribe_endpoint():
        audio_data = request.data
        audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
        r = sr.Recognizer()
        try:
            text = r.recognize_google(audio)
            return text
        except (sr.UnknownValueError, sr.RequestError):
            return ""
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        os._exit(0)
    
    print("[Engine] Engine is running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)

# --- Application Management Functions ---
def get_app_process_names():
    """Return mapping of app names to process names"""
    return {
        'brave': 'brave.exe',
        'chrome': 'chrome.exe',
        'edge': 'msedge.exe',
        'file explorer': 'explorer.exe',
        'vs code': 'code.exe',
        'microsoft word': 'winword.exe',
        'notepad': 'notepad.exe',
        'calculator': 'calculator.exe',
        'paint': 'mspaint.exe',
        'excel': 'excel.exe',
        'powerpoint': 'powerpnt.exe'
    }

def find_browser_path(browser_name):
    """Find the actual path of browsers"""
    possible_paths = {
        'chrome': [
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Google', 'Chrome', 'Application', 'chrome.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'Application', 'chrome.exe')
        ],
        'brave': [
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'BraveSoftware', 'Brave-Browser', 'Application', 'brave.exe')
        ],
        'edge': [
            os.path.join(os.environ.get('PROGRAMFILES', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', ''), 'Microsoft', 'Edge', 'Application', 'msedge.exe')
        ]
    }
    
    if browser_name.lower() in possible_paths:
        for path in possible_paths[browser_name.lower()]:
            if os.path.exists(path):
                return path
    return None

def is_app_running(app_name):
    """Check if an application is currently running"""
    if not PSUTIL_AVAILABLE:
        return "Unable to check running apps"
    
    process_names = get_app_process_names()
    if app_name.lower() in process_names:
        process_name = process_names[app_name.lower()]
        for process in psutil.process_iter(['name']):
            if process.info['name'].lower() == process_name.lower():
                return True
    return False

def close_application(app_name):
    """Close an application by terminating its process - FIXED VERSION"""
    process_names = get_app_process_names()
    
    if app_name.lower() not in process_names:
        return f"ERROR: Application '{app_name}' not recognized"
    
    process_name = process_names[app_name.lower()]
    closed_count = 0
    
    if not PSUTIL_AVAILABLE:
        # Alternative method using taskkill - MORE AGGRESSIVE
        try:
            # Use taskkill to close all instances
            result = subprocess.run(['taskkill', '/f', '/im', process_name], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return f"SUCCESS: Closed {app_name}"
            else:
                # Check if the process is actually running
                try:
                    check_result = subprocess.run(['tasklist', '/fi', f'imagename eq {process_name}'], 
                                                capture_output=True, text=True)
                    if process_name not in check_result.stdout:
                        return f"SUCCESS: {app_name} was not running"
                    else:
                        return f"ERROR: Could not close {app_name}. Process still running."
                except:
                    return f"ERROR: Could not close {app_name}"
        except subprocess.TimeoutExpired:
            return f"ERROR: Timeout closing {app_name}"
        except Exception as e:
            return f"ERROR: Could not close {app_name} - {str(e)}"
    
    # Original psutil method - IMPROVED
    try:
        for process in psutil.process_iter(['name', 'pid']):
            if process.info['name'] and process.info['name'].lower() == process_name.lower():
                try:
                    # Try graceful termination first
                    process.terminate()
                    closed_count += 1
                except:
                    try:
                        # Force kill if graceful doesn't work
                        process.kill()
                        closed_count += 1
                    except:
                        continue
        
        if closed_count > 0:
            return f"SUCCESS: Closed {closed_count} {app_name} process(es)"
        else:
            # Double check if the process is actually running
            if not is_app_running(app_name):
                return f"SUCCESS: {app_name} was not running"
            else:
                return f"ERROR: {app_name} is still running after attempt to close"
                
    except Exception as e:
        return f"ERROR: Could not close {app_name} - {str(e)}"

def open_application(app_name):
    """Open an application with proper path resolution"""
    # First try using webbrowser for browsers (most reliable)
    if app_name.lower() in ['chrome', 'brave', 'edge']:
        try:
            if app_name.lower() == 'chrome':
                webbrowser.get('chrome').open_new('')
            elif app_name.lower() == 'brave':
                # Try to find Brave path and open it
                brave_path = find_browser_path('brave')
                if brave_path:
                    subprocess.Popen([brave_path])
                else:
                    webbrowser.open('https://brave.com')  # Fallback
            elif app_name.lower() == 'edge':
                webbrowser.get('edge').open_new('')
            return f"SUCCESS: Opened {app_name}"
        except Exception as e:
            # Fallback to direct path finding
            pass
    
    # Try finding the actual executable path
    app_paths = {
        'chrome': find_browser_path('chrome'),
        'brave': find_browser_path('brave'),
        'edge': find_browser_path('edge'),
        'file explorer': 'explorer.exe',
        'vs code': ['code.exe'],
        'microsoft word': ['winword.exe'],
        'notepad': ['notepad.exe'],
        'calculator': ['calc.exe'],
        'paint': ['mspaint.exe'],
        'excel': ['excel.exe'],
        'powerpoint': ['powerpnt.exe']
    }
    
    if app_name.lower() in app_paths:
        try:
            path = app_paths[app_name.lower()]
            if path and isinstance(path, str) and os.path.exists(path):
                subprocess.Popen([path])
            elif isinstance(path, list):
                subprocess.Popen(path)
            else:
                # Final fallback - try just the executable name
                process_names = get_app_process_names()
                if app_name.lower() in process_names:
                    subprocess.Popen([process_names[app_name.lower()]])
                else:
                    return f"ERROR: Could not find {app_name} installation"
            
            return f"SUCCESS: Opened {app_name}"
        except Exception as e:
            return f"ERROR: Could not open {app_name} - {str(e)}"
    
    return f"ERROR: Application '{app_name}' not recognized"

def write_to_search_bar(text):
    """Write text to search bar of active browser"""
    try:
        # Copy text to clipboard
        pyperclip.copy(text)
        time.sleep(0.5)
        
        # Paste using Ctrl+V
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.5)
        
        # Press Enter to search
        pyautogui.press('enter')
        return f"SUCCESS: Wrote '{text}' to search bar"
    except Exception as e:
        return f"ERROR: Could not write to search bar - {str(e)}"

def get_search_answer(question):
    """Get answer for a search question (simplified version)"""
    try:
        return f"I searched for: {question}. For detailed answers, please check the search results."
    except Exception as e:
        return f"ERROR: Could not get answer - {str(e)}"

# --- Part 2: The GUI Client and Command Logic ---
# Global variable to store user-selected base path
USER_SELECTED_PATH = None

def extract_app_name(command, action_type):
    """Extract application name from command more accurately"""
    command = command.lower().strip()
    
    # Remove action words
    command = command.replace(action_type, "").strip()
    
    # List of all available applications
    all_apps = list(get_app_process_names().keys())
    
    # Find which app is mentioned in the command
    for app in all_apps:
        if app in command:
            return app
    
    # If no exact match found, try partial matching for common cases
    if "chrome" in command:
        return "chrome"
    elif "brave" in command:
        return "brave"
    elif "edge" in command:
        return "edge"
    elif "code" in command or "vs code" in command:
        return "vs code"
    elif "word" in command:
        return "microsoft word"
    elif "notepad" in command:
        return "notepad"
    elif "calculator" in command:
        return "calculator"
    elif "paint" in command:
        return "paint"
    elif "excel" in command:
        return "excel"
    elif "powerpoint" in command or "ppt" in command:
        return "powerpoint"
    elif "explorer" in command or "file" in command:
        return "file explorer"
    
    return None

def parse_and_execute(command_text):
    global USER_SELECTED_PATH
    command = command_text.lower().strip()
    
    # Use user-selected path or default fallback
    if USER_SELECTED_PATH:
        base_path = USER_SELECTED_PATH
    else:
        home_dir = os.path.expanduser('~')
        base_path = os.path.join(home_dir, 'Documents', 'VoiceAssistantFiles')
    
    os.makedirs(base_path, exist_ok=True)
    try:
        # New application control commands - FIXED LOGIC
        if "close" in command:
            app_name = extract_app_name(command, "close")
            if app_name:
                return close_application(app_name)
        
        elif "open" in command:
            app_name = extract_app_name(command, "open")
            if app_name:
                return open_application(app_name)
        
        # Search and write functionality
        elif "write" in command or "search" in command:
            if "who is" in command or "what is" in command or "how to" in command:
                # Extract the question
                question = command.replace("write", "").replace("search", "").strip()
                # Write to search bar
                write_result = write_to_search_bar(question)
                # Get answer
                answer = get_search_answer(question)
                return f"{write_result}\n{answer}"
            else:
                # Just write text to search bar
                text_to_write = command.replace("write", "").replace("search", "").strip()
                return write_to_search_bar(text_to_write)
        
        # Existing commands
        elif "create folder" in command:
            name = command.replace("create folder", "").strip()
            path = os.path.join(base_path, name)
            os.makedirs(path, exist_ok=True)
            return f"SUCCESS: Created folder '{name}'"
        elif "open folder" in command:
            name = command.replace("open folder", "").strip()
            path = os.path.join(base_path, name)
            if os.path.isdir(path):
                os.startfile(path)
                return f"SUCCESS: Opened folder '{name}'"
            else:
                return f"ERROR: Folder '{name}' not found."
        elif "open web" in command:
            url = command.replace("open web", "").strip()
            if not url.startswith("http"):
                url = f"https://{url}"
            webbrowser.open(url)
            return f"SUCCESS: Opening '{url}'"
        else:
            if not command: return "Heard nothing."
            return f"Command not recognized: '{command}'"
    except Exception as e:
        return f"ERROR: {e}"

class AssistantWidget(ctk.CTk):
    def __init__(self):
        global USER_SELECTED_PATH
        super().__init__()
        self.title("Assistant")
        self.geometry("140x200")  # Made taller for new buttons
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        
        # Add dragging functionality
        self._offset_x = 0
        self._offset_y = 0
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<B1-Motion>", self.do_move)
        
        # Add close button
        self.close_button = ctk.CTkButton(self, text="X", font=("Arial", 12), width=20, height=20, command=self.close_app)
        self.close_button.place(x=115, y=5)
        
        self.mic_button = ctk.CTkButton(self, text="🎤", font=("Arial", 40), command=self.listen)
        self.mic_button.pack(expand=True, fill="both", pady=(30,0))
        
        # Add choose location button
        self.location_button = ctk.CTkButton(self, text="Choose Location", font=("Arial", 10), width=120, height=25, command=self.choose_location)
        self.location_button.pack(pady=(5,0))
        
        # Add apps button to show available applications
        self.apps_button = ctk.CTkButton(self, text="Show Apps", font=("Arial", 10), width=120, height=25, command=self.show_apps)
        self.apps_button.pack(pady=(5,0))
        
        self.feedback_label = ctk.CTkLabel(self, text="Click to Speak", wraplength=120)
        self.feedback_label.pack()
        
        # Show warning if psutil is not available
        if not PSUTIL_AVAILABLE:
            self.feedback_label.configure(text="Install psutil for better app control\nClick to Speak")
    
    def show_apps(self):
        """Show available applications in the feedback label"""
        apps = list(get_app_process_names().keys())
        apps_list = "Available apps: " + ", ".join(apps)
        self.feedback_label.configure(text=apps_list)
        # Reset feedback after 5 seconds
        threading.Timer(5.0, lambda: self.feedback_label.configure(text="Click to Speak")).start()
    
    def choose_location(self):
        global USER_SELECTED_PATH
        selected_path = filedialog.askdirectory(title="Choose folder location for voice commands")
        if selected_path:
            USER_SELECTED_PATH = selected_path
            self.feedback_label.configure(text=f"Location set to: {os.path.basename(selected_path)}")
            # Reset feedback after 3 seconds
            threading.Timer(3.0, lambda: self.feedback_label.configure(text="Click to Speak")).start()
    
    def start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")
    
    def close_app(self):
        try:
            requests.post("http://127.0.0.1:5000/shutdown")
        except requests.exceptions.ConnectionError:
            pass
        self.destroy()
    
    def listen(self):
        self.mic_button.configure(state="disabled", text="...")
        self.feedback_label.configure(text="Listening...")
        # Run the recording in a separate thread to keep the GUI responsive
        threading.Thread(target=self.record_and_process, daemon=True).start()

    def record_and_process(self):
        samplerate = 44100
        duration = 4
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        audio_data = recording.tobytes()
        try:
            response = requests.post("http://127.0.0.1:5000/transcribe", data=audio_data)
            transcribed_text = response.text
            feedback = parse_and_execute(transcribed_text)
            self.feedback_label.configure(text=feedback)
        except requests.exceptions.ConnectionError:
            self.feedback_label.configure(text="Error: Engine not running.")
        finally:
            self.mic_button.configure(state="normal", text="🎤")

# --- Part 3: Main Launcher ---
if __name__ == '__main__':
    multiprocessing.freeze_support()
    
    # Check for required modules
    try:
        import pyautogui
        import pyperclip
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install missing modules using: pip install pyautogui pyperclip")
        input("Press Enter to exit...")
        exit(1)
    
    # Start the background engine in a separate, non-blocking thread
    engine_thread = threading.Thread(target=run_background_engine, daemon=True)
    engine_thread.start()
    
    # Start the GUI in the main thread
    app = AssistantWidget()
    app.mainloop()