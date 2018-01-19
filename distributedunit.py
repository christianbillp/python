#%% Extract features from image
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from gtts import gTTS
from PIL import Image
import numpy as np
import pytesseract
import paramiko
import os

class DistributedUnit():
    
    def __init__(self, unitname, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.temp_filename = f'{unitname}_snapshot.jpg'
    
    def see(self):
        with paramiko.SSHClient() as s: 
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            s.load_system_host_keys()
            s.connect(self.hostname, self.port, self.username, self.password)
            command = f'raspistill -o {self.temp_filename}'
            s.exec_command(command)

    def get(self):
        os.system(f'scp {self.username}@{self.hostname}:{self.temp_filename} .')
        
    def read(self):
        result = pytesseract.image_to_string(Image.open(f'{self.temp_filename}'))
        return result

    def classify(self):
        model = ResNet50(weights='imagenet')
        img = image.load_img(self.temp_filename, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        
        preds = model.predict(x)
        predictions = decode_predictions(preds, top=3)[0]
        best_prediction = predictions[0][1]
        self.latest_prediction = best_prediction

    def say(self):
        tts = gTTS(text=f'Best prediction: {self.latest_prediction}'.replace('_', ' '), lang='en')
        tts.save("hello.mp3")
        print(f'Best prediction: {self.latest_prediction}')
        os.system('mpg123 hello.mp3')

if __name__ == '__main__':
    pass
    #%%
    du = DistributedUnit('unit1', '192.168.0.151', 22, 'pi', 'raspberry')
    
    #%%
    du.see()
    
    #%%
    du.get()
    
    #%%
    du.read()
    
    #%% 
    du.classify()
    
    #%%
    du.say()