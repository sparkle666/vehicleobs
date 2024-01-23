import requests
import asyncio
import aiohttp


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

# async def upload_image_async(file_path):
#     try:
#         endpoint_url = "https://vehicleobs.onrender.com/api/v1/upload/"
#         # endpoint_url = "http://localhost:8000/api/v1/upload/"

#         async with aiohttp.ClientSession() as session:
#             files = {'image': open(file_path, 'rb')}
#             print(f"All Files: {files}")
#             async with session.post(endpoint_url, data={}, files=files) as response:
#                 if response.status == 200:
#                     print("Image uploaded successfully!")
#                     print(await response.text())
#                 else:
#                     print(f"Failed to upload image. Status code: {response.status}")
#     except Exception as e:
#         print(f"Error: {e}")


async def upload_image_async(file_path):
    try:
        endpoint_url = "https://vehicleobs.onrender.com/api/v1/upload/"
        # endpoint_url = "http://localhost:8000/api/v1/upload/"

        async with aiohttp.ClientSession() as session:
            files = {'image': open(file_path, 'rb')}
            print(f"All Files: {files}")

            form = aiohttp.FormData()
            form.add_field('image', files['image'])

            async with session.post(endpoint_url, data=form) as response:
                if response.ok:
                    print("Image uploaded successfully!")
                    print(await response.text())
                else:
                    print(
                        f"Failed to upload image. Status code: {response.status}")
    except Exception as e:
        print(f"Error: {e}")
