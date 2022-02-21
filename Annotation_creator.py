import os
import numpy as np
from PIL import Image
from numpy.random import *
import matplotlib.pyplot as plt
import glob
import cv2
import copy
import time
import json
import re
import sys

# 参照パス 適宜変更の必要あり
CURRENT_PATH = (os.getcwd()) + "/../../blender_traindata_waika/"
#CURRENT_PATH = (os.getcwd()) + "/../../blender_traindata_shinwaika/"

# 出力パス 適宜変更の必要あり
OUTPUT_PATH = (os.getcwd()) + "/../../complete_mask_waika"
#OUTPUT_PATH = (os.getcwd()) + "/../../complete_mask_shinwaika"
#CURRENT_PATH = os.getcwd()

# カレントディレクトリの確認 消してもok
path = os.getcwd()
print("current path = ", path)


class MyEncoder(json.JSONEncoder):
    
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)



###実際の計算部分###
start = time.time()
labels_info = {}
out_x = 0
out_num = 0
fail_count = 0
visible_thresh = 0.4
#contours_list = []

# range(0 ~ 自動生成した訓練データの数)
for i_data in range(0, 1):
    out_num = 0
    dmb_list = []
    # "log_20220218_144131_shinwaika0"　←適宜変更の必要あり
    DATA_PATH = CURRENT_PATH + "/log_20220220_154905_waika0/" +str(i_data)

    if ((os.path.exists(DATA_PATH + '/Appleimage.png') == False)
        or (os.path.exists(DATA_PATH + '/Appledepth01.png') == False)
        or (os.path.exists(DATA_PATH + '/Treedepth.png') == False)):
        print(DATA_PATH)
        continue

    else:
        render_img = Image.open(DATA_PATH + '/Appleimage.png')
        tree_img = Image.open(DATA_PATH + '/Treedepth.png').convert('L')
        npimg_tree = np.array(tree_img)
        masked_npimg_tree = npimg_tree < 200

        label_dict = {
            'fileref': "",
            'size': 000000,
            'filename': "",
            'base64_img_data': "",
            'file_attributes': {},
            'regions': {
            }
        }

    files = glob.glob(DATA_PATH +"/Appledepth*.png")

    #mask_T_F マスクがあるかどうか
    mask_T_F = False
    for file1 in files:
        img = Image.open(file1).convert('L')
        npimg_apple = np.array(img)
        if np.any(npimg_apple < 200) == False:
            print(i_data)
            img.close()
            continue
        npimg_apple_mean = npimg_apple[npimg_apple < 200].mean()
        masked_npimg_apple = npimg_apple < 200
        rows = np.any(masked_npimg_apple, axis=1)
        cols = np.any(masked_npimg_apple, axis=0)
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        dmb_list.append(copy.deepcopy([npimg_apple_mean, masked_npimg_apple, (rmin,rmax,cmin,cmax), file1, npimg_apple]))
        img.close()
    dmb_list.sort(reverse=True)
    dmb_len = len(dmb_list)
    for i in range(dmb_len):

        #見えている部分が15%以上あるか
        visible_complete = True

        #①果実マスクと木マスクのANDを抽出
        treeapp_and_mask = np.bitwise_and(dmb_list[i][1], masked_npimg_tree)

        #②果実マスクのピクセル数を計算
        apple_pixels = len((dmb_list[i][4])[(dmb_list[i][1]) == True])


        #③「果実マスクと木マスクのAND」の領域の深度のリストを取得
        tree_app_or_mask = dmb_list[i][4] > npimg_tree
        tree_app_or_mask = np.bitwise_and(tree_app_or_mask, dmb_list[i][1])
        apple_kakure_pixels = len((dmb_list[i][4])[tree_app_or_mask == True])
        visible_per = (apple_pixels - apple_kakure_pixels) / apple_pixels

        or_mask = tree_app_or_mask
        if visible_per > visible_thresh:
            for j in range(i, dmb_len):
                if i == j:
                    continue
                elif (dmb_list[i][2][0] <= dmb_list[j][2][1] and 
                     dmb_list[i][2][1] >= dmb_list[j][2][0] and
                     dmb_list[i][2][2] <= dmb_list[j][2][3] and 
                     dmb_list[i][2][3] >= dmb_list[j][2][2]):

                    and_mask = np.bitwise_and(dmb_list[i][1], dmb_list[j][1])
                    or_mask = np.bitwise_or(or_mask, and_mask)
                    app_app_kakure_pixels = len((dmb_list[i][4])[or_mask == True])
                    app_app_visible_per = (apple_pixels - app_app_kakure_pixels) / apple_pixels
                    if app_app_visible_per <= visible_thresh:
                        visible_complete = False
                        break
            if visible_complete == True:
                mask = dmb_list[i][1]

                contours, hierarchy = cv2.findContours((mask).astype(np.uint8), cv2.RETR_TREE,
                                                            cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) > 0:
                    x_poligon = [contours[0][ix][0][0] for ix in range(len(contours[0]))]
                    y_poligon = [contours[0][iy][0][1] for iy in range(len(contours[0]))]
                    instance_dict = {'region_attributes': {},
                                     'shape_attributes': {
                        'all_points_x': x_poligon,
                        'all_points_y': y_poligon,
                        'name': 'polygon'}}
                    label_dict['regions'][str(out_num)] = instance_dict
                    out_num = out_num + 1
                    mask_T_F =True
                    #contours_list.append(contours)


        else:
            visible_complete = False
    if mask_T_F == True:
        render_img.convert('RGB').save(OUTPUT_PATH + '/train' + str(out_x) + '.jpg', quality=95)
        label_dict['filename'] = 'train' + str(out_x) + '.jpg'
        labels_info[str(out_x)] = label_dict
        out_x = out_x + 1
    

    render_img.close()
    tree_img.close()

with open(OUTPUT_PATH + '/seisei.json', 'w') as fw:
    # ココ重要！！
    # json.dump関数でファイルに書き込む
    json.dump(labels_info, fw, cls=MyEncoder)
        
t = time.time() - start
print(t)
            


file2 = DATA_PATH + "/Treedepth.png"
img = Image.open(file2).convert('L')
npimg_tree = np.array(img)
masked_npimg_tree = npimg_tree < visible_thresh


###以下は描画処理###
fig = plt.figure()
plt.subplot(2, 1, 1) # 引数はそれぞれ、全体の行数、全体の列数、設定対象のIndex
plt.imshow(npimg_tree)
plt.gray()
plt.axis('off')

plt.subplot(2, 1, 2) 
plt.hist(npimg_tree.flatten(), bins=np.arange(15,30), range=[15, 30]) 
plt.show()
fig.savefig("tree_depth")


#実際の計算
#①果実マスクと木マスクのANDを抽出
and_mask = np.bitwise_and(masked_npimg_apple, masked_npimg_tree)

#②果実マスクのピクセル数を計算
apple_pixels = len(npimg_apple[masked_npimg_apple == True])
print("apple pixel :  ", apple_pixels)

#③「果実マスクと木マスクのAND」の領域の深度のリストを取得
#果実の深度リスト
and_mask_true = and_mask == True
print(and_mask_true)
apple_depth = npimg_apple[and_mask_true]
print(apple_depth)
#木の深度リスト
tree_depth = npimg_tree[and_mask == True]
apple_kakure_pixels = len(apple_depth > tree_depth)
print("apple kakure pixel : ", apple_kakure_pixels)

print("visible pixel of apple(%) : ", apple_kakure_pixels / apple_pixels)


