import os
import base64
from PIL import Image
import io
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
print("Environment variables loaded.")

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')
print("OpenAI API key set.")

client = OpenAI()

# Directory containing the images
image_directory = 'Your path goes here'
csv_file_path = 'captions.csv'
print(f"Image directory set to {image_directory}")
print(f"CSV will be saved at {csv_file_path}")

# List to hold data
data = []

def resize_and_encode_image(filepath, output_size=(256, 256), quality=70):
    """Resize the image and encode it to base64."""
    print(f"Processing image at {filepath}")
    try:
        with Image.open(filepath) as img:
            print(f"Opened image: {filepath}")
            # Resize the image
            img = img.resize(output_size, Image.LANCZOS)
            print(f"Resized image to {output_size}")
            
            # Save the resized image to a byte buffer with increased compression
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=quality)
            print("Image saved to byte array and compressed.")
            
            # Encode to base64
            encoded_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
            print("Image encoded to base64.")
            return encoded_image
    except Exception as e:
        print(f"Error processing image {filepath}: {e}")
        return None

def generate_caption(base64_image):
    """Generate a caption for the given base64 encoded image using OpenAI's API."""
    print("Generating caption for image.")
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300
        )
        print("Caption received from OpenAI.")
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating caption: {e}")
        return "Caption generation failed"

# Process each file in the directory
try:
    print(f"Starting to process files in directory {image_directory}")
    for filename in os.listdir(image_directory):
        if filename.lower().endswith((".jpg", ".png")):  # Checks for jpg or png files
            file_path = os.path.join(image_directory, filename)
            print(f"Found image file: {filename}")
            image_base64 = resize_and_encode_image(file_path)
            if image_base64:
                caption = generate_caption(image_base64)
                data.append({"file_name": filename, "caption": caption})
            else:
                data.append({"file_name": filename, "caption": "Failed to process image"})
except Exception as e:
    print(f"Error processing directory: {e}")

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
try:
    df.to_csv(csv_file_path, index=False)
    print(f"CSV file has been created at {csv_file_path} with {len(data)} entries.")
except Exception as e:
    print(f"Failed to write CSV file: {e}")
