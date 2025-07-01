# MMM-FaceRecognition for MagicMirror²

**MMM-FaceRecognition** is a face recognition module designed for [MagicMirror²](https://magicmirror.builders/), developed by me and my friend. It enables MagicMirror to recognize faces, display personalized messages using OpenAI's ChatGPT, and supports both Arabic and English languages. Additionally, the project includes voice output powered by Amazon Polly.

## 🧠 Features

- 🔒 Accurate face detection and recognition using Python and `face_recognition` library.
- 💬 Personalized greetings generated via OpenAI ChatGPT.
- 🗣️ Supports speech output using Amazon Polly.
- 🌐 Arabic and English language support.
- 🪪 Automatic PDF ID generation for recognized individuals.
- 🖥️ Simple front-end integration with MagicMirror².
- 🗃️ Uses SQLite database to manage stored faces.

## 🛠️ Project Structure


```
MMM-FaceRecognition/
│
├── MMM-FaceRecognition.js 
├── MMM-faceRecogition.py 
└── Other necessary assets 
```
## 🚀 How It Works

1. The Python backend detects and recognizes faces through the webcam.
2. When a face is recognized:
   - ChatGPT generates a personalized greeting.
   - A PDF identity card is generated.
   - (Optional) Amazon Polly converts the greeting to speech.
3. The MagicMirror module displays a message and shows alerts for recognized individuals.

## 🧩 Requirements

- MagicMirror² platform
- Python 3.x
- Required Python packages:
  - `opencv-python`
  - `face_recognition`
  - `numpy`
  - `openai`
  - `fpdf`
  - `sqlite3`
- Amazon Polly credentials (optional)
- OpenAI API key (optional for ChatGPT features)

## 🌍 Language Support

- ✅ Arabic
- ✅ English

## ⚒️ Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
