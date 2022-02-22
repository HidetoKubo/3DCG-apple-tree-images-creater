# リンゴ樹木3DCG画像 自動生成システム
# 概要
これは、深層学習(Mask R-CNN)によって、葉に隠れたリンゴの形状を検出するため、3DCGのリンゴ樹木の学習データ画像を自動生成するシステムです。
BlenderとPythonを用いて、リンゴの3DCG樹木画像と葉に隠れたリンゴの教師データを生成することができます。

具体的には、以下のような手順で学習データが生成できます。
1. Blender (2.93)ファイル「Apple_images_creator.blend」内でPythonスクリプトを実行し、リンゴの3DCG樹木画像とリンゴ・樹木の深度マップを生成
2. Pythonファイル「Annotation_creator.py」を実行し、リンゴ・樹木の深度マップを基に、葉に隠れた果実の教師データ「seisei.json」ファイルを生成

# デモ動画

# 生成できる画像
![Tree](https://user-images.githubusercontent.com/98790632/155055714-547f12e4-8931-4c8d-9a3c-2d82a0ab2a87.png)


# 使い方 動画

# テスト環境
Windows10

# 使用技術、サービス
Blender(2.93), Python
