import sqlite3
import os
import cv2
import numpy as np
import sys
import pickle
import base64

# Ensure UTF-8 encoding for Windows console (if needed)
sys.stdout.reconfigure(encoding='utf-8')

# Function to create the database and table
def create_database(db_name='faces_optimized.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Database '{db_name}' and 'faces' table created.")

# Function to insert an image and Arabic name into the database
def insert_image(db_name='faces_optimized.db', name='', image_path=''):
    image_path = os.path.abspath(image_path)
    try:
        image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"❌ Error loading image '{image_path}': {e}")
        return

    if image is None:
        print(f"❌ Error: Image '{image_path}' not found or not supported by OpenCV.")
        return

    _, img_encoded = cv2.imencode('.jpg', image)
    img_blob = img_encoded.tobytes()

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO faces (name, image) VALUES (?, ?)", (name, img_blob))
    conn.commit()
    conn.close()
    print(f"✅ Inserted '{name}' into database.")

# Function to fetch and encode data into .pkl format
def fetch_and_encode_pkl(db_name='faces_optimized.db', output_file='encodings.pkl'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Make sure the table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS faces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image BLOB NOT NULL
        )
    """)

    cursor.execute("SELECT name, image FROM faces")
    data = cursor.fetchall()
    conn.close()

    packed_data = []
    for name, img_blob in data:
        name_utf8 = name.strip()
        img_base64 = base64.b64encode(img_blob).decode("utf-8")
        packed_data.append({"name": name_utf8, "image": img_base64})

    with open(output_file, "wb") as file:
        pickle.dump(packed_data, file)

    print(f"✅ .pkl file '{output_file}' generated successfully.")

# Main execution
if __name__ == "__main__":
    db_name = 'faces_optimized.db'
    image_folder = os.path.abspath("D:/projects/chatGPT/MMM-FaceRecognition/images")

    # Step 1: Create DB and Table
    create_database(db_name=db_name)

    # Step 2: Check and load images from folder
    if not os.path.exists(image_folder):
        print(f"❌ Folder not found: {image_folder}")
        sys.exit(1)

    image_files = os.listdir(image_folder)
    if not image_files:
        print("⚠️ No images found in the folder.")
        sys.exit(1)

    print("📝 Images found:", image_files)

    for img_name in image_files:
        print(f"🔹 Processing: {repr(img_name)}")
        img_name = img_name.encode('utf-8').decode('utf-8', 'ignore')
        img_path = os.path.join(image_folder, img_name)
        student_name = os.path.splitext(img_name)[0]
        insert_image(db_name=db_name, name=student_name, image_path=img_path)

    # Step 3: Fetch and save to pkl
    fetch_and_encode_pkl(db_name=db_name, output_file='encodings.pkl')
