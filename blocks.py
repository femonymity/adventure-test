import pygame

class Block(pygame.sprite.Sprite):
    '''this class represents all tiles that obstruct player movement
    '''
    def __init__(self, image, x, y):
        '''pass in block image and location'''
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y