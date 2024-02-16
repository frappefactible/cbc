from flask import Flask, request, render_template
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
model = None

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
            return render_template('index.html', prediction=predicted_class, confidence=confidence_percent)
    return render_template('index.html', prediction=None)

if __name__ == '__main__':
    model = tf.keras.models.load_model('modelo2.h5')
    app.run(debug=True)