import pytmx
import pygame

pygame.init()

SCREEN = (384,384)
screen = pygame.display.set_mode(SCREEN)
clock = pygame.time.Clock()

#load map data
gamemap = pytmx.load_pygame('test.tmx')

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    #draw map data on screen
    for layer in gamemap.visible_layers:
        for x, y, gid, in layer:
            tile = gamemap.get_tile_image_by_gid(gid)
            if tile:
                screen.blit(tile, (x * gamemap.tilewidth, y * gamemap.tileheight))
    
    
    pygame.display.flip()    
    clock.tick(60)

pygame.quit()