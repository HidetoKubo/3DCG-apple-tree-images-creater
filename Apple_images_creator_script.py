# -*- coding: utf-8 -*-
import math
import bpy
import random
import time
import numpy as np
import numpy.linalg as LA
import os
import datetime
import sys
import re
import glob
import openpyxl

#path = os.getcwd()

#print("current directory = ", path)

start0 = time.time()

#file path
path = os.path.abspath(os.path.dirname(__file__))
print(path)
FILE_PATH = "/".join(re.split(r'\/', path)[0:-1])

logtime = (datetime.datetime.now())
DATE_DIR = ('/log_' + logtime.strftime('%Y%m%d_%H%M%S') + '_waika')

OUTPUT_PATH = FILE_PATH + '/blender_traindata_waika'+ DATE_DIR
print(OUTPUT_PATH)

HDR_PATH = FILE_PATH + '/hdri'
hdri_files = glob.glob(HDR_PATH + "/*")


def add_object_transform(X,Y,Z,arg_objectname='Default',
arg_rotation=(0,0,0),arg_scale=(1,1,1), randflag = False):
    # 指定オブジェクトを取得する
    selectob=bpy.context.scene.objects[arg_objectname]
    if randflag == True:
        #りんごのパラメータ
        # 位置を変更する
        selectob.location.x = X
        selectob.location.y = Y
        selectob.location.z = Z
        # 回転を変更する
        # 弧度法で設定する必要があるため、度数法の入力を変換する
        selectob.rotation_euler.x = 2*math.pi/360*(random.randint(50, 130))
        selectob.rotation_euler.y = 2*math.pi/360*(random.randint(-40, 30))
        selectob.rotation_euler.z = 2*math.pi/360*(random.randint(0, 360))
        # 拡大縮小を変更する
        scaleparam = random.uniform(1.0, 1.08) # apple_size 0.6~1.08
        selectob.scale.x = scaleparam
        selectob.scale.y = scaleparam
        selectob.scale.z = scaleparam

        
        #カメラのパラメータ
        #位置
        
        #注視点
        
        #照明のパラメータ
        #個数
        #位置

    else:
        
        #りんごのパラメータ
        # 位置を変更する
        selectob.location.x
        selectob.location.y
        selectob.location.z
        # 回転を変更する
        # 弧度法で設定する必要があるため、度数法の入力を変換する
        selectob.rotation_euler.x += 2*math.pi/360*arg_rotation[0]
        selectob.rotation_euler.y += 2*math.pi/360*arg_rotation[1]
        selectob.rotation_euler.z += 2*math.pi/360*arg_rotation[2]
        # 拡大縮小を変更する
        selectob.scale.x *= arg_scale[0]
        selectob.scale.y *= arg_scale[1]
        selectob.scale.z *= arg_scale[2]


        return

def duplicate_object_rename(arg_objectname="Default", arg_dupname=""):

    # 他のオブジェクトに操作を適用しないよう全てのオブジェクトを走査する
    for ob in bpy.context.scene.objects:
        # 非選択状態に設定する
        ob.select_set(False)

    # 指定オブジェクトを取得する
    # (get関数は対象が存在しない場合 None が返る)
    targetob = bpy.data.objects.get(arg_objectname)

    # 指定オブジェクトが存在するか確認する
    if targetob == None:
        # 指定オブジェクトが存在しない場合は処理しない
        return

    # 対象オブジェクトを選択状態に変更する
    targetob.select_set(True)

    # オブジェクトを複製する
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate=None, TRANSFORM_OT_translate=None)

    # 対象オブジェクトの選択状態を解除する
    targetob.select_set(False)

    # 複製オブジェクト名が指定されている場合は名前変更
    if len(arg_dupname) > 0:
        # 複製オブジェクトの名前を取得する
        duplicated_objectname=arg_objectname + ".001"
    
        # 複製オブジェクトを取得する
        duplicatedob=bpy.data.objects[duplicated_objectname]
        
        # 複製オブジェクトの名前を変更する
        duplicatedob.name=arg_dupname

    return


