import pygame
from pygame.sprite import Sprite


class Block(Sprite):
    """This class builds a block at given coordnates and color."""
    
    def __init__(self, game, x, y, color):
        """Initialize block attributes."""
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        
        self.color = self.get_color(color)
        self.points = self.get_points(color)
        self.hp = self.get_hp(color)

        self.x = x
        self.y = y
        self.width = 59.66
        self.height = 39.66
        # self.width = int(60)
        # self.height = int(40)
        self.rect = pygame.Rect(self.x + 3, self.y + 2,
                                self.width, self.height)
        
        self.surface = pygame.Surface((self.width, self.height))
        self.mask = pygame.mask.from_surface(self.surface)

        self.visible = True

    def get_color(self, col):
        # Get RGB tuple for color.
        if col == "blue":
            return (103, 182, 189)
        elif col == "red":
            return (234, 145, 130)
        elif col == "orange":
            return (234, 201, 201)
        elif col == "violet":
            return (184, 105, 98)
        elif col == "yellow":
            return (245, 238, 155)
        
    def get_points(self, col):
        # Define the points of a block with a given color.
        if col == "blue":
            return 100
        elif col == "red":
            return 200
        elif col == "orange":
            return 300
        elif col == "violet":
            return 400
        elif col == "yellow":
            return 500
        
    def get_hp(self, col):
        # Get the hp of a block with a given color.
        if col == "blue":
            return 1
        elif col == "red":
            return 2
        elif col == "orange":
            return 3
        elif col == "violet":
            return 4
        elif col == "yellow":
            return 5

    def check_hp(self):     
        if self.hp <= 0:
            self.visible = False
    
    def check_color(self, hp):
        # Changes color, if hp of block is lowered.
        if hp == 1:
            return (103, 182, 189)
        elif hp == 2:
            return (234, 145, 130)
        elif hp == 3:
            return (234, 201, 201)
        elif hp == 4:
            return (184, 105, 98)
        elif hp == 5:
            return (245, 238, 155)

    def update(self):
        self.check_hp()
        self.color = self.check_color(self.hp)

    def drawme(self):
        # Drawing block on the screen.
        if self.visible:
            pygame.draw.rect(self.screen, self.color, self.rect)
            pygame.draw.rect(self.screen, (20, 20, 20), self.rect, 2)