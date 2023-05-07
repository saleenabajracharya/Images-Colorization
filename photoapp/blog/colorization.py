import numpy as np
import cv2 

prototxt_path='models/colorization.prototxt'
model_path='models/model.caffemodel'
kernel_path='models/kernal.npy'
image_path='person.jpg'

def colorMyImg(bw_imgage):
    print("this is abdul")
    net =cv2.dnn.readNetFromCaffe(prototxt_path,model_path)
    points=np.load(kernel_path)
    points=points.transpose().reshape(2,313,1,1)
    net.getLayer(net.getLayerId("class8_ab")).blobs=[points.astype(np.float32)]
    net.getLayer(net.getLayerId("conv8_313_rh")).blobs=[np.full([1,313],2.606,dtype="float32") ]

    #bw_imgage=cv2.imread(image_path)
    normalized =bw_imgage.astype("float32")/255.0
    lab =cv2.cvtColor(normalized,cv2.COLOR_BGR2LAB)
    resized =cv2.resize(lab,(224,224))
    L=cv2.split(resized)[0]
    L -=50
    net.setInput(cv2.dnn.blobFromImage(L))
    ab=net.forward()[0,:,:,:].transpose((1,2,0))
    ab=cv2.resize(ab,(bw_imgage.shape[1],bw_imgage.shape[0]))
    L=cv2.split(lab)[0]
    colorized =np.concatenate((L[:,:,np.newaxis],ab),axis=2)
    colorized=cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
    colorized=(255.0*colorized).astype("uint8")
    cv2.imshow("BW Image",bw_imgage)
    cv2.imshow("colorized",colorized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return colorized


