'''
My First Adventure Game Project
-------------------------------
made with the help of
https://github.com/justinmeister/PyTMX-Examples/blob/master/Making%20a%20map%20surface/tilerender.py
for help with pygame:
google sentdex tutorial on youtube
or search for pytmx on here youtube.com/c/KidsCanCodeOrg
Tiled Map Editor Tutorial:
https://www.youtube.com/watch?v=mJZQabPyTHo
and of course, Dr Craven's crash course in making games with python/pygame
http://programarcadegames.com/index.php?lang=en
'''
import pygame
import pytmx
import constants
from spritesheet import SpriteSheet
from blocks import Block
from playerclass import Player
import rooms

class Game():

    def __init__(self):
        '''game constructor: create attributes, start game'''

        #initialize sprite lists
        self.all_sprites_list = pygame.sprite.Group()

        #initialize room list
        self.room_list = [ ]
        self.room_list.append(rooms.Home())
        self.room_list.append(rooms.InsideHome())
        self.room_list.append(rooms.Beach())

        #spawn in this room
        self.current_room = self.room_list[1]

        #make a player sprite
        self.player = Player()
        self.all_sprites_list.add(self.player)

    def process_events(self):
        '''process all events. keystrokes, clicks, exit'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.button_down[0] = True
                elif event.key == pygame.K_RIGHT:
                    self.player.button_down[1] = True
                elif event.key == pygame.K_UP:
                    self.player.button_down[2] = True
                elif event.key == pygame.K_DOWN:
                    self.player.button_down[3] = True
                elif event.key == pygame.K_SPACE:
                    print('space!')
                    self.player.button_down[4] = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.button_down[0] = False
                elif event.key == pygame.K_RIGHT:
                    self.player.button_down[1] = False
                elif event.key == pygame.K_UP:
                    self.player.button_down[2] = False
                elif event.key == pygame.K_DOWN:
                    self.player.button_down[3] = False
                elif event.key == pygame.K_SPACE:
                    self.player.button_down[4] = False
        return False

    def run_logic (self):
        '''this is run each frame. it updates positions &
        checks for collisions'''

        #update positions of sprites (aka just the player)
        self.all_sprites_list.update()

        #check for collisions
        hitblock = pygame.sprite.spritecollideany(self.player, self.current_room.wall_list)
        if hitblock:
            #if player bumps up/down, correct it
            dify = self.player.rect.centery - hitblock.rect.centery
            if dify < 0: #player above
                self.player.rect.bottom = hitblock.rect.top
            elif dify > 0: #player below
                self.player.rect.top = hitblock.rect.bottom
            #if player bumps left/right, correct it
            difx = self.player.rect.centerx - hitblock.rect.centerx
            if difx < 0: #player to the left
                self.player.rect.right = hitblock.rect.left
            elif difx > 0:
                self.player.rect.left = hitblock.rect.right

        #check for exiting
        hitblock = pygame.sprite.spritecollideany(self.player, self.current_room.exit_list)
        if hitblock:
            #if player has finished moving onto exit, exit to next room!
            if self.player.rect.center == hitblock.rect.center:
                print('bonk!')
                self.current_room = self.room_list[hitblock.nextroom]
                self.player.rect.x = hitblock.nextrect.x
                self.player.rect.y = hitblock.nextrect.y

        #check for interacting
        #first check if there is an interactible block one block over
        #from where the player stands, in the direction player is facing
        #
        #if yes, print that tile's interaction text in a text box
        #
        #freeze movement input until textbox is exited using space



    def display_frame(self,screen):

        screen.fill(constants.BLACK)

        #this is where we blit the tilemap to screen
        for layer in self.current_room.gamemap.visible_layers:
            for x, y, gid, in layer:
                tile = self.current_room.gamemap.get_tile_image_by_gid(gid)
                if tile:
                    #tile.set_colorkey(constants.WHITE)
                    screen.blit(tile, (x * self.current_room.gamemap.tilewidth, y * self.current_room.gamemap.tileheight))


        self.all_sprites_list.draw(screen)
        #self.current_room.exit_list.draw(screen)

        pygame.display.flip()


def main():

    pygame.init()

    SCREEN = (384, 384)
    screen = pygame.display.set_mode(SCREEN)

    done = False
    game = Game()
    clock = pygame.time.Clock()

    while not done:

        done = game.process_events()

        #game logic
        game.run_logic()

        game.display_frame(screen)

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
