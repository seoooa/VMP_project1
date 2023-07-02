# proj1-3. Robot Arm

import pygame
import os
import numpy as np
import time

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

#pygame init
pygame.init()
pygame.display.set_caption("20211511 김서아")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

#효과음 로드
rb_snd = pygame.mixer.Sound(os.path.join(assets_path, 'robot.mp3'))

#폰트 로드
font = pygame.font.SysFont("arial", 30, True, True)
    
def getRectangle(width, height, x = 0, y = 0):
    v = np.array([[x, y],
                 [x + width, y],
                 [x + width, y + height],
                 [x, y + height]],
                 dtype = "float")

    return v

def R3mat(deg):
    theta = np.deg2rad(deg)
    c = np.cos(theta)
    s = np.sin(theta)

    R = np.array([[c, -s, 0], 
                  [s, c, 0], 
                  [0, 0, 1]], dtype = 'float')
    return R 

def T3mat(tx, ty):
    T = np.array([[1, 0, tx], 
                  [0, 1, ty], 
                  [0, 0, 1]], dtype = 'float')
    
    return T

def draw(M, points, color = (0, 0, 0), p0 = None):
    R = M[0:2, 0:2]
    t = M[0:2, 2]

    points_transformed = (R @ points.T).T + t
    pygame.draw.polygon(screen, color, points_transformed, 10)

    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, points_transformed[0])
#

def main():

    text1 = font.render("Press Q, A key", True, (255,0,0))
    text2 = font.render("Press W, S key", True, (255,255,0))
    text3 = font.render("Press E, D key", True, (0,255,0))
    text4 = font.render("Grip : Press G key", True, (0,0,255))

    angle1 = 10
    angle2 = 35
    angle3 = 45
    angle4 = 0
    angle5 = 0

    width1 = 400
    width2 = 380
    width3 = 80
    width4 = 150

    height1 = 130
    height2 = 100
    height3 = 250
    height4 = 70

    rect1 = getRectangle(width1, height1)
    rect2 = getRectangle(width2, height2)
    rect3 = getRectangle(width3, height3)
    rect4 = getRectangle(width4, height4)

    gap12 = 20
    gap34 = width3/2.

    grip_Flag = 0

    done = False
    while not done:
        if grip_Flag == 1:
            angle4 -= 1
            angle5 += 1
            if angle5 == 70:
                grip_Flag = 2

        if grip_Flag == 2:
            angle4 += 1
            angle5 -= 1
            if angle5 == 0:
                grip_Flag = 0
                
        #1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_q:
                    angle1 -= 5
                elif event.key == pygame.K_a:
                    angle1 += 5
                elif event.key == pygame.K_w:
                    angle2 -= 5
                elif event.key == pygame.K_s:
                    angle2 += 5
                elif event.key == pygame.K_e:
                    angle3 -= 5
                elif event.key == pygame.K_d:
                    angle3 += 5
                if event.key == pygame.K_g:
                    rb_snd.play()
                    grip_Flag = 1
                 
        #2. logic
        center1 = [100, 200.]

        #3. drawing
        screen.fill(BLACK)

        screen.blit(text1, (WINDOW_WIDTH - 270, 100))
        screen.blit(text2, (WINDOW_WIDTH - 270, 130))
        screen.blit(text3, (WINDOW_WIDTH - 270, 160))
        screen.blit(text4, (WINDOW_WIDTH - 270, 190))

        M1 = np.eye(3) @ T3mat(center1[0], center1[1]) @ R3mat(angle1) @ T3mat(0, -height1/2.)
        draw(M1, rect1, (255, 0 ,0))
        M2 = M1 @ T3mat(width1, 0) @ T3mat(0, height1/2.) @ T3mat(gap12, 0) @ R3mat(angle2) @ T3mat(0, -height2/2.)
        draw(M2, rect2, (255, 255, 0))
        M3 = M2 @ T3mat(width2, 0) @ T3mat(0, height2/2.) @ T3mat(gap12, 0) @ R3mat(angle3) @ T3mat(0, -height3/2.)
        draw(M3, rect3, (0, 255, 0))
        M4 = M3 @ T3mat(0, height3) @ T3mat(gap34, 0) @ R3mat(angle4) @ T3mat(0, -height4/2.)
        draw(M4, rect4, (0, 0, 255))
        M5 = M3 @ T3mat(gap34, 0) @ R3mat(angle5) @ T3mat(0, -height4/2.)
        draw(M5, rect4, (0, 0, 255))
   
        pygame.draw.circle(screen, WHITE, center1, 7)

        C1 = M1 @ T3mat(width1, 0) @ T3mat(0, height1/2.)
        center2 = C1[0:2, 2]
        pygame.draw.circle(screen, WHITE, center2, 7)

        C2 = C1 @ T3mat(gap12, 0)
        center3 = C2[0:2, 2]
        pygame.draw.circle(screen, WHITE, center3, 7)

        pygame.draw.line(screen, WHITE, center2, center3, 5)

        C2 = M2 @ T3mat(width2, 0) @ T3mat(0, height2/2.)
        center3 = C2[0:2, 2]
        pygame.draw.circle(screen, WHITE, center3, 7)

        C3 = C2 @ T3mat(gap12, 0)
        center4 = C3[0:2, 2]
        pygame.draw.circle(screen, WHITE, center4, 7)

        pygame.draw.line(screen, WHITE, center3, center4, 5)

        C3 = M3 @ T3mat(0, height3)
        center4 = C3[0:2, 2]

        C4 = C3 @ T3mat(gap34, 0)
        center5 = C4[0:2, 2]
        pygame.draw.circle(screen, WHITE, center5, 7)

        C4 = M3 
        center5 = C4[0:2, 2]

        C5 = C4 @ T3mat(gap34, 0)
        center6 = C5[0:2, 2]
        pygame.draw.circle(screen, WHITE, center6, 7)

        #4.
        pygame.display.flip()
        clock.tick(30)
    #    
    pass 

if __name__ == "__main__":
    main()