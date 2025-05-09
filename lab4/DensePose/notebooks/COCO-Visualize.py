from pycocotools.coco import COCO
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pycocotools.mask as mask_util
from random import randint

# 路径设置
detectron_dir = os.path.abspath("../modules/detectron/detectron")
coco_folder = os.path.join(detectron_dir, 'datasets/data/coco/')
DensePoseData_dir = os.path.abspath("../DensePoseData")

# 加载COCO标注
dp_coco = COCO(os.path.join(coco_folder, 'annotations/densepose_coco_2014_minival.json'))
Selected_im = 8844
im = dp_coco.loadImgs(Selected_im)[0]
ann_ids = dp_coco.getAnnIds(imgIds=im['id'])
anns = dp_coco.loadAnns(ann_ids)

# 加载图像
im_name = os.path.join(coco_folder + 'val2014', im['file_name'])
I = cv2.imread(im_name)
plt.imshow(I[:, :, ::-1]); plt.axis('off'); plt.title("Original Image"); plt.show()

# 初始化 IUV 图
I_im = np.zeros(I.shape[:2], dtype=np.uint8)
U_im = np.zeros(I.shape[:2], dtype=np.uint8)
V_im = np.zeros(I.shape[:2], dtype=np.uint8)

def GetDensePoseMask(Polys):
    MaskGen = np.zeros([256, 256])
    for i in range(1, 15):
        if Polys[i - 1]:
            current_mask = mask_util.decode(Polys[i - 1])
            MaskGen[current_mask > 0] = i
    return MaskGen

# 可视化 I/U/V scatter 图
fig = plt.figure(figsize=[15, 5])
plt.subplot(1, 3, 1); plt.imshow(I[:, :, ::-1]/255.); plt.axis('off'); plt.title('Patch Indices')
plt.subplot(1, 3, 2); plt.imshow(I[:, :, ::-1]/255.); plt.axis('off'); plt.title('U coordinates')
plt.subplot(1, 3, 3); plt.imshow(I[:, :, ::-1]/255.); plt.axis('off'); plt.title('V coordinates')

for ann in anns:
    bbr = np.round(ann['bbox'])
    if 'dp_masks' in ann:
        Point_x = np.array(ann['dp_x']) / 255. * bbr[2]
        Point_y = np.array(ann['dp_y']) / 255. * bbr[3]
        Point_I = np.array(ann['dp_I'])
        Point_U = np.array(ann['dp_U'])
        Point_V = np.array(ann['dp_V'])

        Point_x += bbr[0]
        Point_y += bbr[1]

        plt.subplot(1, 3, 1)
        plt.scatter(Point_x, Point_y, 22, Point_I)
        plt.subplot(1, 3, 2)
        plt.scatter(Point_x, Point_y, 22, Point_U)
        plt.subplot(1, 3, 3)
        plt.scatter(Point_x, Point_y, 22, Point_V)

plt.show()

# 构建稠密 IUV 图
for ann in anns:
    bbr = np.round(ann['bbox'])
    if 'dp_masks' in ann:
        Point_x = np.array(ann['dp_x']) / 255. * bbr[2]
        Point_y = np.array(ann['dp_y']) / 255. * bbr[3]
        Point_I = np.array(ann['dp_I'])
        Point_U = np.array(ann['dp_U'])
        Point_V = np.array(ann['dp_V'])

        Point_x += bbr[0]
        Point_y += bbr[1]

        for x, y, i, u, v in zip(Point_x, Point_y, Point_I, Point_U, Point_V):
            xx, yy = int(round(x)), int(round(y))
            for dx in range(-14, 14):
                for dy in range(-14, 14):
                    xxx, yyy = xx + dx, yy + dy
                    if 0 <= xxx < I.shape[1] and 0 <= yyy < I.shape[0]:
                        I_im[yyy, xxx] = int(i)
                        U_im[yyy, xxx] = int(u * 199)
                        V_im[yyy, xxx] = int(v * 199)

# 切割纹理图集
Tex_Atlas = cv2.imread(os.path.join(DensePoseData_dir, 'demo_data/texture_from_SURREAL.png'))[:, :, ::-1] / 255.0
TextureIm = np.zeros((24, 200, 200, 3))
for i in range(4):
    for j in range(6):
        TextureIm[6 * i + j] = Tex_Atlas[200 * j:200 * (j + 1), 200 * i:200 * (i + 1), :]

# 拼接 IUV 三通道
IUV = np.stack([I_im, U_im, V_im], axis=2).astype(np.uint8)

# 纹理贴图函数，融合原图
def TransferTexture(TextureIm, im, IUV):
    H, W = IUV.shape[0], IUV.shape[1]
    new_im = im.astype(np.float32) / 255.0  # 初始化为原图内容

    for part in range(1, 25):
        mask = IUV[:, :, 0] == part
        if np.sum(mask) == 0:
            continue

        U_part = IUV[:, :, 1][mask]
        V_part = IUV[:, :, 2][mask]

        tex = TextureIm[part - 1]
        tex_coords = tex[V_part, U_part]
        new_im[mask] = tex_coords

    return new_im

# 纹理映射并显示
image = TransferTexture(TextureIm, I, IUV)

plt.figure(figsize=(14, 14))
plt.imshow(image[:, :, ::-1])
plt.axis('off')
plt.title("Texture Transferred Image (with original background)")
plt.show()

print("done")
