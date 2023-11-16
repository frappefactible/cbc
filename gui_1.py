import tkinter as tk
from PIL import Image, ImageTk, ExifTags
import os
import time
from tkinter import messagebox #para crear una ventana nueva
from tkinter import ttk
from tkinter import filedialog, Menu, messagebox
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import requests
import tkinter as tk
from tkinter import simpledialog

# Crear la ventana principal
root = tk.Tk()
root.title("CABA v0.1.0")

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
new_button = tk.Button(toolbox, text="Nuevo", font=("Arial", 12, "bold"), fg="green")
new_button.pack(side="left")


# Definir las funciones para cada opción del menú
def upload_file():
    filename = filedialog.askopenfilename()
    # Aquí puedes añadir el código para manejar el archivo

def import_file():
    filename = filedialog.askopenfilename()
    # Aquí puedes añadir el código para importar el archivo

def export_file():
    filename = filedialog.asksaveasfilename()
    # Aquí puedes añadir el código para exportar el archivo

def open_settings():
    messagebox.showinfo("Configuración", "Aquí puedes abrir la ventana de configuración")

def exit_app():
    root.quit()



# Crear el menú desplegable
menu = Menu(root, tearoff=0)
menu.add_command(label="Subir archivo", command=upload_file)
menu.add_command(label="Importar", command=import_file)
menu.add_command(label="Exportar", command=export_file)
menu.add_command(label="Configuración", command=open_settings)
menu.add_command(label="Salir", command=exit_app)

# Asociar el menú desplegable con el botón "Nuevo"
new_button.bind("<Button-1>", lambda event: menu.post(new_button.winfo_rootx(), new_button.winfo_rooty() + new_button.winfo_height()))
#event.x_root, event.y_root

#---------------------------

def about_us():
    messagebox.showinfo("Software CABA", "Este software fue creado por estudiantes de la UPC para el proyecto CABA. \nSe espera seguir desarrollando el proyecto para que presente mayor número de funciones y caracteristicas. Así como tambien resolver errores, lograr la optimizacion y la adhesion de nuestra red neuronal (en proceso) completamente funcional. \nVersión: 0.1.0 \nFecha: 16/11/2020 \nAutor: Factible Data \nContacto: factiblesoftwarecaba@gmail.com")
about_button = tk.Button(toolbox, text="Acerca de", font=("Arial", 12, "bold"), fg="blue", command=about_us)
about_button.pack(side="left")

# Crear un botón que redirige a tu perfil de GitHub
def open_github():
    webbrowser.open("https://github.com/frappefactible")

github_button = tk.Button(toolbox, text="GitHub", font=("Arial", 12, "bold"), fg="black", command=open_github)
github_button.pack(side="left")


#---------------------------
# Nueva función y botón... agregando correo

def open_email_window():
    email_window = tk.Toplevel()
    email_window.title("CABA: Enviar correo")
    email_window.geometry("300x170")  # Ajusta el tamaño de la ventana a 300px de ancho y 170px de alto

    tk.Label(email_window, text="Introduce tu nombre:", font=("Arial", 14)).pack()
    name_entry = tk.Entry(email_window, font=("Arial", 14))
    name_entry.pack()

    tk.Label(email_window, text="Introduce tu correo electrónico:", font=("Arial", 14)).pack()
    email_entry = tk.Entry(email_window, font=("Arial", 14))
    email_entry.pack()

    send_button = tk.Button(email_window, text="Enviar", font=("Arial", 14), command=lambda: send_email(email_entry.get(), name_entry.get()))
    send_button.pack(pady=15)  # Agrega un espacio de separación de 10px arriba y abajo del botón

def send_email(receiver_email, user_name):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "factiblesoftwarecaba@gmail.com"
    sender_password = "mogjhuwgbeqbwcef"
    #receiver_email = "justicephantombass@gmail.com"
    #"diro581220@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Correo de bienvenida al software CABA"

    body = f"¡Hola {user_name}! \n[Si puedes leer este correo es porque eres asombroso!] \nBienvenido al software CABA, \nAgradecemos tu confianza en Factible Data y esperamos poder ofrecerte soluciones innovadoras y confiables."
    msg.attach(MIMEText(body, 'plain'))

    # Muestra un cuadro de diálogo de información después de enviar el correo electrónico
    messagebox.showinfo("Información", "Correo enviado")

    # Descargar y adjuntar la imagen
    image_url = "https://64.media.tumblr.com/d176ee10668fd22bf6189cb59d57a3a2/505d6502a1cbfe5e-39/s1280x1920/1c92bb401e01841e23157b5204c6817b53f860e3.gifv"
    response = requests.get(image_url)
    img = MIMEImage(response.content)
    msg.attach(img)

    # Adjuntar la imagen
    #with open("path_to_your_image.jpg", 'rb') as f:
    #    img = MIMEImage(f.read())
    #msg.attach(img)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)

    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    server.quit()