def object_visiblity(arg_objectname="", unvisible = True):
    for ob in bpy.context.scene.objects:
        # 非選択状態に設定する
        ob.select_set(False)

    # 指定オブジェクトを取得する
    # (get関数は対象が存在しない場合 None が返る)
    targetob = bpy.data.objects.get(arg_objectname)

    # 指定オブジェクトが存在するか確認する
    if targetob == None:
        # 指定オブジェクトが存在しない場合は処理しない
        return

    # 対象オブジェクトを選択状態に変更する
    targetob.select_set(True)

    if unvisible == True:
        #ビューポート(プレビュー)時，選択したオブジェクトを非表示
        #bpy.context.object.hide_viewport = True
        #レンダリング(画像生成)時，選択したオブジェクトを非表示
        targetob.hide_render = True

    else:
        #ビューポート(プレビュー)時，選択したオブジェクトを非表示
        #bpy.context.object.hide_viewport = False
        #レンダリング(画像生成)時，選択したオブジェクトを非表示
        targetob.hide_render = False

    # 対象オブジェクトの選択状態を解除する
    targetob.select_set(False)
    


# 指定オブジェクトの削除
def delete_object_target(arg_objectname=""):
    
    # 指定オブジェクトを取得する
    # (get関数は対象が存在しない場合 None が返る)
    targetob = bpy.data.objects.get(arg_objectname)

    # 指定オブジェクトが存在するか確認する
    if targetob != None:
        # オブジェクトが存在する場合は削除を行う
        bpy.data.objects.remove(targetob)
    return
    

def make_random_apples(random_min, random_max):
    APPLE_COUNT = random.randint(random_min, random_max)
    for num in range(APPLE_COUNT):
        applename = "Apple" + str(num + 1)
        duplicate_object_rename(arg_objectname="Apple",arg_dupname="Apple"+str(num + 1))
        add_object_transform(0,arg_objectname = applename, randflag = True)
    
def delete_all_apples():
    for obj in bpy.data.objects:
        objname = obj.name
        if ("Apple" in objname) and (objname[-1].isdecimal()):
            delete_object_target(arg_objectname=objname)
            
#樹木モデル削除関数
def delete_tree():
    for obj in bpy.data.objects:
        objname = obj.name
        tree = re.findall('tree.*', objname)
        leaves = re.findall('leaves.*', objname)
        if tree or leaves: # which one is True
        #if ("tree" in objname) or ("leaves" in objname):
            delete_object_target(arg_objectname=objname)

#リンゴの数ランダム設定関数
def apple_count():
    apple_lst=[]
    for obj in bpy.data.objects:   
        objname = obj.name
        #print(objname)
        if re.findall('tree.*', objname):
            #apple_list.append("APPLE_COUNT_" + str(number)) 
            #apple_dic[apple_list[number]] = random.randint(5,25)
            apple_lst.append(random.randint(60,60)) #apple_number: 60~65
        
    return apple_lst
    

# X軸がマイナス値の頂点を選択状態にする
# 引数   arg_objectname：指定オブジェクト名
# 戻り値

# 指定した名前を持つオブジェクトをアクティブ化する関数
def my_activator(obj_name):
    # 全てのオブジェクトのリスト bpy.data.objects のうち obj_name を持つオブジェクトをアクティブ化
    bpy.context.view_layer.objects.active = bpy.data.objects[obj_name]
            
