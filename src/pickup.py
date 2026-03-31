from random import randint


class Pickup:
    """This class creates a certain pickup."""

    def __init__(self, game, drop):
        """Initialize attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.x = 400
        self.y = 100
        self.image = drop
        self.rect = self.image.get_rect()
    
    def check_spawn(self):
        # checks, if a collectible appears at a given chance
        value = randint(1, 1000)
        if value <= 333 and not self.game.active_drop:
        # if value <= 500:
            # if len(self.game.drops_collected) <= 4:
                return True

    def update(self):
        # Update position of pickup.
        self.y += self.settings.pickup_speed

    def drawme(self):
        # Draw pickup to the screen.
        if not self.rect.top >= self.screen_rect.bottom: 
            self.screen.blit(self.image, (self.x, self.y))