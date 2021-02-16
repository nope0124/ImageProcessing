import sys
import fileinput
from pathlib import Path
import time
import copy

import cv2
    
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'PNG', 'JPG', 'JPEG'])

COMMANDS = set(['mosaic', 'blur', 'extraction'])

def main():

    if len(sys.argv) <= 2: #例外処理
        print("No arguments")
        return
    
    filename = sys.argv[1]
    COMMAND = sys.argv[2]
    if Path(filename).exists() and COMMAND in COMMANDS:  # 第一引数がファイルだったら
    
        EXTENSION = filename.rsplit('.', 1)[1]
        if EXTENSION not in ALLOWED_EXTENSIONS:
            print("Invalid extension")
            return
        ori_img = cv2.imread(filename) #画像の読み込み
        if ori_img is None:
            print("No images")
            return
        
        WIDTH = ori_img.shape[1]
        HEIGHT = ori_img.shape[0]
        MAX = max(WIDTH, HEIGHT)
        
        if COMMAND == 'mosaic':
        
            if max(WIDTH, HEIGHT) >= 500:
                if ori_img.shape[0] > ori_img.shape[1]: #縦長
                    HEIGHT = 500
                    WIDTH = int(HEIGHT * ori_img.shape[1] / ori_img.shape[0])
                else: #横長
                    WIDTH = 500
                    HEIGHT = int(WIDTH * ori_img.shape[0] / ori_img.shape[1])
            img = cv2.resize(ori_img, (WIDTH, HEIGHT))
            size = max(WIDTH, HEIGHT) // (50 + min(0, (MAX - 500) // 10)) #サイズが500px以下なら分割数を減らす
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
            
            img = cv2.resize(img, (ori_img.shape[1], ori_img.shape[0]))
            PATH = filename.rsplit('.', 1)[0] + '_mosaic'
            if Path(PATH + '.' + EXTENSION).exists():
                cnt = 1
                while Path(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION).exists():
                    cnt += 1
                cv2.imwrite(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION, img)
                print("Succeeded!")
            else:
                cv2.imwrite(PATH + '.' + EXTENSION, img)
                print("Succeeded!")
                
        elif COMMAND == 'blur':
        
            if max(WIDTH, HEIGHT) >= 500:
                if ori_img.shape[0] > ori_img.shape[1]: #縦長
                    HEIGHT = 500
                    WIDTH = int(HEIGHT * ori_img.shape[1] / ori_img.shape[0])
                else: #横長
                    WIDTH = 500
                    HEIGHT = int(WIDTH * ori_img.shape[0] / ori_img.shape[1])
            tmp_img = cv2.resize(ori_img, (WIDTH, HEIGHT))

            #初期化
            img = [[[0 for k in range(3)] for j in range(WIDTH)] for k in range(HEIGHT)]
            
            #二次元imos法
            tmp = 7
            for k in range(3):
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        img[max(i - tmp, 0)][max(j - tmp, 0)][k] += tmp_img[i][j][k]
                        if i + tmp + 1 < HEIGHT and j + tmp + 1 < WIDTH:
                            img[max(i - tmp, 0)][j + tmp + 1][k] -= tmp_img[i][j][k]
                            img[i + tmp + 1][max(j - tmp, 0)][k] -= tmp_img[i][j][k]
                            img[i + tmp + 1][j + tmp + 1][k] += tmp_img[i][j][k]
                        elif i + tmp + 1 < HEIGHT:
                            img[i + tmp + 1][max(j - tmp, 0)][k] -= tmp_img[i][j][k]
                        elif j + tmp + 1 < WIDTH:
                            img[max(i - tmp, 0)][j + tmp + 1][k] -= tmp_img[i][j][k]

            #縦の累積和
            for j in range(WIDTH):
                for i in range(1, HEIGHT):
                    for k in range(3):
                        img[i][j][k] += img[i - 1][j][k]
            #横の累積和
            for i in range(HEIGHT):
                for j in range(1, WIDTH):
                    for k in range(3):
                        img[i][j][k] += img[i][j - 1][k]
            
            #平均化
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    for k in range(3):
                        div = (1 + min(j, tmp) + min(WIDTH - j - 1, tmp)) * (1 + min(i, tmp) + min(HEIGHT - i - 1, tmp))
                        img[i][j][k] /= div
            
            #tmp_imgへの書き出し
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    for k in range(3):
                        tmp_img[i][j][k] = img[i][j][k]
            
            tmp_img = cv2.resize(tmp_img, (ori_img.shape[1], ori_img.shape[0]))
            PATH = filename.rsplit('.', 1)[0] + '_blur'
            if Path(PATH + '.' + EXTENSION).exists():
                cnt = 1
                while Path(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION).exists():
                    cnt += 1
                cv2.imwrite(PATH + '(' + str(cnt) + ')' + '.' + EXTENSION, tmp_img)
                print("Succeeded!")
            else:
                cv2.imwrite(PATH + '.' + EXTENSION, tmp_img)
                print("Succeeded!")
                
        elif COMMAND == 'extraction':
            print("Invalid command")
        else:
            print("Invalid command")
            return
        
            
            
        
    else:  # 第一引数がファイルではなかったら
        print("Invalid arguments")

if __name__ == "__main__":
    start = time.time()
    main()
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
