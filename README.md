# MMM-FaceRecognition

**Face Recognition Module for MagicMirror²**

MMM-FaceRecognition is a smart face recognition module for [MagicMirror²](https://magicmirror.builders/) that allows your MagicMirror to recognize faces, greet users with personalized messages using ChatGPT, generate ID cards, and even provide voice feedback via Amazon Polly.

This module supports both Arabic and English, making it ideal for multi-lingual smart mirrors.


## 📦 Installation

Assuming you're inside your MagicMirror directory, run the following commands:

```
cd modules
git clone https://github.com/eyad6789/MMM-FaceRecognition.git
You will also need to set up the Python backend for face detection and recognition (see below).
```
## ⚙️ Requirements
- MagicMirror²
- Python 3.x

### Required Python packages:
- opencv-python
- face_recognition
- numpy
- openai
- fpdf
- sqlite3
- OpenAI API Key (optional for ChatGPT greetings) 
- Amazon Polly credentials (optional for voice support)
- A connected webcam

## 🖥️ Raspberry Pi Notes
The module has been tested on Raspberry Pi with a standard USB webcam.
For Raspberry Pi Camera support, make sure to enable the legacy camera mode:
```
sudo raspi-config
Then navigate to:
```
```
3 Interface Options -> I1 Legacy Camera -> Enable
```
## 🗂️ Project Structure
```
MMM-FaceRecognition/
│
├── MMM-FaceRecognition.js   
├── MMM-faceRecogition.py    
├── faces_optimized.db        
├── idCard.jpg                
└── Other supporting assets
```
## ⚒️ Configuration
To use this module, add it to the modules array in your config/config.js file:

```
modules: [
  {
    module: "MMM-FaceRecognition",
    position: "top_left", // Optional: Position for debug information
    config: {
      recognizedMessage: "Hello, ", // Message prefix when a face is recognized
      updateInterval: 10000          // Time between UI updates in ms
    }
  }
];
```
### Configuration Options: 
| Option              | Description                              | Default     |
| ------------------- | ---------------------------------------- | ----------- |
| `recognizedMessage` | Message prefix when a face is recognized | `"Hello, "` |
| `updateInterval`    | Time in milliseconds between UI updates  | `10000`     |


🚀 How It Works
The Python backend continuously processes webcam frames to detect and recognize faces.

When a known face is detected:

A greeting message is generated using ChatGPT.

An ID card in PDF format is generated automatically.

(Optional) Amazon Polly speaks the greeting aloud.

The MagicMirror module displays the recognition message and shows alerts.

🌐 Language Support
✅ Arabic

✅ English

🔑 API Integration
ChatGPT: Requires an OpenAI API key for generating dynamic greeting messages.

Amazon Polly (Optional): For speech output; AWS credentials required.

🗃️ Database
Face data is managed using an SQLite database (faces_optimized.db). You can store images and names which the system uses for recognition.

🧪 Tested Devices
Standard USB webcams

Raspberry Pi Camera (with legacy mode enabled)

📢 Notifications Sent
Notification	Payload	Description
FACE_RECOGNIZED	{ name }	Sent when a known face is recognized

🗒️ Changelog
[1.0.0] - 2025-07-01

Initial release with:

Face recognition using Python and face_recognition

MagicMirror integration

ChatGPT greetings

ID card PDF generation

Optional voice support via Amazon Polly

🙏 Acknowledgements
Special thanks to:

OpenAI for ChatGPT API

Amazon for Polly TTS

The MagicMirror² community for the awesome platform

