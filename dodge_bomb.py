import os
import random
import time
import sys
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def gameover(screen:pg.Surface) -> None:  #gameoverの定義
    go_img=pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(go_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    font=pg.font.Font(None,80)
    go_img.set_alpha(120)
    go_kk_img = pg.image.load("fig/8.png")
    txt=font.render("GameOver",
                    True,(255,255,255))
    go_img.blit(txt,[400,300])
    go_img.blit(go_kk_img,[340,290])
    go_img.blit(go_kk_img,[720,290])
    screen.blit(go_img,[0,0])
    pg.display.update()
    time.sleep(5)
def init_bb_imgs() ->tuple[list[pg.Surface],list[int]]:
    bb_imgs=[]
    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_imgs.append(bb_img)
    bb_accs=[a for a in range(1,11)]
    return bb_img, bb_accs
def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH <rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT <rct.bottom:
        tate = False
    return yoko,tate
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))  #
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    # bb_img = pg.Surface((20,20))  # 空のサーフェイス
    # pg.draw.circle(bb_img,(255,0,0),(10,10),10) #  爆弾四隅消した
    # bb_img.set_colorkey((0,0,0))  # 爆弾座標
    vx, vy = +5, +5 #  爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)  # 爆弾座標
    bb_rct.centery = random.randint(0,HEIGHT)

    avx = vx*bb_accs[min(tmr//500, 9)]
    avy = vy*bb_accs[min(tmr//500, 9)]
    bb_rct.move_ip(avx,avy)
    bb_img = bb_imgs[min(tmr//500, 9)]
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            return gameover(screen)#  ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()