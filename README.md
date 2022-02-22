# リンゴ樹木3DCG画像 自動生成システム
# 概要
これは、深層学習(Mask R-CNN)によって、葉に隠れたリンゴの形状を検出するため、3DCGのリンゴ樹木の学習データ画像を自動生成するシステムです。
BlenderとPythonを用いて、リンゴの3DCG樹木画像と葉に隠れたリンゴの教師データを生成することができます。
なお、これらは大学院での私の研究内容であり、「Annotation_creator.py」を除き、全て自身で制作を行いました。

システムに関して、具体的には以下のような手順で学習データが生成できます。
1. Blender (2.93)ファイル「Apple_images_creator.blend」内でPythonスクリプトを実行し、リンゴの3DCG樹木画像とリンゴ・樹木の深度マップを生成
2. Pythonファイル「Annotation_creator.py」を実行し、リンゴ・樹木の深度マップを基に、葉に隠れた果実の教師データ「seisei.json」ファイルを生成

# システム紹介動画
https://user-images.githubusercontent.com/98790632/155083360-8efa7880-360f-4927-93d0-efa7ac0be556.mp4

# デモ動画
https://user-images.githubusercontent.com/98790632/155083376-624fa457-8af9-428e-a997-3d402e9011bd.mp4

# 生成できる画像

![tree](https://user-images.githubusercontent.com/98790632/155055961-0a3a2b3a-aefe-4443-8b7a-fe93a46bd81c.png)

![tree_depth](https://user-images.githubusercontent.com/98790632/155056295-b0f6ad81-07d2-48ba-ab88-8acbe902b5d5.png)

![apple_depth](https://user-images.githubusercontent.com/98790632/155056304-45122e0a-9e11-4673-8753-50745db41ed5.png)

# アップロードファイルの説明
・「Apple_images_creator.blend」: 3DCGリンゴ画像と深度マップを生成するBlenderファイル。スクリプト内にて出力のパスを任意のディレクトリに変更する必要があります。

・「Annotation_creator.py」: 生成した深度マップを基にアノテーションデータを生成するファイル。入力、出力のパスを任意のディレクトリに変更する必要があります。

・「texture.zip」：Blenderファイル内で用いるテクスチャ画像が入ったフォルダ。「Apple_images_creator.blend」と同じディレクトリに入れておく必要があります。

・「add_curve_sapling_3_2_8.zip」: Blenderの外部アドオン(拡張)機能が入ったフォルダ。下記サイトのような手順で、あらかじめBlenderで使えるようにする必要があります。
https://bookyakuno.com/how-to-install-addon/

・「Apple_images_creator_script.py」：「Apple_images_creator.blend」のスクリプト。実行の必要はありません。参考程度にご覧ください。

# テスト環境
Windows10

# 使用技術、サービス
Blender(2.93), Python
