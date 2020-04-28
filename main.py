from keras.models import load_model
from flask import Flask, url_for, send_from_directory, request, redirect, flash, jsonify
from flask_cors import CORS, cross_origin
import logging, os
from werkzeug import secure_filename
import numpy as np
import json
from keras.preprocessing import image
from keras import backend as K


app = Flask(__name__)
cors = CORS(app, resources={r"/api_root": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/', methods = ['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def api_root():
    app.logger.info(PROJECT_HOME)

    app.logger.info(app.config['UPLOAD_FOLDER'])
    img = request.files['image']
    img_name = secure_filename(img.filename)
    create_new_folder(app.config['UPLOAD_FOLDER'])
    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    app.logger.info("saving {}".format(saved_path))
    img.save(saved_path)
    #Before prediction
    K.clear_session()
    # traitement de la prediction
    
    test_image = image.load_img("uploads/{}".format(img.filename), target_size=(64,64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image,axis=0)
    classifier = load_model('classifier_for_API.h5')
    result = classifier.predict(test_image)


    x=0
    c=0
    i=0
    prediction=""
    while (i<5):
        if result[0][i]>=x:
            x=result[0][i]
            c=i
            
        i=i+1
    if (x==0 and c==4) :
        c=5
    if c == 0:
        prediction = 'daisy'
    elif c == 1:
        prediction = 'dandelion'
    elif c == 2:
        prediction = 'rose'
    elif c == 3:
        prediction = 'sunflower'
    elif c == 4:
        prediction = 'tulip'
    elif c==5:
        prediction ="pas de prediction trouver"
    print(prediction)
    
    #After prediction
    K.clear_session()
    return jsonify(prediction)
@app.route('/hello')

def hello():
    
    return "Hello flower app works !"


if __name__ == '__main__':
   
    app.run(host='localhost', debug=True)
