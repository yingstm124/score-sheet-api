import Utility
from keras.models import load_model

class Predict:
    
    def __init__(self, img, debug=False):
        self.debug = debug
        self.image = img
        self.model = load_model('model/mnist.h5')

    def getResult(self):
        predicts = self.model.predict(self.image.reshape(1,28,28,1))
        result = np.argmax(predicts)

        if(self.debug):
            print('result --> ',result)
            showImage(self.image, 'image')

        return result