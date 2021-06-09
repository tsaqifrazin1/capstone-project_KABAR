import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, request
import base64
import requests
from PIL import Image
from io import BytesIO
import os


app = Flask(__name__)
label = {'cardboard': 0, 'metal': 1, 'paper': 2, 'plastic': 3, 'trash': 4}
labels = list(label.keys())

@app.route('/send-image', methods=['POST'])
def send_image():
    if request.method == 'POST':
        if 'image' not in request.files:
            from datetime import datetime
            url = request.json["image"]
            dateTimeObj = datetime.now()
            file_name_base64_data = dateTimeObj.strftime("%d-%b-%Y--(%H-%M-%S)")

            file_name_for_regular_data = url[-10:-4]

            try:
                if "data:image/jpeg;base64," in url:
                    base_string = url.replace("data:image/jpeg;base64,", "")
                    decoded_img = base64.b64decode(base_string)
                    img = Image.open(BytesIO(decoded_img))

                    file_name = file_name_base64_data + ".jpg"
                    img.save(file_name, "jpeg")

                elif "data:image/;base64," in url:
                    base_string = url.replace("data:image/png;base64,", "")
                    decoded_img = base64.b64decode(base_string)
                    img = Image.open(BytesIO(decoded_img))

                    file_name = file_name_base64_data + ".png"
                    img.save(file_name, "jpeg")
                else:
                    response =requests.get(url)
                    img = Image.open(BytesIO(response.content)).convert("RGB")
                    file_name = file_name_for_regular_data + '.jpg'
                    img.save(file_name, "jpeg")
                status = "Image has been succesfully sent to the server.\n"
                model = keras.models.load_model('kabar_model')
                imge = keras.preprocessing.image.load_img(file_name, target_size=(150, 150))
                X = image.img_to_array(imge)
                X = np.expand_dims(X, axis = 0)
                images = np.vstack([X])
                val = model.predict(images)
                result = labels[np.argmax(val)]
                status = str(result)
                os.remove(file_name)
            except Exception as e:
                status = "Error! = " + str(e)

        else :
            try:
                file = request.files['image']
                file.save("img.jpg")
                file_name = 'img.jpg'
                status = "Image has been succesfully sent to the server.\n"
                model = keras.models.load_model('kabar_model')
                imge = keras.preprocessing.image.load_img(file_name, target_size=(150, 150))
                X = image.img_to_array(imge)
                X = np.expand_dims(X, axis = 0)
                images = np.vstack([X])
                val = model.predict(images)
                result = labels[np.argmax(val)]
                status = str(result)
                os.remove(file_name)
            except Exception as e:
                status = "Error! = 'no selected file'" + str(e)
        return status
    else:
        return 'method is not defined'

if __name__ == "__main__":
    app.run(debug=True, port=8080)