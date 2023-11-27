import openai
import tkinter as tk
from tkinter import PhotoImage, Text
from decouple import config
from getkey import getkey, key
from tkinter.messagebox import askokcancel
from PIL import Image, ImageTk
import threading

#Variables de entorno provenientes de un .env
api_key = config("API_KEY")
system_content = config("SYSTEM_CONTENT")

def chatGpt():
    openai.api_key = api_key
    
    #Contexto del asistente (Lo tomo de una variable de entorno. Es un string que define una tarea o la personalidad que se espera de chatGpt)
    #Ejemplo: SYSTEM_CONTENT = "Eres un asistente muy util y cooperativo"
    messages = [{"role": "system", "content": system_content}]
    
    #Ventana Tkinter
    ventana = tk.Tk()
    ventana.title("ChatGPT Personal")
    ventana.iconbitmap('./images/iconoVentana.ico')
    
    #Etiqueta para mostrar la respuesta
    label = tk.Label(ventana, height=30, width=150,  bg='#161515', anchor='nw', borderwidth=5, relief="solid", wraplength=800)
    label.pack(fill='both', expand=True)
    
    #Función para limpiar el entry
    def borrarPlaceholder(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            
    #Entrada de texto para el prompt
    placeholder_text = "Escriba aquí"
    entry = tk.Entry(ventana, font=' "Calibri" 20 bold italic', bg='#ADB24F', borderwidth=5, relief="solid", justify='left')
    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", borrarPlaceholder)
    entry.pack(fill=tk.X, expand=True, side=tk.LEFT)

    def inputGpt(event):
        prompt = entry.get()
        messages.append({"role": "user", "content": prompt})
        label.config(text="Esperando la respuesta...", background='#4EC844', anchor="center", fg='#FFFFFF')
        hilo = threading.Thread(target=apiRequest, args=(messages))
        hilo.start()

    def apiRequest(*args):
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        del messages[1:]
        response_content = response.choices[0].message.content
        prompt = entry.get()
        messages.append({"role": "user", "content": prompt})
        messages.append({"role": "assistant", "content": response_content})
        mostrarRespuesta(response_content, 0)
        print("Mensajes: ", messages)
        
    def mostrarRespuesta(response_content, index):
        if index < len(response_content):
            label.config(text="Usuario: " + messages[1]["content"] + "\n\n" + response_content[:index + 1], background='#161515', justify='left', anchor='nw', padx=10, fg='#FFFFFF')
            ventana.after(10, mostrarRespuesta, response_content, index + 1)
    
    def cerrarAplicacion(event):
        confirmacion = askokcancel(title='Cerrar Aplicación', message='¿Seguro que deseas cerrar ChatGpt?', icon='question')
        if confirmacion:
            ventana.destroy()
            
    #Botón para enviar el prompt
    iconoBtn = PhotoImage(file="./images/iconoBtn.png", height=50,  width=50)
    btnEnvío = tk.Button(ventana, height=40,  width=40, image=iconoBtn, highlightcolor="#46B4AC", background="#78B446",borderwidth=4, cursor="hand2", command=inputGpt)
    btnEnvío.pack(side=tk.RIGHT)

    #Configuraciones de la ventana (Por ejemplo, eventos y ejecución)
    ventana.bind("<Return>", inputGpt)
    ventana.bind("<Escape>", cerrarAplicacion)
    ventana.mainloop()

if __name__ == "__main__":
    chatGpt()
