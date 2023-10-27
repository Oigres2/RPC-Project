import xmlrpc.client
import base64
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from io import BytesIO
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

def save_image(data, operation, image_name):
    with open(f"{image_name}_{operation}.jpg", "wb") as f:
        f.write(base64.b64decode(data))

def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

    while True:
        os.system('cls')
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
                    result = proxy.convert_to_grayscale(encoded_image_data)
                    operation = 'grayscale'
                elif choice == '2':
                    width = int(input("Nova largura: "))
                    height = int(input("Nova altura: "))
                    result = proxy.resize_image(encoded_image_data, width, height)
                    operation = 'resize'
                elif choice == '3':
                    angle = float(input("Ângulo de rotação (em graus): "))
                    result = proxy.rotate_image(encoded_image_data, angle)
                    operation = 'rotate'

                if result:
                    save_image(result, operation, image_path.split('.')[0])
                    print(f"Operação concluída. Imagem processada salva como '{image_path.split('.')[0]}_{operation}.jpg'.")
                    input("Pressione 'Enter' para continuar para o menu")
                else:
                    print("Ocorreu um erro durante o processamento.")
            else:
                print("O arquivo de imagem não foi encontrado.")
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()