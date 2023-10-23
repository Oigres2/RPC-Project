import xmlrpc.server
from PIL import Image
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
    rotated_image = image.rotate(angle)
    buffered = BytesIO()
    rotated_image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def create_image_processing_task(encoded_image, operation, *args):
    task_id = len(TASKS) + 1
    TASKS[task_id] = {'status': 'processing'}
    threading.Thread(target=process_image, args=(task_id, encoded_image, operation, *args)).start()
    return task_id

def process_image(task_id, encoded_image, operation, *args):
    try:
        if operation == 'grayscale':
            result = convert_to_grayscale(encoded_image)
        elif operation == 'resize':
            result = resize_image(encoded_image, *args)
        elif operation == 'rotate':
            result = rotate_image(encoded_image, *args)
        else:
            TASKS[task_id]['status'] = 'error'
            TASKS[task_id]['result'] = 'Operação não suportada'
            return

        TASKS[task_id]['status'] = 'completed'
        TASKS[task_id]['result'] = result
    except Exception as e:
        TASKS[task_id]['status'] = 'error'
        TASKS[task_id]['result'] = str(e)

def get_task_status(task_id):
    task = TASKS.get(task_id, {})
    return task

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")
server.register_function(create_image_processing_task, "create_image_processing_task")
server.register_function(get_task_status, "get_task_status")
server.serve_forever()
