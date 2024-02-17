from flask import Flask, request, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
model = None

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Cambia esto por tu servidor SMTP
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'factiblesoftwarecaba@gmail.com'  # Cambia esto por tu correo electrónico
app.config['MAIL_PASSWORD'] = 'mogjhuwgbeqbwcef'  # Cambia esto por tu contraseña

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def upload_predict():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            image = Image.open(image_file)
            image_copy = image.copy()  # Hacer una copia de la imagen original
            image = image.resize((28, 28))  # or whatever size you need
            image_array = np.array(image)
            image_array = image_array.reshape(1, 28, 28, 3)  # or whatever your model expects
            image = np.array(image)
            image = image.reshape(1, 28, 28, 3)  # or whatever your model expects
            predictions = model.predict(image_array)
            print(predictions)
            predicted_class = np.argmax(predictions)
            confidence = predictions[0][predicted_class]
            confidence_percent = round(confidence * 100, 2)  # Redondear a 2 decimales

            # Umbral de confianza
            confidence_threshold = 69.99  # Ajusta este valor según tus necesidades

            if confidence_percent < confidence_threshold:
                return render_template('index.html', prediction="La imagen subida no parece estar relacionada con el cáncer de piel.", confidence="-")
            
            # Agregar texto a la imagen
            draw = ImageDraw.Draw(image_copy)
            font = ImageFont.truetype("arial.ttf", 15)  # Asegúrate de tener la fuente arial.ttf en tu directorio de trabajo
            text = f"Clase: {predicted_class}, Precisión: {confidence_percent}%"
            draw.text((0, 0), text, (255, 255, 255), font=font)  # Cambia las coordenadas y el color según tus necesidades


            # Guardar la imagen subida en una carpeta temporal
            filename = secure_filename(image_file.filename)
            image_path = os.path.join('temp/', filename)
            image_copy.save(image_path)

            # Reabrir el archivo y guardarlo
            #image_file.seek(0)  # Retroceder al inicio del archivo
            #with open(image_path, 'wb') as f:
            #    f.write(image_file.read())

            # Código para enviar el correo electrónico
            email = request.form['email']
            msg = Message('Hola, aqui tiene los resultados de su predicción', sender='factiblesoftwarecaba@gmail.com', recipients=[email])
            msg.body = f"La predicción tuvo un <span style='color:green;'>{confidence_percent}%</span> de precisión, detectando asi una clase <span style='color:red;'>{predicted_class}</span> dentro del modelo."
            msg.html = msg.body  # Set the HTML version of the body message
    
            #with app.open_resource(image_path) as fp:
            #    msg.attach(filename, "image/jpeg", fp.read())
            with open(image_path, 'rb') as fp:
                    msg.attach(filename, "image/jpeg", fp.read())

            mail.send(msg)

            #return render_template('index.html', prediction=predictions)

        return render_template('index.html', prediction=predicted_class, confidence=confidence_percent)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    model = tf.keras.models.load_model('modelo2.h5')
    app.run(debug=True)