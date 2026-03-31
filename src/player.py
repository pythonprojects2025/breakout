import pygame


class Player:
    """This class builds the player platform."""
    
    def __init__(self, game):
        """Initialize player attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.width = self.settings.player_width
        self.height = 30
        self.x = 400 - self.width/2
        self.x = float(self.x)
        self.y = self.screen_rect.height - self.height - 9
        self.speed = self.settings.player_speed
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (123, 123, 123)

        self.moving_left = False
        self.moving_right = False
        
    def update(self):
        # Update position of platform for each frame.
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.moving_left == True and self.x > 0:
            self.x -= self.speed

        if (self.moving_right == True and 
            self.x < self.game.settings.screen_width - self.width):
            self.x += self.speed

        self.rect.x = self.x

    def drawme(self):
        # Drawing the platform on the screen.
        pygame.draw.rect(self.screen, self.color, (self.rect))
        pygame.draw.rect(self.screen, (60, 60, 60), (self.rect), 2)

