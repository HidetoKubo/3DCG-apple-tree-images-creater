# 3DCGリンゴ樹木画像 自動生成システム
# 概要
これは、深層学習を用いてリンゴ形状の検出を行えるようにするため、3DCGのリンゴ樹木の学習データ画像を自動生成するシステムです。
「Apple_images_creator.Blender」というBlenderファイルのスクリプトを実行することで、リンゴの3DCG樹木画像、樹木のデプスマップ、果実のデプスマップが生成されます。
また、「mask_images_creator.py」というPythonファイルを実行することで、「seisei.json」というマスクデータの出力ファイルが生成されます。

具体的には、Blender (2.93) 内でPythonスクリプトを実行し、自動で画像のレンダリングを行っています。

# デモ動画

# 生成できる画像
![Cycles](https://user-images.githubusercontent.com/98790632/154609642-a3ea4864-92b6-466e-af3c-151c2f581357.png)
