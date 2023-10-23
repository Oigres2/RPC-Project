import xmlrpc.client
import base64
import tkinter as tk
from tkinter import filedialog

def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    return None

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        print("Escolha uma operação:")
        print("1. Grayscale")
        print("2. Redimensionar")
        print("3. Rotacionar")
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
                    task_id = proxy.create_image_processing_task(encoded_image_data, 'grayscale')
                elif choice == '2':
                    width = int(input("Nova largura: "))
                    height = int(input("Nova altura: "))
                    task_id = proxy.create_image_processing_task(encoded_image_data, 'resize', width, height)
                elif choice == '3':
                    angle = float(input("Ângulo de rotação (em graus): "))
                    task_id = proxy.create_image_processing_task(encoded_image_data, 'rotate', angle)

                print("Tarefa criada com ID:", task_id)

                while True:
                    task_status = proxy.get_task_status(task_id)
                    status = task_status.get('status', 'unknown')
                    if status == 'completed':
                        result = task_status.get('result', '')
                        if result:
                            with open("processed_image.jpg", "wb") as f:
                                f.write(base64.b64decode(result))
                            print("Tarefa concluída. Imagem processada salva como 'processed_image.jpg'.")
                        break
                    elif status == 'error':
                        print("Erro:", task_status.get('result', 'Erro desconhecido'))
                        break
            else:
                print("O arquivo de imagem não foi encontrado.")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Esconder a janela principal do Tkinter
    main()