#オブジェクトにマテリアルを割り当てる関数
def assign_material():
    #leaf_random = random.randint(1,2)
    leaf_random = 1
    #print("leaf_random= ", leaf_random)
    for obj in bpy.data.objects:   
        objname = obj.name
        tree = re.findall('tree.*', objname)
        leaves = re.findall('leaves.*', objname)
        cube = re.findall('cube', objname)
        
        if tree:
            for slot in obj.material_slots:
                if slot.name.startswith(""):
                    (base, sep, ext) = slot.name.rpartition(".")
                    if slot.name == "":
                        if "tree_mat" in bpy.data.materials:
                            slot.material = bpy.data.materials.get("tree_mat")
        
        elif cube:
            for slot in obj.material_slots:
                    if leaf_random == 1:
                        if "Material.001" in bpy.data.materials:#[Material.001] = gleen leaf (leaf_powerpoint.png)
                            slot.material = bpy.data.materials.get("Material.001")                         
                    elif leaf_random == 2:
                        if "Material.002" in bpy.data.materials:#[Material.002] = yellow leaf (leaf_yellow.png)
                                slot.material = bpy.data.materials.get("Material.002")
            
        elif leaves:         
            my_activator(objname) #leaves active
            bpy.ops.object.material_slot_add() #slot add
            for slot in obj.material_slots:          
                if slot.name.startswith(""):
                    (base, sep, ext) = slot.name.rpartition(".")
                    if slot.name == "":
######### red apple: random leaf code 赤リンゴ時の葉色割り当てコード #############
                        if leaf_random == 1:
                            if "Material.001" in bpy.data.materials:#[Material.001] = gleen leaf (leaf_powerpoint.ong)
                                slot.material = bpy.data.materials.get("Material.001")                         
                        elif leaf_random == 2:
                            if "Material.002" in bpy.data.materials:#[Material.002] = yellow leaf (leaf_yellow.ong)
                                slot.material = bpy.data.materials.get("Material.002")
#####################################################################################


#指定した範囲の全枝頂点を取得し、リストで返す関数
def apple_put_branch():
    name = "tree"
    bpy.context.view_layer.objects.active = bpy.data.objects[name]
    # 全てのオブジェクトを非選択状態にする
    bpy.ops.object.select_all(action='DESELECT')

    # 指定されたオブジェクト名を選択状態にする
    bpy.data.objects[name].select_set(True)

    # メッシュ化する
    bpy.ops.object.convert(target='MESH')
    # スムーズシェード(ポリゴンを滑らかにする)
    bpy.ops.object.shade_smooth()

    vertices_lst = []
    i = 1
    for v in bpy.context.object.data.vertices : 
        X =  v.co.x 
        Y =  v.co.y 
        Z =  v.co.z
        if (X < -0.2 or 0.2 < X) and (Y < -0.2 or 0.2 < Y):
            vertices_lst.append([X,Y,Z])
        else:
            i += 1
    return vertices_lst


