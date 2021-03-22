# Mosaic
選択した画像を自動で加工するプログラム。

モザイク処理、ぼかし処理、減色処理ができる。

モザイク

<img width="300" src="https://raw.githubusercontent.com/nope0124/Mosaic/master/number_mosaic.png">

ぼかし

<img width="300" src="https://raw.githubusercontent.com/nope0124/Mosaic/master/number_blur.png">

減色

<img width="300" src="https://raw.githubusercontent.com/nope0124/Mosaic/master/number_extraction.png">


## 使い方

コマンドの種類：mosaic, blur, extraction

```
$ python main.py [画像ファイルの相対パス] [コマンド]
```
(例)
```
$ python main.py number.png mosaic
Succeeded!
```



・加工処理した画像は、ファイル名 + _mosaic + 拡張子という名前で元画像と同じディレクトリに保存される。

・すでに同名のファイルが存在している場合は番号を追加し、上書きを避ける。

・対応ファイルはjpg, png, jpeg。

・実行時間は数秒で、画像サイズの制限なし。

