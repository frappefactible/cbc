import tkinter as tk
from PIL import Image, ImageTk, ExifTags
import os
import time
from tkinter import messagebox #para crear una ventana nueva
from tkinter import ttk
import webbrowser

# Crear la ventana principal
root = tk.Tk()
root.title("CABA")

#---------------------------------
# Crear un Canvas y un Scrollbar
canvas = tk.Canvas(root, width=700, height=500, bg="white")
scrollbar = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

# Configurar el Canvas para que use el Scrollbar
canvas.configure(xscrollcommand=scrollbar.set)

# Colocar el Canvas y el Scrollbar en la ventana
scrollbar.pack(side="bottom", fill="x")
canvas.pack(side="bottom", fill="both", expand=True)

# Crear un marco dentro del Canvas para contener los botones
frame = tk.Frame(canvas)

# Añadir el marco al Canvas
canvas.create_window((0, 0), window=frame, anchor="nw")

# Función para actualizar el área de desplazamiento del Canvas
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

# Vincular el evento <Configure> del marco a la función update_scrollregion
frame.bind("<Configure>", update_scrollregion)

#---------------------------------

# Crear un frame para la caja de herramientas
toolbox = tk.Frame(root)
toolbox.pack(side="top", anchor="nw")

# Crear los botones de la caja de herramientas
new_button = tk.Button(toolbox, text="Nuevo")
new_button.pack(side="left")

about_button = tk.Button(toolbox, text="Acerca de")
about_button.pack(side="left")

# Crear un botón que redirige a tu perfil de GitHub
def open_github():
    webbrowser.open("https://github.com/frappefactible")

github_button = tk.Button(toolbox, text="GitHub", command=open_github)
github_button.pack(side="left")

#-------------------------

# Crear las imágenes
image1 = Image.open("ISIC_0024306.jpeg")
image2 = Image.open("ISIC_0024307.jpeg")
image3 = Image.open("ISIC_0024308.jpeg")
image4 = Image.open("ISIC_0024309.jpeg")

# Crear los objetos ImageTk
photo1 = ImageTk.PhotoImage(image1)
photo2 = ImageTk.PhotoImage(image2)
photo3 = ImageTk.PhotoImage(image3)
photo4 = ImageTk.PhotoImage(image4)

# Crear un label para mostrar la información
info_label = ttk.Label(root)
info_label.pack(side="bottom")

# Función para mostrar información
def show_info(event, name, date, patient):
    info = f"Nombre: {name}\nFecha: {date}\nPaciente: {patient}"
    info_label.config(text=info)
# Función para ocultar información
def hide_info(event):
    info_label.config(text="")

# Función para mostrar metadatos
def show_metadata(event, image_path, photo):
    # Crear una nueva ventana
    new_window = tk.Toplevel(root)

    # Mostrar la imagen en la nueva ventana
    image_label = tk.Label(new_window, image=photo)
    image_label.image = photo  # Guardar una referencia a la imagen
    image_label.pack()

    # Obtener el tamaño del archivo en bytes
    file_size = os.path.getsize(image_path)

    # Abrir la imagen y obtener su resolución
    image = Image.open(image_path)
    resolution = image.size  # (ancho, alto)

    # Obtener la fecha de creación del archivo
    creation_time = os.path.getctime(image_path)
    creation_date = time.ctime(creation_time)

    # Crear un label para mostrar los metadatos
    metadata_label = tk.Label(new_window, text=f"Tamaño del archivo: {file_size} bytes\nResolución: {resolution[0]} x {resolution[1]}\nFecha de creación: {creation_date}\n\n - Prueba de algoritmo KNN\nPrecisión: x\nExactitud: x\nRecall: x\nF1 Score: x ")
    metadata_label.pack()

#Creación de ventana pequeña de informacion
#def show_info(event, name, date, patient):
#    info = f"Nombre: {name}\nFecha: {date}\nPaciente: {patient}"
#    messagebox.showinfo("Información", info)

# Crear los botones y asignarles las imágenes
button1 = tk.Button(frame, image=photo1)
button1.bind("<Enter>", lambda event: show_info(event, "ISIC_0024306.jpeg", "Fecha1", "Paciente1"))
button1.bind("<Leave>", hide_info)
button1.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024306.jpeg", photo1))
button2 = tk.Button(frame, image=photo2)
button2.bind("<Enter>", lambda event: show_info(event, "ISIC_0024307.jpeg", "Fecha2", "Paciente2"))
button2.bind("<Leave>", hide_info)
button2.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024307.jpeg", photo2))
button3 = tk.Button(frame, image=photo3)
button3.bind("<Enter>", lambda event: show_info(event, "ISIC_0024308.jpeg", "Fecha3", "Paciente3"))
button3.bind("<Leave>", hide_info)
button3.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024308.jpeg", photo3))
button4 = tk.Button(frame, image=photo4)
button4.bind("<Enter>", lambda event: show_info(event, "ISIC_0024309.jpeg", "Fecha4", "Paciente4"))
button4.bind("<Leave>", hide_info)
button4.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024309.jpeg", photo4))

# Crear los botones y asignarles las imágenes
#button1 = tk.Button(root, image=photo1)
#button1.bind("<Enter>", lambda event: show_info(event, "ISIC_0024306.jpg", "Fecha1", "Paciente1"))
#button2 = tk.Button(root, image=photo2)
#button2.bind("<Enter>", lambda event: show_info(event, "ISIC_0024307.jpg", "Fecha2", "Paciente2"))
#button3 = tk.Button(root, image=photo3)
#button3.bind("<Enter>", lambda event: show_info(event, "ISIC_0024308.jpg", "Fecha3", "Paciente3"))

# Mostrar los botones en la ventana
button1.pack(side="left")
button2.pack(side="left")
button3.pack(side="left")
button4.pack(side="left")

# Mostrar la ventana y esperar a que el usuario interactúe con ella
root.mainloop()