#色温度,太陽位置のランダム自動変更関数
def atmos_texture():
    random_atmos = random.randint(1,9) #36パターンの中から一つをランダムで算出
    #random_atmos = 9
    print("random_atmos = ", random_atmos)
    # 1~9 : 春 (1~3: 朝、　4~6: 昼、　7~9: 夕)
    # 10~18 : 夏
    # 19~27 : 秋
    # 28~36 : 冬

    if random_atmos == 1: # 春×朝×晴れ
        sun_elevation = 16.93 #太陽の高度
        sun_rotation = 74.06 #太陽の回転
        sun_intensity = 0.03/1 #太陽光の強さ
        air_density = 0.002 #空気抵抗
        dust_density = 0 #ちり
        ozone_density = 0 #オゾン
        back_color = 2
        #mix_percent = 
    
    elif random_atmos == 2: # 春×朝×曇り
        sun_elevation = 16.93 #太陽の高度
        sun_rotation = 74.06 #太陽の回転
        sun_intensity = 0.03/10 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.6 #ちり
        ozone_density = 0 #オゾン
        back_color = 0.2
        #mix_percent = 
        
    elif random_atmos == 3: # 春×朝×雨
        sun_elevation = 16.93 #太陽の高度
        sun_rotation = 74.06 #太陽の回転
        sun_intensity = 0.03/20 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.8 #ちり
        ozone_density = 5 #オゾン
        back_color = 0.1
        #mix_percent = 
        
    elif random_atmos == 4: # 春×昼×晴れ
        sun_elevation = 76.14 #太陽の高度
        sun_rotation = 200.18 #太陽の回転
        sun_intensity = 0.2/1 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0 #ちり
        ozone_density = 0 #オゾン
        back_color = 3.5
        #mix_percent = 
        
    elif random_atmos == 5: # 春×昼×曇り
        sun_elevation = 76.14 #太陽の高度
        sun_rotation = 200.18 #太陽の回転
        sun_intensity = 0.2/10 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.6 #ちり
        ozone_density = 0 #オゾン
        back_color = 2
        #mix_percent = 
        
    elif random_atmos == 6: # 春×昼×雨
        sun_elevation = 76.14 #太陽の高度
        sun_rotation = 200.18 #太陽の回転
        sun_intensity = 0.2/20 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.8 #ちり
        ozone_density = 5 #オゾン
        back_color = 1.25
        #mix_percent = 
        
    elif random_atmos == 7: # 春×夕×晴れ
        sun_elevation = 9.11 #太陽の高度
        sun_rotation = 291.36 #太陽の回転
        sun_intensity = 0.03/1 #太陽光の強さ
        air_density = 0.7 #空気抵抗
        dust_density = 2 #ちり
        ozone_density = 0 #オゾン
        back_color = 0.2
        #mix_percent = 
        
    elif random_atmos == 8: # 春×夕×曇り
        sun_elevation = 9.11 #太陽の高度
        sun_rotation = 291.36 #太陽の回転
        sun_intensity = 0.03/10 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.8 #ちり
        ozone_density = 1.5 #オゾン
        back_color = 0.8
        #mix_percent = 
        
    elif random_atmos == 9: # 春×夕×雨
        sun_elevation = 9.11 #太陽の高度
        sun_rotation = 291.36 #太陽の回転
        sun_intensity = 0.03/20 #太陽光の強さ
        air_density = 0 #空気抵抗
        dust_density = 0.8 #ちり
        ozone_density = 1.5 #オゾン
        back_color = 0.3
        #mix_percent = 
    
    else:
        print("atmos error")

    sun_elevation = sun_elevation*(math.pi/180) #太陽の高度
    sun_rotation = sun_rotation*(math.pi/180) #太陽の回転
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].sun_elevation = sun_elevation
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].sun_rotation = sun_rotation
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].sun_intensity = sun_intensity
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].air_density = air_density
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].dust_density = dust_density
    bpy.data.worlds["World.001"].node_tree.nodes["大気テクスチャ"].ozone_density = ozone_density
    bpy.data.worlds["World.001"].node_tree.nodes["背景"].inputs[1].default_value = back_color
    #bpy.data.worlds["World.001"].node_tree.nodes["Mix.002"].inputs[0].default_value = mix_percent





#処理時間を測定し、Excel出力する関数
def time_measure(time_lst):
    # ファイルの読み込み
    wb=openpyxl.load_workbook("time_measure.xlsx")
    # シートの読み込み
    sheet = wb['Sheet1']
    # 値の代入
    count = 0
    for num in time_lst:
        # column: 列,  row: 行
        sheet.cell(column=9,row=3+count).value = num
        count += 1

    # 保存先とファイル名の設定
    wb.save("time_measure.xlsx")


