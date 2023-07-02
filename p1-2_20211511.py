# proj1-2. Solar System

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

#효과음 로드
a_snd = pygame.mixer.Sound(os.path.join(assets_path, 'alien.mp3'))

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
        pygame.draw.line(screen, color, p0, points_transformed[0])
#

def main():
    text = font.render("When you press W key, an alien spaceship appears", True, GREEN)

    angle  = 0
    angleSP1 = 0
    angleP1 = 0
    angleM1 = 0
    angleP1M1 = 0

    angleSP2 = 0
    angleP2 = 0
    angleM2 = 0
    angleP2M2 = 0

    angleM3 = 0
    angleP2M3 = 0

    angleM4 = 0
    angleM3M4 = 0

    WP = 0
    angle_A = 0

    Sun = getRegularPolygon(40, 100)
    Planet1 = getRegularPolygon(40, 50)
    Planet2 = getRegularPolygon(40, 70)
    Moon1 = getRegularPolygon(4, 30)
    Moon2 = getRegularPolygon(5, 40)
    Moon3 = getRegularPolygon(6, 20)
    Moon4 = getRegularPolygon(10, 10)

    Alien = getRegularPolygon(3, 20)

    distSP1 = 300
    distP1M1 = 130

    distSP2 = 500
    distP2M2 = 150

    distP2M3 = 130

    distM3M4 = 50

    dist_A = 100

    done = False
    while not done:
        angle += 3
        angleSP1 += 1
        angleP1 += 5
        angleM1 += 7
        angleP1M1 += 10

        angleSP2 += 2
        angleP2 += 5
        angleM2 += 7
        angleP2M2 += 2

        angleM3 += 7
        angleP2M3 += 5

        angleM4 += 10
        angleM3M4 += 3

        angle_A += 4

        #1. event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    done = True

                if event.key == pygame.K_w:
                    WP = np.random.randint(1, 5)
                    a_snd.play()
       
        #2. logic

        #3. drawing
        screen.fill(BLACK)
        screen.blit(text, (WINDOW_WIDTH/3. - 50, 10))

        center = (WINDOW_WIDTH/2., WINDOW_HEIGHT/2.)
        Msun = T3mat(center[0], center[1]) @ R3mat(angle)
        draw(Msun, Sun, (250, 100, 50), center)

        Mplanet1 = T3mat(center[0], center[1]) @ R3mat(angleSP1) @ T3mat(distSP1, 0) @ R3mat(-angleSP1) @ R3mat(angleSP1)
        draw(Mplanet1, Planet1, (100, 5, 50), Mplanet1[:2, 2])

        Mmoon1 = Mplanet1 @ R3mat(angleP1M1) @ T3mat(distP1M1, 0) @ R3mat(-angleM1) @ R3mat(angleM1)
        draw(Mmoon1, Moon1, (0, 50, 255), Mmoon1[:2, 2])

        Mplanet2 = T3mat(center[0], center[1]) @ R3mat(angleSP2) @ T3mat(distSP2, 0) @ R3mat(-angleSP2) @ R3mat(angleSP2)
        draw(Mplanet2, Planet2, (100, 5, 150), Mplanet2[:2, 2])

        Mmoon2 = Mplanet2 @ R3mat(angleP2M2) @ T3mat(distP2M2, 0) @ R3mat(-angleM2) @ R3mat(angleM2)
        draw(Mmoon2, Moon2, (255, 228, 0), Mmoon2[:2, 2])

        Mmoon3 = Mplanet2 @ R3mat(angleP2M3) @ T3mat(distP2M3, 0) @ R3mat(-angleM3) @ R3mat(angleM3)
        draw(Mmoon3, Moon3, (255, 0, 127), Mmoon3[:2, 2])

        Mmoon4 = Mmoon3 @ R3mat(angleM3M4) @ T3mat(distM3M4, 0) @ R3mat(-angleM4) @ R3mat(angleM4)
        draw(Mmoon4, Moon4, (0, 100, 100), Mmoon4[:2, 2])

        #Alien Wadering
        if WP == 1:
            Malien = T3mat(center[0], center[1]) @ R3mat(angle_A) @ T3mat(dist_A + 50, 0) @ R3mat(-angle_A) @ R3mat(angle_A)
            draw(Malien, Alien, GREEN, Malien[:2, 2])
        elif WP == 2:
            Malien = Mplanet1 @ R3mat(angle_A) @ T3mat(dist_A - 30, 0) @ R3mat(-angle_A) @ R3mat(angle_A)
            draw(Malien, Alien, GREEN, Malien[:2, 2])
        elif WP == 3:
            Malien = Mplanet2 @ R3mat(angle_A) @ T3mat(dist_A - 10, 0) @ R3mat(-angle_A) @ R3mat(angle_A)
            draw(Malien, Alien, GREEN, Malien[:2, 2])
        elif WP == 4:
            Malien = Mmoon3 @ R3mat(angle_A) @ T3mat(dist_A - 30, 0) @ R3mat(-angle_A) @ R3mat(angle_A)
            draw(Malien, Alien, GREEN, Malien[:2, 2])

        #4.
        pygame.display.flip()
        clock.tick(30)
    #    
    pass 

if __name__ == "__main__":
    main()