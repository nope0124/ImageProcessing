import sys
import fileinput
from pathlib import Path

import cv2
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])


def main():

    if len(sys.argv) == 1: #例外処理
        print("No arguments")
        return
    
    if Path(sys.argv[1]).exists():  # 第一引数がファイルだったら
        filename = sys.argv[1]
        EXTENSION = filename.rsplit('.', 1)[1]
        if EXTENSION in ALLOWED_EXTENSIONS:
            ori_img = cv2.imread(filename) #画像の読み込み
            if ori_img is None:
                print("No images")
                return
            WIDTH = ori_img.shape[1]
            HEIGHT = ori_img.shape[0]
            if max(WIDTH, HEIGHT) >= 1000:
                if ori_img.shape[0] > ori_img.shape[1]: #縦長
                    HEIGHT = 1000
                    WIDTH = int(HEIGHT * ori_img.shape[1] / ori_img.shape[0])
                else: #横長
                    WIDTH = 1000
                    HEIGHT = int(WIDTH * ori_img.shape[0] / ori_img.shape[1])
            ori_img = cv2.resize(ori_img, (WIDTH, HEIGHT))
            size = max(WIDTH, HEIGHT) // 50
            img = ori_img
            for i in range(HEIGHT // size + 1):
                for j in range(WIDTH // size + 1):
                    R = 0
                    G = 0
                    B = 0
                    cnt = 1
                    for k in range(size):
                        for l in range(size):
                            if i * size + k >= HEIGHT:
                                continue
                            if j * size + l >= WIDTH:
                                continue
                            cnt += 1
                            R += img[i * size + k][j * size + l][0]
                            G += img[i * size + k][j * size + l][1]
                            B += img[i * size + k][j * size + l][2]
                    R /= cnt
                    G /= cnt
                    B /= cnt
                    for k in range(size):
                        for l in range(size):
                            if i * size + k >= HEIGHT:
                                continue
                            if j * size + l >= WIDTH:
                                continue
                            img[i * size + k][j * size + l][0] = R
                            img[i * size + k][j * size + l][1] = G
                            img[i * size + k][j * size + l][2] = B
            PATH = filename.rsplit('.', 1)[0] + '_mosaic'
            if Path(PATH + '.' + EXTENSION).exists():
                cnt = 1
                while Path(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION).exists():
                    cnt += 1
                cv2.imwrite(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION, img)
                print("Successful!")
            else:
                cv2.imwrite(PATH + '.' + EXTENSION, img)
                print("Successful!")
            
        else:
            print("Invalid extension")
        
    else:  # 第一引数がファイルではなかったら
        print("No files")

if __name__ == "__main__":
    main()
