import numpy as np
import pygame as pg

def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    running = True
    pg.mouse.set_visible(False)
    clock = pg.time.Clock()
    hres = 120
    halfvres = 100 # half of vertical resolution
    mod = hres/60
    posx, posy, rot = 0,0,0
    floor = pg.surfarray.array3d(pg.image.load('floor.jpg'))
    kart = pg.surfarray.array3d(pg.image.load('MarioKart.png'))
    sky = pg.image.load('skybox.jpg')
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, halfvres*2)))
    ns = halfvres/((halfvres+0.1-np.linspace(0, halfvres, halfvres)))# depth
    cos22 = np.cos(np.deg2rad(np.linspace(-30,30, hres)/mod)) # perspective correction
    shade = 0.4 + 0.6*(np.linspace(0, halfvres, halfvres)/halfvres)
    shade = np.dstack((shade, shade, shade))

    frame = np.ones([hres, halfvres*2, 3])
    while running: #main game loop
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        for i in range(hres):
            rot_i = rot + np.deg2rad(i/mod - 30)
            sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i/mod-30))
            frame[i][:halfvres] = sky[int(np.rad2deg(rot_i)%360)][:halfvres]/255
            xs, ys = posx+ns*cos/cos2, posy+ns*sin/cos2
            xxs, yys = (xs/30%1*1023).astype('int'), (ys/30%1*1023).astype('int')
            frame[i][2*halfvres-len(ns):2*halfvres] = shade*kart[np.flip(xxs),np.flip(yys)]/255
                          
        surf = pg.surfarray.make_surface(frame*255)
        surf = pg.transform.scale(surf, (800, 600))
        screen.blit(surf, (0, 0))
        pg.display.update()

        pressed_keys = pg.key.get_pressed()        
        posx, posy, rot = movement(pressed_keys,posx, posy, rot, clock.tick()/500)
        pg.mouse.set_pos([300, 400])

        fps = int(clock.get_fps())
        pg.display.set_caption("Pycasting maze - FPS: " + str(fps))
        

    pg.quit()

def movement(pressed_keys,posx, posy, rot, et):
    
    x, y = (posx, posy)
    
    p_mouse = pg.mouse.get_pos()
    rot = rot - 4*np.pi*(0.5-(p_mouse[0]-300)/6400)
    
    if pressed_keys[pg.K_UP] or pressed_keys[ord('w')]:
        x, y = (x + et*np.cos(rot), y + et*np.sin(rot))
        
    if pressed_keys[pg.K_DOWN] or pressed_keys[ord('s')]:
        x, y = (x - et*np.cos(rot), y - et*np.sin(rot))
        
    if pressed_keys[pg.K_LEFT] or pressed_keys[ord('a')]:
        x, y = (x + et*np.sin(rot), y - et*np.cos(rot))
        
    if pressed_keys[pg.K_RIGHT] or pressed_keys[ord('d')]:
        x, y = (x - et*np.sin(rot), y + et*np.cos(rot))
        
    posx, posy = (x, y)
                                                
    return posx, posy, rot

if __name__ == '__main__':
    main()
