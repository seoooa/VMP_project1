# proj1-1. Clock

import pygame
import os
import numpy as np
import datetime

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
ck_snd = pygame.mixer.Sound(os.path.join(assets_path, 'ckoo.mp3'))

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
    pygame.draw.polygon(screen, color, points_transformed, 2)

    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, points_transformed[0])
#

def main():
    Now = datetime.datetime.now()

    h1 = Now.hour
    min1 = Now.minute
    sec1 = Now.second

    h2 = Now.hour
    min2 = Now.minute
    sec2 = Now.second

    h_tmp = h2
    m_tmp = min2
    s_tmp = sec2

    angle1_h = (h1 - 12) * 30 + 0.5 * min1
    angle1_min = min1 * 6 + 0.1 * sec2
    angle1_sec = sec1 * 6

    width1 = 150
    width2 = 260
    width3 = 350

    height1 = 1
    height2 = 1
    height3 = 1

    h_needle = getRectangle(width1, height1)
    m_needle = getRectangle(width2, height2)
    s_needle = getRectangle(width3, height3)

    done = False
    while not done: 

        angle1_h += 1/6000
        angle1_min += 1/500
        angle1_sec += 0.12

        angle2_h = (h2 - 12) * 30 + 0.5 * min2
        angle2_min = min2 * 6 + 0.1 * sec2
        angle2_sec = sec2 * 6

        text1 = font.render("Current Time", True, (255,255,255))

        text2_h = font.render(str(h_tmp % 24), True, (255,255,255))
        text2_m = font.render(': ' + str(m_tmp % 60), True, (255,255,255))
        text2_s = font.render(': ' + str(s_tmp % 60), True, (255,255,255))

        text3 = font.render("Press h,m,s key!", True, (255,255,255))

        if m_tmp % 60 == 0 and s_tmp % 60 == 0 :
            ck_snd.play()

        if int(angle1_min) % 360 == 0 :
            ck_snd.play()

        #1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    done = True

                elif event.key == pygame.K_h:
                    h2 += 1
                    h_tmp += 1

                elif event.key == pygame.K_m:
                    min2 += 1
                    m_tmp += 1
                    
                    if m_tmp % 60 == 0:
                        h_tmp += 1

                elif event.key == pygame.K_s:
                    sec2 += 1
                    s_tmp += 1

                    if s_tmp % 60 == 0:
                        m_tmp += 1

       
        #2. logic
        center1 = (WINDOW_WIDTH/3., WINDOW_HEIGHT/2. - 20)
        center2 = (2 * WINDOW_WIDTH/3., WINDOW_HEIGHT/2. - 20)

        #3. drawing
        screen.fill(BLACK)

        screen.blit(text1, (WINDOW_WIDTH/3. - 70, 650))

        screen.blit(text2_h, (2 * WINDOW_WIDTH/3. - 50, 600))
        screen.blit(text2_m, (2 * WINDOW_WIDTH/3.- 20, 600))
        screen.blit(text2_s, (2 * WINDOW_WIDTH/3. + 30, 600))

        screen.blit(text3, (2 * WINDOW_WIDTH/3. - 80, 650))

        pygame.draw.circle(screen, (255,255,255), center1, 100, 1)
        pygame.draw.circle(screen, (255,255,255), center2, 100, 1)

        M1 = T3mat(center1[0], center1[1]) @ T3mat(0, -height1/2.)
        M2 = T3mat(center2[0], center2[1]) @ T3mat(0, -height1/2.)

        #hour
        M1_H = M1 @ T3mat(0, height1/2.) @R3mat(-90 + angle1_h) @T3mat(0, -height1/2.)
        M2_H = M2 @ T3mat(0, height1/2.) @R3mat(-90 + angle2_h) @T3mat(0, -height1/2.)
        draw(M1_H, h_needle, (255, 255, 255))
        draw(M2_H, h_needle, (255, 255, 255))

        #minute
        M1_M = M1 @ T3mat(0, height1/2.) @ R3mat(-90 + angle1_min) @ T3mat(0, -height1/2.)
        M2_M = M2 @ T3mat(0, height1/2.) @ R3mat(-90 + angle2_min) @ T3mat(0, -height1/2.)
        draw(M1_M, m_needle, (255, 255, 255))
        draw(M2_M, m_needle, (255, 255, 255))

        #second
        M1_S = M1 @ T3mat(0, height1/2.) @ R3mat(-90 + angle1_sec) @ T3mat(0, -height1/2.)
        M2_S = M2 @ T3mat(0, height1/2.) @ R3mat(-90 + angle2_sec) @ T3mat(0, -height1/2.)
        draw(M1_S, s_needle, (255, 255, 255))
        draw(M2_S, s_needle, (255, 255, 255))

        pygame.draw.circle(screen, (255, 255, 255), center1, 5)
        pygame.draw.circle(screen, (255, 255, 255), center2, 5)

        #4.
        pygame.display.flip()
        clock.tick(50)
    #    
    pass 

if __name__ == "__main__":
    main()