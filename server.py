import xmlrpc.server
from PIL import Image, ImageFilter
import base64
from io import BytesIO
import threading

TASKS = {}

def convert_to_grayscale(encoded_image):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image)).convert('L')
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def resize_image(encoded_image, width, height):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    image = image.resize((width, height), Image.ANTIALIAS)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def rotate_image(encoded_image, angle):
    decoded_image = base64.b64decode(encoded_image)
    image = Image.open(BytesIO(decoded_image))
    image = image.rotate(angle)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def create_image_processing_task(encoded_image, operation, *args):
    task_id = len(TASKS) + 1
    TASKS[task_id] = {'status': 'processing'}
    threading.Thread(target=process_image, args=(task_id, encoded_image, operation, *args)).start()
    return task_id

def process_image(task_id, encoded_image, operation, *args):
    if operation == 'grayscale':
        result = convert_to_grayscale(encoded_image)
    elif operation == 'resize':
        result = resize_image(encoded_image, *args)
    elif operation == 'rotate':
        result = rotate_image(encoded_image, *args)
    TASKS[task_id]['status'] = 'completed'
    TASKS[task_id]['result'] = result

def get_task_status(task_id):
    task = TASKS.get(task_id, {})
    return task

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")
server.register_function(convert_to_grayscale, "convert_to_grayscale")
server.register_function(resize_image, "resize_image")
server.register_function(rotate_image, "rotate_image")
server.register_function(create_image_processing_task, "create_image_processing_task")
server.register_function(get_task_status, "get_task_status")
server.serve_forever()
