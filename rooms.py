import pygame
import pytmx
from blocks import Block

class Room():
    '''base class for each new room in the game world.
    make a subclass for each room.'''
    def __init__(self):
        '''Each room should have:
        * an index number
        * a name
        * a gamemap
        * a list of wall blocks
        * a list of exits <- make exits sprites!
        * a list of npc sprites
        '''
        #self.gamemap = None
        self.exit_list = pygame.sprite.Group()
    
    def get_tile_list(self,layer):
        '''given a map & specified layer, returns a Group of Block sprites
        on each tile in that layer
        '''
        block_list = pygame.sprite.Group()

        #get block layer
        blocklayer = self.gamemap.get_layer_by_name(layer)
        #make a bunch of blocks, one for each collidable tile
        for x, y, gid in blocklayer:
            tile = self.gamemap.get_tile_image_by_gid(gid)
            if tile:
                blockx = x * self.gamemap.tilewidth
                blocky = y * self.gamemap.tileheight
                block = Block(tile,blockx,blocky)
                block_list.add(block)
        
        return block_list

class Exit(pygame.sprite.Sprite):
    '''class for Exit sprites:
    invisible tiles that teleport u to a new room or tile when collided with
    '''
    def __init__(self, tilex, tiley, newindex, newtilex, newtiley):
        super().__init__()
        #give it a blank image
        self.image = pygame.Surface((16, 16)).convert()
        self.image.fill((0,0,255))
        self.rect = self.image.get_rect()
        self.rect.x = tilex * 16
        self.rect.y = tiley * 16
        self.nextroom = newindex
        self.nextrect = pygame.Rect(newtilex * 16, newtiley * 16, 16, 16)

class Home(Room):
    '''class for the room with player's home in it
    '''
    def __init__(self):
        super().__init__()
        
        self.index = 0
        self.name = 'home'
        self.gamemap = pytmx.load_pygame('lpc-tileset-16x16/test.tmx')
        self.wall_list = self.get_tile_list('Wall Layer')
        
        #add exits here
        #
        #door exit at tile (9, 15)
        #leads to room index 1, tile (11,14)
        exit = Exit(9, 15, 1, 11, 14)
        self.exit_list.add(exit)
        # + etc
        #south exit to beach (12, 24) - (19, 24)
        for i in range(12,20):
            exit = Exit(i, 24, 2, i, 0)
            self.exit_list.add(exit)        
        
        #add npcs here
        self.npc_list = pygame.sprite.Group()

class InsideHome(Room):
    '''class map for inside players home'''
    def __init__(self):
        super().__init__()
        
        self.index = 1
        self.name = 'inside_home'
        self.gamemap = pytmx.load_pygame('lpc-tileset-16x16/home_inside.tmx')
        self.wall_list = self.get_tile_list('Wall Layer')
        
        #add exits here
        #
        #door exit at tile (11, 15)
        #leads to room index 0, tile (9, 16)
        exit = Exit(11, 15, 0, 9, 16)
        self.exit_list.add(exit)

class Beach(Room):
    '''class map for beach south of home'''
    def __init__(self):
        super().__init__()
        
        self.index = 2
        self.name = 'beach'
        self.gamemap = pytmx.load_pygame('lpc-tileset-16x16/beach.tmx')
        self.wall_list = self.get_tile_list('Wall Layer')
        
        #add exits here
        #
        #north exit on tiles (12, -1) - (19, -1)
        for i in range(12,20):
            exit = Exit(i, -1, 0, i, 23)
            self.exit_list.add(exit)