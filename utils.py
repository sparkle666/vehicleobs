import requests

def upload_image(file_path):
    endpoint_url = "https://vehicleobs.onrender.com/api/v1/upload/"
    # endpoint_url = "http://localhost:8000/api/v1/upload/"

    try:
        with open(file_path, 'rb') as file:
            files = {'image': file}
            print(f"All Files: {files}")
            response = requests.post(endpoint_url, files=files)

            if response.ok:
                print("Image uploaded successfully!")
                print(response.json())
            else:
                print(
                    f"Failed to upload image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