#樹木3Dモデル作成関数
def tree_create():
    #branchDist=1.35
    #levels=10
    #splitHeight=0.2
    #baseSize=0.10

    a_1 = random.uniform(1.0,1.1) # a_1: stem length shin:1.0~1.3, 1.2~1.4
    a_2 = random.uniform(0.4,0.5) # a_2: first branch length:0.3,0.5
    #branch number change
    b = random.randint(20,30) # b: branch number 4, 10: 10~20
    c = random.randint(10,20) # c: first branch angle adjustment
    d_1 = random.randint(250,300) # c: stem curve adjustment
    d_2 = random.randint(0,300) # c: first branch curve adjustment
    e = random.uniform(0.020,0.026) # e: stem & branch wide
    #leaf change
    f = random.randint(30,40) # f: leaf number 40~50
    g = random.uniform(1,2) # leaf size 0.33~0.50
    
    #bevelRes=1 カーブオブジェクトを囲うベベルの外周(切り口)の滑らかさ
    bpy.ops.curve.tree_add(do_update=True,\
    bevel=True,\
    prune=False,\
    showLeaves=True,\
    useArm=False,\
    seed=0,\
    handleType='0',\
    bevelRes=4,\
    resU=4,\
    levels=8,\
    length=(a_1, a_2, 0.9, 0.45),\
    lengthV=(0.05, 0.1, 0.15, 0.25),\
    taperCrown=0,\
    branches=(0, b, 5, 9),\
    curveRes=(8, 5, 3, 1),\
    curve=(0, c, 60, 0),\
    curveV=(d_1, d_2, 75, 75),\
    curveBack=(0, 0, 0, 0),\
    baseSplits=0,\
    segSplits=(0, 0, 0, 0),\
    splitByLen=True,\
    rMode='rotate',\
    splitStraight=0,\
    splitLength=0,\
    splitAngle=(8, 20, 25, 30),\
    splitAngleV=(2, 5, 5, 5),\
    scale=13,\
    scaleV=3,\
    attractUp=(0, 0, 0.25, 0.25),\
    attractOut=(0, 0, 0, 0),\
    shape='7',\
    shapeS='4',\
    customShape=(0.5, 1, 0.3, 0.5),\
    branchDist=1.35,\
    nrings=0,\
    baseSize=0.30,\
    baseSize_s=0.5,\
    leafBaseSize=0.2,\
    splitHeight=0.2, \
    splitBias=0, \
    ratio=e,\
    minRadius=0.0015,\
    closeTip=False, \
    rootFlare=1.25, \
    splitRadiusRatio=10, \
    autoTaper=True, \
    taper=(1, 1, 1, 1), \
    noTip=False, \
    radiusTweak=(1, 1, 1, 1), \
    ratioPower=0.8, \
    downAngle=(90, 110, 45, 45), \
    downAngleV=(0, 75, 10, 10), \
    useOldDownAngle=False, \
    useParentAngle=True, \
    rotate=(99.5, 137.5, 137.5, 137.5),\
    rotateV=(15, 0, 0, 0),\
    scale0=1, \
    scaleV0=0.05, \
    pruneWidth=0.4, \
    pruneBase=0.3, \
    pruneWidthPeak=0.6, \
    prunePowerHigh=0.5, \
    prunePowerLow=0.001,\
    pruneRatio=1,\
    leaves=f, \
    leafType='0', \
    leafDownAngle=60, \
    leafDownAngleV=30,\
    leafRotate=90, \
    leafRotateV=10, \
    leafObjZ='+2', \
    leafObjY='+1', \
    leafScale=g,\
    leafScaleX=0.6, \
    leafScaleT=-0.25,\
    leafScaleV=0.25,\
    leafShape='dFace',\
    leafDupliObj='cube',\
    leafangle=-30, \
    horzLeaves=True,\
    leafDist='6', \
    armAnim=False, \
    previewArm=False,\
    leafAnim=False,\
    frameRate=1, \
    loopFrames=0, \
    wind=20, \
    gust=10, \
    gustF=0.075,\
    af1=1, af2=1, af3=4, \
    makeMesh=False,\
    armLevels=10,\
    boneStep=(1, 1, 1, 1),\
    matIndex=(0, 0, 0, 0))
    


camera = bpy.data.objects['Camera']
def look_at(target):
    ray = np.subtract(target, camera.location)
    ray_xy = np.array([ray[0], ray[1], 0])
    x = np.array([-ray[2], +0, ray[1]])
    y = np.array([LA.norm(ray_xy), 0, -ray[0]])
    camera.rotation_euler = np.arctan2(y, x)


DATA_COUNT = 1
VIEW_COUNT = 1

#一回でいい動作
tree_polylist = []

for i in bpy.data.objects["tree"].to_mesh().vertices:
    tree_polylist.append(i.co)
