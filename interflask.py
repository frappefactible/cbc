from flask import Flask, request, render_template
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image

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
            image = image.resize((28, 28))  # or whatever size you need
            image = np.array(image)
            image = image.reshape(1, 28, 28, 3)  # or whatever your model expects
            predictions = model.predict(image)
            print(predictions)
            predicted_class = np.argmax(predictions)
            confidence = predictions[0][predicted_class]
            confidence_percent = round(confidence * 100, 2)  # Redondear a 2 decimales

            # Guardar la imagen subida en una carpeta temporal
            filename = secure_filename(image_file.filename)
            image_path = os.path.join('temp/', filename)
            image_file.save(image_path)

            # Código para enviar el correo electrónico
            email = request.form['email']
            msg = Message('Hola, aqui tiene los resultados de su predicción', sender='factiblesoftwarecaba@gmail.com', recipients=[email])
            msg.body = f"La predicción tuvo un <span style='color:green;'>{confidence_percent}%</span> de precisión, detecando asi una clase <span style='color:red;'>{predicted_class}</span> dentro del modelo."
            msg.html = msg.body  # Set the HTML version of the body message
    
            with app.open_resource(image_path) as fp:
                msg.attach(filename, "image/jpeg", fp.read())

            mail.send(msg)

            #return render_template('index.html', prediction=predictions)

        return render_template('index.html', prediction=predicted_class, confidence=confidence_percent)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    model = tf.keras.models.load_model('modelo2.h5')
    app.run(debug=True)