email_button = tk.Button(toolbox, text="Enviar correo", font=("Arial", 12, "bold"), fg="red", command=open_email_window)
email_button.pack(side="left")
#email_button = tk.Button(toolbox, text="Enviar correo", font=("Arial", 12, "bold"), fg="red", command=send_email)
#email_button.pack(side="left")

#---------------------------


#-------------------------

# Pendiente 16/11/2023
# Crear una lista para almacenar las imágenes
image_list = []

# Crear un frame para los botones de categoría
category_frame = tk.Frame(root)
category_frame.pack(side="top", fill="x")

# Crear un frame para las imágenes
image_frame = tk.Frame(root)
image_frame.pack(fill="both", expand=True)

def load_image_gallery(category):
    # Asegúrate de eliminar cualquier imagen anterior de la lista
    image_list.clear()
    # Eliminar cualquier imagen anterior del frame de las imágenes
    for widget in image_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()
    if category == "Categoría 1":
        image1 = Image.open("ISIC_0024306.jpg")
        image2 = Image.open("ISIC_0024307.jpg")

        photo1 = ImageTk.PhotoImage(image1)
        photo2 = ImageTk.PhotoImage(image2)

        # Guardar las imágenes en la lista
        image_list.append(photo1)
        image_list.append(photo2)

        button1 = tk.Button(image_frame, image=photo1)
        button1.bind("<Enter>", lambda event: show_info(event, "ISIC_0024306.jpg", "Fecha1", "Paciente1"))
        button1.bind("<Leave>", hide_info)
        button1.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024306.jpg", photo1))
        button1.pack(side="left")

        button2 = tk.Button(image_frame, image=photo2)
        button2.bind("<Enter>", lambda event: show_info(event, "ISIC_0024307.jpg", "Fecha2", "Paciente2"))
        button2.bind("<Leave>", hide_info)
        button2.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024307.jpg", photo2))
        button2.pack(side="left")

    elif category == "Categoría 2":
        image3 = Image.open("ISIC_0024308.jpg")
        image4 = Image.open("ISIC_0024309.jpg")
        image5 = Image.open("F8ew2v5WQAARCWc.png")

        photo3 = ImageTk.PhotoImage(image3)
        photo4 = ImageTk.PhotoImage(image4)
        photo5 = ImageTk.PhotoImage(image5)

        # Guardar las imágenes en la lista
        image_list.append(photo3)
        image_list.append(photo4)
        image_list.append(photo5)

        button3 = tk.Button(image_frame, image=photo3)
        button3.bind("<Enter>", lambda event: show_info(event, "ISIC_0024308.jpg", "Fecha3", "Paciente3"))
        button3.bind("<Leave>", hide_info)
        button3.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024308.jpg", photo3))
        button3.pack(side="left")

        button4 = tk.Button(image_frame, image=photo4)
        button4.bind("<Enter>", lambda event: show_info(event, "ISIC_0024309.jpg", "Fecha4", "Paciente4"))
        button4.bind("<Leave>", hide_info)
        button4.bind("<Button-1>", lambda event: show_metadata(event, "ISIC_0024309.jpg", photo4))
        button4.pack(side="left")

        button5 = tk.Button(image_frame, image=photo5)
        button5.bind("<Enter>", lambda event: show_info(event, "F8ew2v5WQAARCWc.png", "Fecha5", "Paciente5"))
        button5.bind("<Leave>", hide_info)
        button5.bind("<Button-1>", lambda event: show_metadata(event, "F8ew2v5WQAARCWc.png", photo5))
        button5.pack(side="left")

categories = ["Categoría 1", "Categoría 2", "Categoría 3", "Categoría 4"]

for category in categories:
    button = tk.Button(category_frame, text=category, font=("Arial", 12, "bold"), fg="brown", command=lambda category=category: load_image_gallery(category))
    button.pack(side="left",pady=10)

# Crear las imágenes 
image1 = Image.open("ISIC_0024306.jpg")
image2 = Image.open("ISIC_0024307.jpg")
image3 = Image.open("ISIC_0024308.jpg")
image4 = Image.open("ISIC_0024309.jpg")

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

#-------------------------

# Mostrar la ventana y esperar a que el usuario interactúe con ella
root.mainloop()
