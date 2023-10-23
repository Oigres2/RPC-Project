import xmlrpc.client
import base64


proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

with open("w.jpg", "rb") as f:
    encoded_image_data = base64.b64encode(f.read()).decode('utf-8')

processed_image_data = proxy.convert_to_grayscale(encoded_image_data)

with open("processed_image.jpg", "wb") as f:
    f.write(base64.b64decode(processed_image_data))
