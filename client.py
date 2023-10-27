import xmlrpc.client
import base64
import tkinter as tk
from tkinter import filedialog
import os 

root = tk.Tk()
root.withdraw()

def select_image():
    root.wm_attributes('-topmost', 1)
    file_path = filedialog.askopenfilename()
    root.wm_attributes('-topmost', 0)
    if file_path:
        return file_path
    return None

def save_image(data, image_name):
    with open(image_name, "wb") as f:
        f.write(base64.b64decode(data))

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        os.system('cls')
        print("Escolha uma operação:")
        print("1. Grayscale")
        print("2. Redimensionar")
        print("3. Rotacionar")
        print("4. Consultar Status da Tarefa")
        print("0. Sair")
        choice = input("Opção: ")

        if choice == '0':
            break

        if choice in ['1', '2', '3']:
            image_path = select_image()
            if image_path:
                with open(image_path, "rb") as f:
                    encoded_image_data = base64.b64encode(f.read()).decode('utf-8')

                if choice == '1':
                    operation = 'grayscale'
                    task_id = proxy.create_image_processing_task(encoded_image_data, operation)
                elif choice == '2':
                    operation = 'resize'
                    width = int(input("Nova largura: "))
                    height = int(input("Nova altura: "))
                    task_id = proxy.create_image_processing_task(encoded_image_data, operation, width, height)
                elif choice == '3':
                    operation = 'rotate'
                    angle = float(input("Ângulo de rotação (em graus): "))
                    task_id = proxy.create_image_processing_task(encoded_image_data, operation, angle)

                print(f"Tarefa de processamento de imagem criada. ID da tarefa: {task_id}")

                input("Pressione 'Enter' para continuar para o menu")
            else:
                print("O arquivo de imagem não foi encontrado.")
        elif choice == '4':
            task_id = input("Digite o ID da tarefa: ")
            task_info = proxy.get_task_status(int(task_id))

            if task_info['status'] == 'completed':
                result_data = task_info['result']
                image_name = f"processed_image_{task_id}.jpg"
                save_image(result_data, image_name)
                print(f"Operação concluída. Imagem processada salva como '{image_name}'.")
            elif task_info['status'] == 'processing':
                print("A tarefa está em andamento.")
            elif task_info['status'] == 'not_found':
                print("Tarefa não encontrada.")

            input("Pressione 'Enter' para continuar para o menu")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
