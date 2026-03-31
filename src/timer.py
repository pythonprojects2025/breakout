import pygame


class Timer:
    """This class builds a timer, to show the remaining bonus-time."""
    
    def __init__(self, game):
        """Initialize timer attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings

        self.dmgup_image = game.dmgup_image
        self.widthup_image = game.widthup_image
        self.dmgup_image = pygame.transform.scale(self.dmgup_image, (20, 20))
        self.widthup_image = pygame.transform.scale(
                                self.widthup_image, (20, 20))
        
        self.x = 130
        self.y = 10
        self.value = 180
        self.label_rect = pygame.Rect(self.x, self.y, 180, 20)
        self.reset()

    def reset(self):
        # Reset the timer.
        self.collected = False
        self.value = 180
        self.value_rect = pygame.Rect(self.x, self.y, self.value, 20)
    
    def update(self):
        # Timer starts counting down, once a pickup is collected.
        if self.collected:
            if self.value <= 0:
                self.collected = False
                self.value = 180
                self.value_rect = pygame.Rect(self.x, self.y, self.value, 20)
                self.game.drops_collected.append(self.game.active_drop)
                self.game.active_drop = ""
                self.game.pickup_collected = False
            elif self.value > 0: 
                if self.game.active_drop == "widthup":
                    self.value -= 0.21
                elif self.game.active_drop == "dmgup":
                    self.value -= 0.33
                self.value_rect = pygame.Rect(self.x, self.y, self.value, 20)

    def drawme(self):  
        # Drawing timer on the screen if not time is up.
        if self.collected and self.value > 0:     
            pygame.draw.rect(self.screen, (234, 234, 234), (self.label_rect))
            pygame.draw.rect(self.screen, (24, 24, 34), (self.value_rect))
        if self.game.active_drop == "dmgup":
            self.screen.blit(self.dmgup_image, (320, 10))
        if self.game.active_drop == "widthup":
            self.screen.blit(self.widthup_image, (320, 10))
