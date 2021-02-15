# Mosaic
選択した画像を自動でモザイク処理するプログラム

モザイク前

<img width="300" src="https://raw.githubusercontent.com/nope0124/Mosaic/master/number.png">

モザイク後

<img width="300" src="https://raw.githubusercontent.com/nope0124/Mosaic/master/number_mosaic.png">


## 使い方（CUI版）



```
$ python mosaic.py [画像ファイルの相対パス]
```
(例)
```
$ python mosaic.py number.png
Successful!
```



・モザイク処理した画像は、ファイル名 + _mosaic + 拡張子という名前で元画像と同じディレクトリに保存される。

・すでに同名のファイルが存在している場合は番号を追加し、上書きを避ける。

・対応ファイルはjpg, png, jpeg。

・画像サイズの制限なし。

