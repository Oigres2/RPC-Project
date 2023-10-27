import xmlrpc.server
import base64
from PIL import Image
from io import BytesIO
import queue
import threading
from concurrent.futures import ThreadPoolExecutor


TASKS = {}
task_queue = queue.Queue()

thread_pool = ThreadPoolExecutor(max_workers=100)

def create_image_processing_task(encoded_image, operation, *args):
    task_id = len(TASKS) + 1
    TASKS[task_id] = {'status': 'A processar'}

    task_queue.put((task_id, encoded_image, operation, args))

    return task_id

def process_image():
    while True:
        task_id, encoded_image, operation, args = task_queue.get()
        decoded_image = base64.b64decode(encoded_image)
        image = Image.open(BytesIO(decoded_image))

        if operation == 'grayscale':
            image = image.convert('L')
        elif operation == 'resize':
            width, height = args
            image = image.resize((width, height), Image.LANCZOS)
        elif operation == 'rotate':
            angle = args[0]
            image = image.rotate(angle)

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        processed_image_data = base64.b64encode(buffered.getvalue()).decode('utf-8')

        TASKS[task_id]['status'] = 'Finalizado'
        TASKS[task_id]['result'] = processed_image_data

        task_queue.task_done()

def get_task_status(task_id):
    if task_id in TASKS:
        return TASKS[task_id]
    else:
        return {'status': 'Não Encontrado'}

processing_thread = threading.Thread(target=process_image)
processing_thread.daemon = True
processing_thread.start()

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Listening on port 8000...")

server.register_function(create_image_processing_task, "create_image_processing_task")
server.register_function(get_task_status, "get_task_status")

server.serve_forever()
