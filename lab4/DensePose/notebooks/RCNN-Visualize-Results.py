import numpy
import cv2
import matplotlib.pyplot as plt
import numpy as np

import os

# 如果路径不对，将DensePoseData_dir改为你的绝对路径
# DensePoseData_dir = "D:\\projects\\DensePose\\DensePoseData"
DensePoseData_dir = os.path.abspath("../DensePoseData")
print(DensePoseData_dir)

im  = cv2.imread(os.path.join(DensePoseData_dir, 'demo_data/demo_im.jpg'))
IUV = cv2.imread(os.path.join(DensePoseData_dir, 'infer_out/demo_im_IUV.png'))
INDS = cv2.imread(os.path.join(DensePoseData_dir, 'infer_out/demo_im_INDS.png'), 0)

fig = plt.figure(figsize=[15,15])
plt.imshow(   np.hstack((IUV[:,:,0]/24. ,IUV[:,:,1]/256. ,IUV[:,:,2]/256.))  )
plt.title('I, U and V images.')
plt.axis('off') ; plt.show()

fig = plt.figure(figsize=[12,12])
plt.imshow( im[:,:,::-1] )
plt.contour( IUV[:,:,1]/256.,10, linewidths = 1 )
plt.contour( IUV[:,:,2]/256.,10, linewidths = 1 )
plt.axis('off') ; plt.show()

fig = plt.figure(figsize=[12,12])
plt.imshow( im[:,:,::-1] )
plt.contour( INDS, linewidths = 4 )
plt.axis('off') ; plt.show()