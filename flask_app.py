from flask import Flask, request, jsonify, render_template, Response
import numpy as np
from PIL import Image
import torch, time, os, zipfile, json, base64
from flask_sse import sse
from io import BytesIO
from modifiers import apply_modifiers

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_dataset():
    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Extract the zip file
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(UPLOAD_FOLDER)

    extracted_files = []
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            extracted_files.append(os.path.relpath(os.path.join(root, file), UPLOAD_FOLDER))

    # Load images as Numpy array
    image_files = sorted([f for f in extracted_files if f.endswith('.png') or f.endswith('.jpg')])

    if not image_files:
        return jsonify({"error": "No images found in the uploaded ZIP file"}), 400

    images = []
    for img_file in image_files:
        img_path = os.path.join(UPLOAD_FOLDER, img_file)
        img = Image.open(img_path).convert('RGB')
        img = np.array(img)
        images.append(img)

    if not images:
        return jsonify({"error": "Failed to load images"}), 500

    images_array = np.array(images)

    # Save the array to a .npy file
    np.save(os.path.join(PROCESSED_FOLDER, 'images.npy'), images_array)

    return jsonify({"message": "Dataset uploaded successfully"})


@app.route('/delete_dataset', methods=['POST'])
def delete_dataset():
    # Delete files in the upload and processed folders
    for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                os.remove(file_path)
            except Exception as e:
                return jsonify({"error": f"Error deleting file {file_path}: {str(e)}"})

    return jsonify({"message": "Dataset and processed files deleted successfully"})



def encode_image(image_tensor):
    image_array = image_tensor.numpy().astype(np.uint8)  # Convert tensor to uint8
    image = Image.fromarray(image_array)  # Create a PIL image
    buffer = BytesIO()  # Create an in-memory buffer
    image.save(buffer, format="PNG")  # Save the image in PNG format to the buffer
    buffer.seek(0)  # Move to the beginning of the buffer
    return base64.b64encode(buffer.read()).decode('utf-8')  # Encode to Base64

@app.route('/simulate', methods=['GET'])
def simulate():
    modifiers = request.args.get('modifiers', default='{}')
    modifiers = json.loads(modifiers)

    def generate(modifiers):
        data = np.load(os.path.join(PROCESSED_FOLDER, 'images.npy'))
        data = torch.tensor(data, dtype=torch.float32)
        print("Data shape:", data.shape)

        for i in range(data.shape[0]):
            original_image = encode_image((data[i] * 255).byte())
            modified_image = encode_image((apply_modifiers(data[i], modifiers) * 255).byte())
            print(f"Sending image {i}")
            
            yield f"data: {json.dumps({'original_image': original_image, 'modified_image': modified_image})}\n\n"
            #time.sleep(0.1)

    return Response(generate(modifiers), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run()
