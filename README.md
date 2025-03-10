# Drift Detection Simulator

This project is a Drift Detection Simulator built using Flask. It allows users to upload a dataset of images, apply various noise and drift modifiers, and visualize the effects on the images.

## Project Structure
MLOps-web-interface
- processed (if not present then generated automatically)
- - images.zip (processed dataset)
- uploads (if not present then generated automatically)
- - images.zip (uploaded dataset)
- templates
- - index.html
- flask_app.py
- modifiers.py
- deploy-flask-app.sh (bash script for cluster)
- requirements.txt


## Requirements

- Python 3.8+
- Docker (for deployment)
- Kubernetes (for deployment)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. Start the Flask application:
    ```sh
    python flask_app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

## Usage

### Upload Dataset

1. Click on the "Select Dataset" button and choose a ZIP file containing your image dataset.
2. Click on the "Upload Dataset" button to upload and extract the images.

### Apply Modifiers

1. Select the modifiers you want to apply (e.g., Gaussian Noise, Shot Noise, etc.).
2. Click on the "Apply Modifiers and Simulate" button to apply the selected modifiers and visualize the results.

### Delete Dataset

1. Click on the "Delete Dataset" button to delete the uploaded dataset and processed files.

## Deployment

### Using Docker and Kubernetes

1. Ensure Docker and Kubernetes are installed and configured on your machine.

2. Run the deployment script:
    ```sh
    ./deploy-flask-app.sh
    ```

This script will:
- Log in to Docker Hub
- Build and push the Docker image
- Apply Kubernetes configurations for Persistent Volume, Persistent Volume Claim, Deployment, and Service
- Wait for the pod to be ready and fetch logs

## Files

- [flask_app.py]: Main Flask application file.
- [modifiers.py]: Contains functions to apply various noise and drift modifiers to the images.
- [index.html]: Main HTML template for the web interface.
- [requirements.txt]: List of Python dependencies.
- [deploy-flask-app.sh]: Shell script to deploy the Flask app to Kubernetes using Docker and kubectl.

## License

This project is licensed under the MIT License.
