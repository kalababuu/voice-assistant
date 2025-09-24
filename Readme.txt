🎯 Voice Commands Reference
📱 Application Commands
Open Applications
Command	What It Does	Example
open chrome	Opens Google Chrome	"open chrome"
open brave	Opens Brave Browser	"open brave browser"
open edge	Opens Microsoft Edge	"open edge"
open vs code	Opens Visual Studio Code	"open vs code"
open microsoft word	Opens Microsoft Word	"open word"
open notepad	Opens Notepad	"open notepad"
open calculator	Opens Calculator	"open calculator"
open paint	Opens Microsoft Paint	"open paint"
open excel	Opens Microsoft Excel	"open excel"
open powerpoint	Opens Microsoft PowerPoint	"open powerpoint"
open file explorer	Opens File Explorer	"open file explorer"
Close Applications
Command	What It Does	Example
close chrome	Closes Google Chrome	"close chrome"
close brave	Closes Brave Browser	"close brave"
close edge	Closes Microsoft Edge	"close edge"
close vs code	Closes Visual Studio Code	"close vs code"
close microsoft word	Closes Microsoft Word	"close word"
close notepad	Closes Notepad	"close notepad"
close calculator	Closes Calculator	"close calculator"
close paint	Closes Microsoft Paint	"close paint"
close excel	Closes Microsoft Excel	"close excel"
close powerpoint	Closes Microsoft PowerPoint	"close powerpoint"
close file explorer	Closes File Explorer	"close file explorer"
🌐 Web & Search Commands
Web Browsing
Command	What It Does	Example
open web [website]	Opens website in browser	"open web google.com"
open web [url]	Opens full URL	"open web https://github.com"
Search & Typing
Command	What It Does	Example
write [text]	Types text in active search bar	"write weather today"
search [query]	Searches the query online	"search python tutorials"
who is [person]	Searches for person info	"who is the president"
what is [topic]	Searches for topic info	"what is artificial intelligence"
how to [task]	Searches for instructions	"how to bake a cake"
📁 File Management Commands
Command	What It Does	Example
create folder [name]	Creates new folder	"create folder my projects"
open folder [name]	Opens existing folder	"open folder documents"
🖥️ User Interface Guide
Main Window Controls
🎤 Microphone Button: Click and speak to give commands

Choose Location: Set default folder for file operations

Show Apps: Display list of supported applications

X Button: Close the application completely

Drag Anywhere: Click and drag to move the window

Status Messages
The assistant provides feedback after each command:

✅ SUCCESS: Command executed successfully

❌ ERROR: Command failed or wasn't understood

🎧 Listening...: Recording your voice

⏳ Processing...: Converting speech to text

💡 Usage Tips & Best Practices
Speaking Clearly
Speak naturally but clearly

Wait for the "Listening..." prompt before speaking

Keep commands concise: "open chrome" vs "can you please open chrome for me"

Pause briefly between words for better recognition

Command Structure
text
[action] [target] [additional parameters]
Examples:

open chrome → Action: open, Target: chrome

write machine learning → Action: write, Target: machine learning

create folder work files → Action: create, Target: folder, Parameter: work files

Supported Applications List
The assistant can control these applications:

Browsers: Chrome, Brave, Edge

Development: VS Code

Office Suite: Word, Excel, PowerPoint

System Tools: File Explorer, Calculator, Notepad, Paint

🛠️ Troubleshooting
Common Issues & Solutions
Problem	Solution
"Module not found" error	Run: pip install missing-module-name
"Engine not running" error	Wait a few seconds after startup for engine to load
Commands not recognized	Speak clearly and use exact command formats
Can't close applications	Install psutil: pip install psutil
Microphone not working	Check system microphone permissions
Performance Tips
Close other audio applications when using the assistant

Use a quality microphone for better speech recognition

Keep the assistant window visible to see status updates

Restart the application if you experience issues

🔧 Advanced Features
Customization
You can extend the application by modifying the get_app_process_names() function to add support for more applications.

Technical Details
Speech Recognition: Google Speech-to-API

Audio Processing: 4-second recordings at 44.1kHz

Process Management: Uses Windows task management

GUI Framework: CustomTkinter for modern interface

📋 Command Cheat Sheet
Quick Reference
text
# Applications
"open [app]" / "close [app]"

# Web & Search
"open web [site]" / "write [text]" / "search [query]"

# Files
"create folder [name]" / "open folder [name]"

# Information
"who is [person]" / "what is [topic]" / "how to [task]"
Supported Apps Shortcuts
chrome, brave, edge - Web browsers

vs code - Development

word, excel, powerpoint - Office apps

notepad, calculator, paint - System tools

file explorer - File management

🆘 Support
Getting Help
If you encounter issues:

Check the troubleshooting section above

Ensure all dependencies are installed

Verify your microphone is working

Try speaking more clearly and using exact command formats

Common Error Messages
"Command not recognized" - Use supported command formats

"Application not found" - Application may not be installed

"Error: Engine not running" - Restart the application

📄 License
This project is open source and available for personal and educational use.

Enjoy hands-free computer control! 🎧✨

Tip: Keep this README handy until you memorize the command patterns!

text

This README file includes:

1. **Complete installation instructions**
2. **Detailed command reference** with examples
3. **User interface guide**
4. **Troubleshooting section**
5. **Usage tips and best practices**
6. **Quick reference cheat sheet**
7. **Technical specifications**

The manual is written in clear, user-friendly language with plenty of examples to help users get started quickly!
