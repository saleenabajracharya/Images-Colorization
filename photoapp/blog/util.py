import numpy as np
import cv2 
from django.core.files.uploadedfile import InMemoryUploadedFile

prototxt_path='models/colorization.prototxt'
model_path='models/model.caffemodel'
kernel_path='models/kernal.npy'

def colorMyImg(uploaded_image):
    net =cv2.dnn.readNetFromCaffe(prototxt_path,model_path)
    points=np.load(kernel_path)
    points=points.transpose().reshape(2,313,1,1)
    net.getLayer(net.getLayerId("class8_ab")).blobs=[points.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs=[np.full([1,313],2.606,dtype="float32") ]

    # Convert InMemoryUploadedFile to numpy array
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    uploaded_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    normalized = uploaded_image.astype("float32")/255.0
    lab = cv2.cvtColor(normalized,cv2.COLOR_BGR2LAB)
    resized = cv2.resize(lab,(224,224))
    L = cv2.split(resized)[0]
    L -= 50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0,:,:,:].transpose((1,2,0))
    ab = cv2.resize(ab,(uploaded_image.shape[1],uploaded_image.shape[0]))
    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:,:,np.newaxis],ab),axis=2)
    colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized = (255.0*colorized).astype("uint8")
    cv2.destroyAllWindows()
    return colorized
    
