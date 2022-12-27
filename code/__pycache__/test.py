import cv2
import os
import tensorflow as tf

# img = cv2.imread(r"C:\Users\molan\Downloads\Datasets\malaria_dataset\COCO_mkapa_train\000001.jpg")
# tensor_img = tf.convert_to_tensor(img)


# tensor_resized = tf.image.resize_with_pad(tensor_img, 896, 896, 3)

import csv 


f = open('test.csv', 'a')
header = ["filename"]

writer = csv.writer(f) 
writer.writerow(header)
data = []
for file in os.listdir(r'C:\Users\molan\Downloads\Datasets\malaria_dataset\COCO_mkapa_train') :
    if ".jpg" in file :
        data.append([f"{file}, {1}"])



writer.writerows(data)
        
f.close()