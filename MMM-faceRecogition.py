import os
import cv2
import numpy as np
import face_recognition as face_rec
import openai
from datetime import datetime
from fpdf import FPDF
import logging
import pickle
import sqlite3

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize text-to-speech engine

#  Set OpenAI API Key
# openai.api_key = "set your key"
def chatgpt_greet(name):
    """Generate a personalized greeting using OpenAI API."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Say hello to {name}"}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error("Error with ChatGPT API: %s", e)
        return f"Hello {name}, welcome!"

def resize(img, scale):
    """Resize the image by a specific scale."""
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

def find_encoding(images):
    """Encode faces in the given list of images."""
    img_encodings = []
    for img in images:
        if img is not None:  # Check if image is valid
            img = resize(img, 0.50)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_rec.face_encodings(img)
            if encodings:  # Ensure encodings exist
                img_encodings.append(encodings[0])
    logging.info("Encodings generated for %d images.", len(img_encodings))
    return img_encodings

def save_encodings_to_file(encodings, names, file_path='encodings.pkl'):
    """Save encodings and names to a file."""
    with open(file_path, 'wb') as f:
        pickle.dump((encodings, names), f)
    logging.info("Encodings saved to file.")

def load_encodings_from_file(file_path='encodings.pkl'):
    """Load encodings and names from a file."""
    with open(file_path, 'rb') as f:
        encodings, names = pickle.load(f)
    logging.info("Encodings loaded from file.")
    return encodings, names

def fetch_images_from_db():
    """Fetch images and names from the database."""
    conn = sqlite3.connect('faces_optimized.db')  # Replace with your database
    cursor = conn.cursor()

    # Example: Assuming a table `faces` with `name` and `encoding` columns
    cursor.execute("SELECT name, image FROM faces")
    data = cursor.fetchall()
    conn.close()

    names = []
    images = []

    for name, img_blob in data:
        names.append(name)
        
        # Decode image from BLOB and check if it's valid
        try:
            img_array = np.frombuffer(img_blob, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is not None:  # Only append if the image is valid
                images.append(img)
                print(f"Image for {name} has shape: {img.shape}")  # Debugging output
            else:
                logging.warning(f"Failed to decode image for {name}")
        except Exception as e:
            logging.error(f"Error processing image for {name}: {e}")

    return names, images

def mark_attendance(name, attendance_buffer):
    """Mark attendance if the name is not already in the buffer."""
    now = datetime.now()
    time_str = now.strftime('%H:%M')
    if name not in attendance_buffer:
        attendance_buffer[name] = time_str
        logging.info("Marked attendance for: %s at %s", name, time_str)
        statement = chatgpt_greet(name)
        # engine.say(statement)

def generate_identity_pdf(name, event, file_path, template_path='idCard.jpg'):
    """Generate a PDF ID card using a pre-designed template."""
    try:
        pdf = FPDF('P', 'mm', (54, 86))  # Standard ID card size
        pdf.add_page()

        # Add the template image as a background
        pdf.image(template_path, x=0, y=0, w=54, h=86)

        # Overlay text onto the template
        pdf.set_font('Arial', 'B', 9)
        pdf.set_text_color(255, 255, 255)  # White text for visibility on darker backgrounds

        # Add Name
        pdf.set_xy(4, 20)  # Adjust coordinates based on your template
        pdf.cell(0, 10, f"Name: {name}", ln=True)

        # Add Event
        pdf.set_xy(4, 30)
        pdf.cell(0, 10, f"Event: {event}", ln=True)

        # Add Date
        pdf.set_xy(4, 40)
        pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

        # Save the PDF
        pdf.output(file_path)
        logging.info("PDF generated and saved to %s", file_path)
    except Exception as e:
        logging.error("Error while generating the PDF: %s", e)

def process_frame(frame, encode_list_known, student_names, attendance_buffer):
    """Process a single frame for face detection and recognition."""
    smaller_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_frame = cv2.cvtColor(smaller_frame, cv2.COLOR_BGR2RGB)

    faces_in_frame = face_rec.face_locations(rgb_frame, model='hog')  # Use GPU-accelerated model if available
    encodings_in_frame = face_rec.face_encodings(rgb_frame, faces_in_frame)

    for encoding, face_location in zip(encodings_in_frame, faces_in_frame):
        matches = face_rec.compare_faces(encode_list_known, encoding)
        face_distances = face_rec.face_distance(encode_list_known, encoding)

        if matches and matches[np.argmin(face_distances)]:
            name = student_names[np.argmin(face_distances)].upper()
            
            # Skip attendance marking if this face has already been recognized
            if name in attendance_buffer:
                continue  # Skip if already marked

            y1, x2, y2, x1 = face_location
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            mark_attendance(name, attendance_buffer)

            # Generate PDF for recognized person
            file_name = f"{name.replace(' ', '_')}_identity_template.pdf"
            generate_identity_pdf(name, "Annual Conference 2025", file_name)

# Check if encodings are already saved; otherwise, fetch and process images
encoding_file = 'encodings.pkl'

# Check if the encodings file exists
if not os.path.exists(encoding_file):
    logging.info("Encodings file not found. Regenerating encodings...")

    # Fetch images and names from the database
    student_names, student_images = fetch_images_from_db()

    # If no images were fetched, log an error and stop the process
    if not student_images:
        logging.error("No images found in the database to generate encodings.")
    else:
        # Generate encodings from the images
        encode_list = find_encoding(student_images)

        # If encodings are successfully generated, save them
        if encode_list:
            save_encodings_to_file(encode_list, student_names, encoding_file)
        else:
            logging.error("Failed to generate encodings for the images.")
else:
    # Load encodings from the file if it exists
    encode_list, student_names = load_encodings_from_file(encoding_file)

# Initialize video capture with lower resolution
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Attendance buffer to temporarily store attendance data
attendance_buffer = {}

frame_count = 0  # To control frame skipping

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Skip every 5 frames to optimize performance
        if frame_count % 5 == 0:
            if 'encode_list' in globals():  # Check if encode_list is defined
                process_frame(frame.copy(), encode_list, student_names, attendance_buffer)
            else:
                logging.error("Encoding list is not defined. Skipping face recognition.")
        frame_count += 1

        # Show the video frame
        cv2.imshow('Video', frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()


