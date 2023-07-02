# proj1-4. LP Player

import pygame
import os
import numpy as np

WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#pygame init
pygame.init()
pygame.display.set_caption("20211511 김서아")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')

#폰트 로드
font = pygame.font.SysFont("arial", 30, True, True)

def getRegularPolygon(N, Radius = 1):
    v = []
    for i in range(N):
        rad = i * 2 * np.pi / N

        x = np.cos(rad) * Radius
        y = np.sin(rad) * Radius

        v.append([x, y])
    
    vnp = np.array(v)

    return vnp

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
    pygame.draw.polygon(screen, color, points_transformed, 0)

    if p0 is not None:
        pygame.draw.line(screen, color, p0, points_transformed[0])
#

def music_select(music, m_select):

    if m_select == 1:
        music = pygame.mixer.Sound(os.path.join(assets_path, 'calltosoul.mp3'))
    elif m_select == 2:
        music = pygame.mixer.Sound(os.path.join(assets_path, 'weeknds.mp3'))
    else:
        music = pygame.mixer.Sound(os.path.join(assets_path, 'summerwalk.mp3'))

    return music

def main():

    #효과음 로드
    music1 = pygame.mixer.Sound(os.path.join(assets_path, 'summerwalk.mp3'))

    color1 = WHITE
    color2 = GRAY
    color3 = GRAY

    text1 = font.render("Summer Walk - Olexy", True, BLACK)
    text2 = font.render("Call to Soul - markotopa", True, BLACK)
    text3 = font.render("Weeknds - DayFox", True, BLACK)

    text4 = font.render("Select music by N key", True, (15,15,15))
    text5 = font.render("You can move it by Direction key", True, (15,15,15))
    text6 = font.render("Press Space bar", True, (15,15,15))

    play_Flag = 0
    sound_Flag = 0
    one_Flag = 0

    m_select = 0
    space_cnt = 0

    LP1 = getRegularPolygon(40, 450)
    LP2 = getRegularPolygon(40, 150)

    angle = 0
    angle1 = -15
    angle2 = 90

    width1 = 500
    width2 = 100

    height1 = 15
    height2 = 15

    rect1 = getRectangle(width1, height1)
    rect2 = getRectangle(width2, height2)

    done = False
    while not done:
        angle += 3

        #1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_UP:
                    angle1 -= 5
                elif event.key == pygame.K_DOWN:
                    angle1 += 5
                elif event.key == pygame.K_SPACE:
                    space_cnt += 1
                    if space_cnt % 2 == 1:
                        play_Flag = 1
                    else:
                        play_Flag = 0

                        music1.stop()
                        sound_Flag = 0
                        one_Flag = 0

                elif event.key == pygame.K_n:
                    m_select += 1
                    m_select %= 3

                    music1.stop()
                    sound_Flag = 0
                    one_Flag = 0
                    music1 = music_select(music1, m_select)

                    if m_select == 1:
                        color1 = GRAY
                        color2 = WHITE
                        color3 = GRAY
                    elif m_select == 2:
                        color1 = GRAY
                        color2 = GRAY
                        color3 = WHITE
                    else:
                        color1 = WHITE
                        color2 = GRAY
                        color3 = GRAY
       
        #2. logic

        #3. drawing
        screen.fill(GRAY)

        pygame.draw.rect(screen, color1, [WINDOW_WIDTH - 330, 105, 300, 50])
        pygame.draw.rect(screen, color2, [WINDOW_WIDTH - 330, 155, 300, 50])
        pygame.draw.rect(screen, color3, [WINDOW_WIDTH - 330, 205, 300, 50])

        screen.blit(text1, (WINDOW_WIDTH - 320, 110))
        screen.blit(text2, (WINDOW_WIDTH - 320, 160))
        screen.blit(text3, (WINDOW_WIDTH - 320, 210))
        screen.blit(text4, (WINDOW_WIDTH - 370, 60))
        screen.blit(text5, (20, 20))
        screen.blit(text6, (WINDOW_WIDTH/2. - 100, WINDOW_HEIGHT/3.- 60))

        center = (WINDOW_WIDTH/2., WINDOW_HEIGHT - 80)

        MLP1 = T3mat(center[0], center[1])
        draw(MLP1, LP1, (0, 0, 0), center)
        MLP2 = T3mat(center[0], center[1]) 
        draw(MLP2, LP2, (230, 0, 0), center)

        if play_Flag == 1:
            MLP1 = T3mat(center[0], center[1]) @ R3mat(angle)
            draw(MLP1, LP1, (0, 0, 0), center)
            MLP2 = T3mat(center[0], center[1]) @ R3mat(angle)
            draw(MLP2, LP2, (230, 0, 0), center)

        center1 = [0, 200.]
        M1 = np.eye(3) @ T3mat(center1[0], center1[1]) @ R3mat(angle1) @ T3mat(0, -height1/2.)
        draw(M1, rect1, (0, 0 ,0))
        
        M2 = M1 @ T3mat(width1, 0) @ R3mat(angle2) @ T3mat(0, -height2/2.)
        draw(M2, rect2, (0, 0, 0))

        C1 = M2 @ T3mat(width2, 0) @ T3mat(0, height2/2.)
        center2 = C1[0:2, 2]
        pygame.draw.circle(screen, BLACK, center2, 7)

        if play_Flag == 1 and sound_Flag == 0:
           if angle1 % 360 >= 10 and angle1  % 360 <= 40:
               sound_Flag = 1
        
        if sound_Flag == 1:
            if angle1 % 360 < 10 or angle1  % 360 > 40:
                music1.stop()
                sound_Flag = 0
                one_Flag = 0
            elif one_Flag == 0:
                one_Flag = 1
                music1.play()

        #4.
        pygame.display.flip()
        clock.tick(30)
    #    
    pass 

if __name__ == "__main__":
    main()