import xmlrpc.server
from PIL import Image
import base64
from io import BytesIO

def convert_to_grayscale(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    image = image.convert('L')  # Convert to grayscale
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def resize_image(encoded_image, width, height):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    image = image.resize((width, height), Image.LANCZOS)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def rotate_image(encoded_image, angle):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    rotated_image = image.rotate(angle)
    buffered = BytesIO()
    rotated_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")
server.register_function(convert_to_grayscale, "convert_to_grayscale")
server.register_function(resize_image, "resize_image")
server.register_function(rotate_image, "rotate_image")
server.serve_forever()