tree_polylist_len = len(tree_polylist)

    
#学習データの生成
#作成するデータの数だけ繰り返す
for data_num in range(DATA_COUNT):
    
    #既存の樹木オブジェクト削除
    start = time.time()
    delete_tree()
    delete_tree_time = time.time() - start
    
    #新しい樹木オブジェクト生成
    bpy.context.scene.cursor.location = (0,0,0)
    start2 = time.time()
    tree_create()
    tree_create_time = time.time() - start2
    
    #マテリアルの割り当て
    start3 = time.time()
    assign_material() # material assign
    assign_material_time = time.time() - start3
    
    apple_list =  apple_count() #リンゴの数ランダム設定
    
    #枝頂点の取得
    start4 = time.time()
    vertices_lst = apple_put_branch()
    apple_put_branch_time = time.time() - start4
    
    #色温度の変更
    start4_2 = time.time()
    atmos_texture()
    atmos_change_time = time.time() - start4_2
    
    #果実の透過処理
    start5 = time.time()
    object_visiblity(arg_objectname="Apple", unvisible = False)
    apple_visibility_time = time.time() - start5
    
    
    #果実オブジェクトの生成
    start6 = time.time()
    location_list = random.sample(vertices_lst, apple_list[0])
    sum1 = 0
    y = 0#-6
    for num in range(len(location_list)):        
        applename = "Apple" + str(num + 1)
        #果実オブジェクトの名前変更
        duplicate_object_rename(arg_objectname="Apple",arg_dupname="Apple"+str(num + 1))
        #果実の枝配置
        add_object_transform(location_list[num][0],location_list[num][1],location_list[num][2],arg_objectname = applename,randflag = True)     
    apple_create_time = time.time() - start6

    
    #視点切り替え
    for view_num in range(VIEW_COUNT):
        #撮影のたびに変更    
        poly_id = random.randint(0, tree_polylist_len)
        #print(poly_id)
        polyx = tree_polylist[poly_id][0]
        polyy = tree_polylist[poly_id][1]
        polyz = tree_polylist[poly_id][2]
        in_camera_num = 0

        look_at_point = [polyx, polyy, polyz]
        camera.location = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(6, 18))
        look_at(look_at_point)      
        
        #render(filename=f'render{i}.png')
        
        # ↓レンダリングの設定↓
        
        #ブレンダーエンジンの種類選択
        bpy.context.scene.render.engine = 'CYCLES'
        #従来は128 テストは64
        #bpy.context.scene.cycles.samples = 32
        #bpy.context.scene.cycles.samples = 64
        bpy.context.scene.cycles.samples = 128
        
        #add_object_transform(arg_objectname="Camera", randflag = True)

        
        #3DCG農園画像のレンダリング
        start7 = time.time()
        object_visiblity(arg_objectname="Apple", unvisible = True)
        bpy.ops.render.render()
        bpy.data.images['Render Result'].save_render(OUTPUT_PATH + str(data_num)+'/'+str(view_num)+'/Appleimage.png')
        render_appleimage_time = time.time() - start7


        #ブレンダーエンジンの種類選択
        bpy.context.scene.render.engine = 'BLENDER_EEVEE'
        #eeveeによるレンダリング用のピクセルあたりのサンプル数
        bpy.context.scene.eevee.taa_render_samples = 8
        object_visiblity(arg_objectname="tree", unvisible = True)
        object_visiblity(arg_objectname="cube", unvisible = True)
        object_visiblity(arg_objectname="leaves", unvisible = True)
        object_visiblity(arg_objectname="grass", unvisible = True)
        
        #果実デプスマップの生成
        start8 = time.time()
        bpy.ops.render.render()
        
        #透明オプションの有効化
        bpy.context.scene.render.film_transparent = True
        
        #背景を透明にして１つずつりんごを撮影(透明部分と不透明部分で2値化可能な画像)
        for obj_mask in range(len(location_list)):
            for objs in range(len(location_list)):
                if obj_mask == objs:
                    object_visiblity(arg_objectname="Apple"+str(obj_mask + 1), unvisible = False)
                else:
                    object_visiblity(arg_objectname="Apple"+str(objs + 1), unvisible = True)

            #コンポジターノード(レンダリング画像の編集機能)の有効化
            #画像を深度形式で表す
            bpy.context.scene.use_nodes = True
            # bpy.ops: オペレーターの呼び出し
            #(アクティブな)シーンのレンダリング
            bpy.ops.render.render()
            # bpy.data: Blender内のデータアクセス
            # bpy.data.images['画像'].pixels:  Blenderファイルが使用している'画像'データのピクセル値の配列にアクセス
            #'Viewer Node'画像データのピクセル値を配列化
            pixels = bpy.data.images['Viewer Node'].pixels
            #変数arrは0~1の値をとる
            arr = np.array(pixels)
            
            #果実デプスマップのレンダリング
            
            #変数arr>0, つまり果実が画角内にあるなら、デプスマップ生成
            if arr.max() > 0:
                #if obj_mask == 1:
                #    with open(OUTPUT_PATH + "depth.npz", "wb") as f:
                #        np.savez(f, arr)
                start9 = time.time()
                bpy.data.images['Render Result'].save_render(OUTPUT_PATH 
                + str((data_num)*VIEW_COUNT) + '/' + str(view_num)+'/Appledepth'
                + str(in_camera_num + 1).rjust(2,'0')+'.png')
                in_camera_num = in_camera_num + 1
                apple_depth_time = time.time() - start9        
        all_apple_depth_time = time.time() - start8
        one_apple_depth_time = all_apple_depth_time / len(location_list)
        
        #全果実の透過       
        for unvisible_apple in range(len(location_list)):
            objname = "Apple" + str(unvisible_apple + 1)
            object_visiblity(arg_objectname=objname, unvisible = True)
        
        #木と葉の透過解除
        object_visiblity(arg_objectname="tree", unvisible = False)
        object_visiblity(arg_objectname="cube", unvisible = False)
        object_visiblity(arg_objectname="leaves", unvisible = False)
        
        #樹木デプスマップのレンダリング
        start10 = time.time()
        bpy.ops.render.render()      
        bpy.data.images['Render Result'].save_render(OUTPUT_PATH + str((data_num)*VIEW_COUNT) + '/' + str(view_num)+'/Treedepth.png')
        tree_depth_time = time.time() - start10
        
        #コンポジターノード(レンダリング画像の編集機能)の無効化
        bpy.context.scene.use_nodes = False
        
        #全果実の透過解除
        object_visiblity(arg_objectname="Apple", unvisible = False)
        for unvisible_apple in range(len(location_list)):
            objname = "Apple" + str(unvisible_apple + 1)
            object_visiblity(arg_objectname=objname, unvisible = False)
        
        #全オブジェクトの透過解除
        object_visiblity(arg_objectname="Apple", unvisible = False)
        object_visiblity(arg_objectname="cube", unvisible = False)
        object_visiblity(arg_objectname="grass", unvisible = False)
        
        #透明オプションの無効化
        bpy.context.scene.render.film_transparent = False
       
        
    #果実オブジェクトの削除
    start12 = time.time()
    for remove_apple in range(len(location_list)):
        objname = "Apple" + str(remove_apple + 1)
        delete_object_target(arg_objectname=objname)
    apple_delete_time = time.time() - start12

all_time = time.time() - start0

# ↓計測した処理時間の出力↓

all_depth_time = all_apple_depth_time + tree_depth_time
#プログラム処理時間の算出
program_time = tree_create_time +\
 delete_tree_time +\
 assign_material_time +\
 apple_put_branch_time +\
 atmos_change_time +\
 apple_visibility_time +\
 apple_create_time +\
 apple_delete_time
#レンダリング処理時間の算出
render_time = render_appleimage_time + all_depth_time
#計測した処理時間をリストに格納
time_lst = [len(location_list),\
 all_time,\
 tree_create_time,\
 delete_tree_time,\
 assign_material_time,\
 apple_put_branch_time,\
 atmos_change_time,\
 apple_visibility_time,\
 apple_create_time,\
 apple_delete_time,\
 render_appleimage_time,\
 all_depth_time,\
 one_apple_depth_time,\
 all_apple_depth_time,\
 tree_depth_time,\
 program_time,\
 render_time]

#エクセルに出力
#time_measure(time_lst)

