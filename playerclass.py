import pygame
import constants
from spritesheet import SpriteSheet

class Player(pygame.sprite.Sprite):
    '''stores player properties & logic'''
    def __init__(self):
        super().__init__()

        #this holds spritesheet images for animated walk in dir
        
        self.walking_frames = [[ ], [ ], [ ], [ ]]
        # 0 = left 1 = right 2 = up 3 = down
        
        #load player spritesheet into an array
        sprite_sheet = SpriteSheet('fake_zelda.png')
        #left
        image = sprite_sheet.get_image(constants.WHITE, 0, 16, 16, 16)
        self.walking_frames[0].append(image)
        image = sprite_sheet.get_image(constants.WHITE, 16, 16, 16, 16)
        self.walking_frames[0].append(image)
        #right
        image = sprite_sheet.get_image(constants.WHITE, 32, 0, 16, 16)
        self.walking_frames[1].append(image)
        image = sprite_sheet.get_image(constants.WHITE, 48, 0, 16, 16)
        self.walking_frames[1].append(image)
        #up
        image = sprite_sheet.get_image(constants.WHITE, 0, 0, 16, 16)
        self.walking_frames[2].append(image)
        image = sprite_sheet.get_image(constants.WHITE, 16, 0, 16, 16)
        self.walking_frames[2].append(image)
        #down
        image = sprite_sheet.get_image(constants.WHITE, 32, 16, 16, 16)
        self.walking_frames[3].append(image)
        image = sprite_sheet.get_image(constants.WHITE, 48, 16, 16, 16)
        self.walking_frames[3].append(image)

        #motion attributes
        self.speed = 2
        self.change_x = 0
        self.change_y = 0
        self.direction = 3
        # 0 = left 1 = right 2 = up 3 = down        

        #defining s.image and s.rect is /required/ for sprite class
        self.image = self.walking_frames[self.direction][0]
        self.rect = self.image.get_rect()
        
        #set initial position: tile (11,10)
        self.rect.x = 11 * 16
        self.rect.y = 10 * 16
 
        #take in input for next step direction?
        self.next_step = True
        
        #is the player exiting a room?
        self.exit = False
        
        #stores which buttons are held, gives smoother motion
        #left right up down space
        self.button_down = [False, False, False, False, False]  
        #space
        self.interact = False
    
    def update(self):
        '''update player with tile-locked smooth movement algorithm
        later we can add SPACE interaction in a similar way
        '''
        #do we want key input yet?
        if self.rect.x % 16 == 0 and self.rect.y % 16 == 0:
            self.next_step = True
        
            #prioritize interact input
            if self.button_down[4]:
                self.next_step = not self.interact
                self.interact = not self.interact
        
        #if next_step, record key input to be used for the next 16 frames
        if self.next_step:
            self.next_step = False
            if self.button_down[0]:
                self.change_x = -self.speed
                self.change_y = 0
                self.direction = 0
            elif self.button_down[1]:
                self.change_x = self.speed
                self.change_y = 0
                self.direction = 1
            elif self.button_down[2]:
                self.change_x = 0
                self.change_y = -self.speed
                self.direction = 2
            elif self.button_down[3]:
                self.change_x = 0
                self.change_y = self.speed
                self.direction = 3
            else:
                self.change_x = 0
                self.change_y = 0
                self.next_step = True
        #regardless, update rect
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        #choose sprite frame 0 or 1 based on rect.x/y position
        #
        #change frame_freq (1,2,4,8,...) for different sprite image change rate
        #bigger number means slower-motion (with movement speed unchanged)
        #
        frame_freq = 8
        frame = (self.rect.x + self.rect.y) // frame_freq
        frame = frame % (2 * self.speed)
        frame = frame // 2
        #len(self.walking_frames[self.direction])
        self.image = self.walking_frames[self.direction][frame]