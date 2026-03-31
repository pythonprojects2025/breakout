import pygame
import sys
from random import randint, choice
from time import *

from player import Player
from settings import Settings
from ball import Ball
from block import Block
from button import Button
from scorelabel import Scorelabel
from pickup import Pickup
from timer import Timer
from highscore import Highscore


class Game:
    """Main gameclass."""

    def __init__(self):
        """Initialize attributes"""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()   
        self.fps = 60
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height)) 
              
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Game")   
        self.bg_color = self.settings.bg_color

        self.load_images()
        self.intro_sound = pygame.mixer.Channel(0).play(
                                pygame.mixer.Sound('sound/intro.mp3'))   
        
        self.tracks = [1, 2, 3, 4, 5]
        self.level_sound = self.load_sound()

        self.ball_speed = self.settings.ball_speed  
        self.play_button = Button(self, "Play!")
        self.platform = Player(self)
        self.ball = Ball(self, self.platform.rect.center[0])
        self.scorelabel = Scorelabel(self)
        self.pickup = Pickup(self, self.lifeup_image)
        self.timer = Timer(self)
           
        self.blocks = []
        self.level_pos = []
        self.active_drop = ""
        self.drops_collected = []
        self.active_balls = []    
        self.points = 0
        self.current_level = 1
        self.lives = self.settings.lives
        self.bonus = ""
        
        self.game_active = False
        self.level_running = False
        self.pickup_visible = False
        self.pickup_collected = False
        self.endscreen_visible = False
        self.winscreen_visible = False
        self.ball_lost = False
        self.level_up = False

        self.load_level_pos(self.current_level)
        self.highscore = Highscore(self)
        
    def run_game(self):  
        # Main game loop.   
        while True:
            self.check_events()

            if self.game_active:
                if self.ball_lost:
                    pygame.time.delay(1000)
                    self.ball_lost = False
                if self.level_up:
                    self.load_new_sound()

                self.platform.update()
                for ball in self.active_balls:
                    ball.update()                
                
                if self.level_running:
                    self.check_block_collision()
                    self.update_blocks()
                    self.check_level_end()
                    self.bonus_action(self.active_drop)
                    if self.pickup_visible:
                        self.pickup.update()
                        self.check_pickup()
                    self.timer.update()

                self.scorelabel.prep_score(self.points)
            self.update_screen()  
            self.clock.tick(self.fps)

    def check_events(self):
        # check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()          

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

            if self.game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.platform.moving_left = True
                    if event.key == pygame.K_RIGHT:
                        self.platform.moving_right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.platform.moving_left = False
                    if event.key == pygame.K_RIGHT:
                        self.platform.moving_right = False

    def load_images(self):
        self.title_screen = pygame.image.load("images/title_screen.png")
        self.end_screen = pygame.image.load("images/end_screen.png")
        self.ball_lost_screen = pygame.image.load("images/ball_lost.png")
        self.levelup_screen = pygame.image.load("images/levelup.png")
        self.dmgup_image = pygame.image.load("images/dmg_up.png")
        self.lifeup_image = pygame.image.load("images/life_up.png")
        self.widthup_image = pygame.image.load("images/width_up.png")
        self.multiball_image = pygame.image.load("images/multiball.png")
        self.winscreen_image = pygame.image.load("images/win_screen.png")
     
    def load_sound(self):
        if self.tracks:
            track = choice(self.tracks)
        elif not self.tracks:
            self.tracks = [1, 2, 3, 4, 5]
            track = choice(self.tracks)

        if track == 1:
            self.tracks.remove(1)
            return "sound/level_a.mp3"          
        elif track == 2:
            self.tracks.remove(2)
            return "sound/level_b.mp3"
        elif track == 3:
            self.tracks.remove(3)
            return "sound/level_c.mp3"
        elif track == 4:
            self.tracks.remove(4)
            return "sound/level_d.mp3"
        elif track == 5:
            self.tracks.remove(5)
            return "sound/level_e.mp3"
        
    def load_new_sound(self):
        if self.current_level <= 7:
            pygame.time.delay(1800)
            self.level_up = False
            self.level_sound = self.load_sound()
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound(self.level_sound))
            
    def check_play_button(self, mouse_pos):
        # Start a new game when button is clicked and reset game stats.
        if not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                pygame.mixer.Channel(1).play(
                    pygame.mixer.Sound('sound/blib.mp3'))
                sleep(1)
                self.points = 0
                self.current_level = 1
                self.level_pos = []
                self.blocks = []
                self.bonus = ""
                self.active_drop = ""
                self.drops_collected = []
                self.active_balls = []
                
                self.load_level_pos(self.current_level)
                self.get_blocks()               
                self.active_balls.append(self.ball)
                self.ball.start_pos()
                self.ball_speed = self.settings.ball_speed
                self.platform.speed = self.settings.player_speed
                self.lives = self.settings.lives   
                self.tracks = [1, 2, 3, 4, 5]
         
                self.level_running = False
                self.game_active = True
                self.pickup_visible = False
                self.pickup_collected = False
                self.timer.value = 180
                self.timer.collected = False
                self.endscreen_visible = False
                self.platform.moving_left = False
                self.platform.moving_right = False
                self.highscore.grats = False
                pygame.mouse.set_visible(False)
                self.scorelabel.prep_level(self.current_level)

                self.level_sound = self.load_sound()
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound(self.level_sound)) 
    
    def check_bonus(self, block):
        # Checks if a drop will spawn, loads the image and build the pickup.
        bonus = self.pickup.check_spawn()
        if bonus and not self.pickup_visible and not self.active_drop:
            image = self.chose_pickup()
            if not self.bonus in self.drops_collected or self.bonus == 'multiball':
                self.create_pickup(block.rect, image)
                pygame.mixer.Channel(2).play(
                    pygame.mixer.Sound('sound/spawn.mp3'))    
                         
    def chose_pickup(self):
        # Get the sort of the pickup at a given chance, if one is created.
        value = randint(1, 1000)
        if value > 666:
            self.bonus = "widthup"
            return self.widthup_image
        elif value <= 666 and value > 333 :
            self.bonus = "dmgup"
            return self.dmgup_image
        if value <= 333 and value >= 90:
            self.bonus = "multiball"
            return self.multiball_image
        elif value < 90:
            self.bonus = "lifeup"
            return self.lifeup_image
        
    def create_pickup(self, rect, image):
        self.pickup = Pickup(self, image)
        self.pickup.x = rect.x
        self.pickup.y = rect.y
        self.pickup_visible = True

    def check_pickup(self):    
        # checks, if the drop is either collected or lost 
        self.pickup_rect = pygame.Rect(self.pickup.x, self.pickup.y, 40, 40)
        
        if self.pickup_rect.colliderect(self.platform.rect):
            if self.bonus == "multiball":
                pygame.mixer.Channel(2).play(
                    pygame.mixer.Sound('sound/multiball.mp3'))
            else:
                pygame.mixer.Channel(2).play(
                    pygame.mixer.Sound('sound/pickupget.mp3'))
                
            if self.pickup_visible and not self.pickup_collected:
                if self.bonus == "lifeup" and not self.lives >= 4:
                    self.lives += 1
                if self.bonus == "multiball":
                    self.get_multiball()

                self.pickup_collected = True
                self.pickup_visible = False   
                self.active_drop = self.bonus                              
                self.bonus = ""
                self.timer.collected = True
            
        if (self.pickup_rect.top > self.screen_rect.bottom and 
            self.pickup_visible):           
            self.pickup_visible = False
            self.active_drop = ""
            self.bonus = ""

    # def get_multiball(self):
    #     self.ball_2 = Ball(self, self.platform.rect.center[0])
    #     self.ball_2.speed_x = self.ball_speed + 0.3
    #     self.ball_3 = Ball(self, self.platform.rect.center[0])
    #     self.ball_3.speed_x = -self.ball_speed + 0.3
    #     self.active_balls.append(self.ball_2)
    #     self.active_balls.append(self.ball_3)

    def get_multiball(self):
        ball = Ball(self, self.platform.rect.center[0])
        ball.speed_x = self.ball_speed + 0.15
        # self.ball_3 = Ball(self, self.platform.rect.center[0])
        # self.ball_3.speed_x = -self.ball_speed + 0.3
        self.active_balls.append(ball)
        ball = Ball(self, self.platform.rect.center[0])
        ball.speed_x = -self.ball_speed + 0.15
        self.active_balls.append(ball)

    def bonus_action(self, drop):
        # Changes the values for damage and platform-width when a bonus-drop 
        # is colleted and reset values if time is out.
        if self.active_drop:
            if drop == "widthup":
                self.platform.width = 180
            elif drop == "dmgup":
                self.ball.dmg = 3

        if not self.active_drop:
            self.ball.dmg = 1
            self.platform.width = 100   
                
    def get_color(self):
        # Get the pool with increasing amount of colors for each level.
        if self.current_level == 1:
            colors = ["blue", "orange", "red", "blue", "red"]
        elif self.current_level == 2:
            colors = ["blue", "red", "orange", "blue", "orange", "red", 
                      "violet"]
        elif self.current_level >= 3:
            colors = ["blue", "red", "yellow", "orange", "violet", "orange",
                      "blue"]

        return choice(colors)
    
    def get_blocks(self):
        # create the block-rects
        for i in self.level_pos:
            color = self.get_color()
            new_block = Block(self, i[0], i[1], color)
            self.blocks.append(new_block)

    def update_blocks(self):
        # check the blocks for ballcollision and remove block, if hp <= 0 
        buffer = []
        for ball in self.active_balls:     
            for block in self.blocks:
                block.update()             
                if ball.rect.colliderect(block.rect):  
                    if not buffer:               
                        block.hp -= ball.dmg
                        buffer.append("hit")
                    if block.hp <= 0:
                        pygame.mixer.Channel(1).play(
                            pygame.mixer.Sound('sound/blib2.mp3'))
                        self.points += block.points
                        self.blocks.remove(block)
                        self.check_bonus(block)

    def check_block_collision(self):
        # Collision detection for the blocks, changes direction of the ball.
        buffer = []
        for i in self.blocks:
            for ball in self.active_balls:
                offset_x = i.rect.x - ball.rect.x
                offset_y = i.rect.y - ball.rect.y
                if ball.mask.overlap(i.mask, (offset_x, offset_y)):

                    if not buffer:
                        # check top of block
                        if (ball.rect.bottom >= i.rect.top and
                            ball.rect.top < i.rect.top):
                            if (ball.rect.left <= i.rect.right and
                                ball.rect.right >= i.rect.left):
                                if ball.direction_y == 1:
                                    buffer.append("collided")
                                    ball.direction_y *= -1
                                    ball.speed_y += 0.00127   

                    if not buffer:
                        # check bottom of block
                        if (ball.rect.top <= i.rect.bottom and
                            ball.rect.bottom > i.rect.bottom): 
                            if (ball.rect.left <= i.rect.right and
                                ball.rect.right >= i.rect.left):  
                                if ball.direction_y == -1: 
                                    buffer.append("collided")
                                    ball.direction_y *= -1
                                    ball.speed_y += 0.00123  

                    if not buffer:
                        # check left side of block
                        if (ball.rect.right >= i.rect.left and
                            ball.rect.left < i.rect.left): 
                            if (ball.rect.bottom >= i.rect.top and
                                ball.rect.top <= i.rect.bottom):  
                                if ball.direction_x == 1:
                                    buffer.append("collided")
                                    ball.direction_x *= -1  
                                    ball.speed_x += 0.00132 

                    if not buffer:                    
                        # check right side of block   
                        if (ball.rect.left <= i.rect.right and
                            ball.rect.right > i.rect.right): 
                            if (ball.rect.bottom >= i.rect.top and
                                ball.rect.top <= i.rect.bottom):  
                                if ball.direction_x == -1: 
                                    buffer.append("collided")   
                                    ball.direction_x *= -1
                                    ball.speed_x += 0.00121                                  

    def dead(self):
        # actions, if a ball is lost
        self.lives -= 1
        if self.lives > 0:
            self.level_running = False  
            self.platform.moving_left = False
            self.platform.moving_right = False       
            self.pickup_visible = False
            self.pickup_collected = False
            self.ball_lost = True
            self.timer.reset()
            self.active_drop = ""
            
            pygame.mixer.Channel(1).play(
                pygame.mixer.Sound('sound/balllost.mp3'))
            self.active_balls = []
            self.active_balls.append(self.ball)
            self.ball.start_pos()
        else:
            pygame.mixer.Channel(0).play(
                pygame.mixer.Sound('sound/fail.mp3'))
            self.play_button = Button(self, "Replay?")
            self.highscore.prep_high_score()
            self.game_active = False
            self.level_running = False        
            pygame.mouse.set_visible(True)
            self.endscreen_visible = True
            self.current_level = 1
            pygame.time.delay(3000)
            if self.highscore.grats:
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('sound/highscore.mp3'))
            self.active_balls = []
            self.active_balls.append(self.ball)
            
    def check_level_end(self):
        # Loading the next level, if all the blocks are removed.
        # Raise current_level and speed for ball and platform.
        if len(self.blocks) == 0:           
            self.level_running = False
            self.pickup_visible = False
            self.pickup_collected = False
            self.level_up = True
            self.active_drop = ""
            self.drops_collected = []

            self.current_level += 1
            self.ball_speed += 0.25
            self.platform.speed += 0.5

            self.active_balls = []
            self.active_balls.append(self.ball)

            if self.current_level <= 7:
                self.ball.start_pos()
                self.load_level_pos(self.current_level)
                self.get_blocks()
                self.scorelabel.prep_level(self.current_level)
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('sound/complete.mp3'))
                
            if self.current_level > 7:
                self.winscreen_visible = True
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('sound/win.mp3'))
                     
    def load_level_pos(self, level):
        # Blockpositions for each level.

        # if level == 1:
        #     # Test
        #     self.level_pos = [(370, 270)]

        if level == 1:
            # Glasses
            self.level_pos = [
                            (250, 50), (490, 50),
                            (190, 90), (310, 90), (430, 90), (550, 90),                           
                            (130, 130), (370, 130), (610, 130),
                            (70, 170), (370, 170), (670, 170),
                            (70, 210), (370, 210), (670, 210), 
                            (130, 250), (370, 250), (610, 250),
                            (190, 290), (310, 290), (430, 290), (550, 290),
                            (250, 330), (490, 330)
                            ] 

        if level == 2:
            # V
            self.level_pos = [
                            (70, 50), (130, 50), (310, 50), (370, 50),
                            (430, 50), (610, 50), (670, 50),                        
                            (190, 90), (550, 90),   
                            (70, 130), (250, 130), (490, 130), (670, 130),                           
                            (130, 170), (310, 170), (430, 170),(610, 170),                            
                            (190, 210), (370, 210), (550, 210),
                            (250, 250), (490, 250),
                            (310, 290), (430, 290),
                            (370, 330)                           
                            ]     
            
        if level == 3:
            # Alien 2
            self.level_pos = [
                            (190, 50), (370, 50), (550, 50),
                            (250, 90), (370, 90), (490, 90),
                            (130, 130), (310, 130), (370, 130), (430, 130), 
                            (610, 130),
                            (190, 170), (250, 170), (370, 170), (490, 170),
                            (550, 170),
                            (310, 210), (370, 210), (430, 210),
                            (250, 250), (490, 250), 
                            (190, 290), (250, 290), (310, 290), (370, 290),
                            (430, 290), (490, 290),
                            (130, 330), (190, 330), (370, 330), (550, 330),
                            (610, 330)
                            ]
            
        if level == 4:
            # Butterfly
            self.level_pos = [
                            (130, 50), (190, 50), (250, 50), (370, 50),
                            (490, 50), (550, 50), (610, 50), 
                            (70, 90), (310, 90), (430, 90), (670, 90),                           
                            (70, 130), (310, 130), (430, 130), (670, 130),
                            (130, 170), (190, 170), (250, 170), (370, 170),
                            (490, 170), (550, 170), (610, 170),
                            (130, 210), (310, 210), (430, 210), (610, 210), 
                            (70, 250),  (310, 250), (430, 250), (670, 250), 
                            (70, 290), (310, 290), (430, 290), (670, 290),
                            (130, 330), (190, 330), (250, 330), (370, 330),
                            (490, 330), (550, 330), (610, 330)
                            ] 
            
        if level == 5:
            # Alien 3
            self.level_pos = [
                            (70, 50), (370, 50), (670, 50), (130, 90),
                            (190, 90), (370, 90), (550, 90), (610, 90),
                            (250, 130), (310, 130), (370, 130), (430, 130),
                            (490, 130), 
                            (190, 170), (370, 170), (550, 170),
                            (130, 210), (190, 210), (250, 210), (310, 210),
                            (370, 210), (430, 210), (490, 210), (550, 210),
                            (610, 210), 
                            (250, 250), (490, 250),
                            (190, 290), (310, 290), (370, 290), (430, 290),
                            (550, 290), 
                            (70, 330), (130, 330), (370, 330), (610, 330), 
                            (670, 330)
                            ]
            
        if level == 6:
            # Bee
            self.level_pos = [
                            (130, 50), (190, 50), (310, 50), (370, 50),
                            (430, 50), (550, 50), (610, 50), 
                            (70, 90), (250, 90), (490, 90), (670, 90),                           
                            (70, 130), (250, 130), (490, 130), (670, 130),
                            (130, 170), (190, 170), (310, 170), (370, 170),
                            (430, 170), (550, 170), (610, 170),
                            (70, 210), (190, 210), (370, 210), (550, 210), 
                            (670, 210), 
                            (70, 250), (250, 250), (310, 250), (430, 250),
                            (490, 250), (670, 250), 
                            (70, 290), (130, 290), (190, 290), (250, 290),
                            (490, 290), (550, 290), (610, 290), (670, 290),
                            (130, 330), (250, 330), (310, 330), (370, 330),
                            (430, 330), (490, 330), (610, 330)
                            ]   
              
        if level == 7:
            # Alien 4
            self.level_pos = [
                            (250, 50), (370, 50), (490, 50), 
                            (70, 90), (190, 90), (250, 90), (310, 90), 
                            (370, 90), (430, 90), (490, 90), (550, 90), 
                            (670, 90),                           
                            (70, 130), (190, 130), (310, 130), (370, 130),
                            (430, 130), (550, 130), (670, 130), 
                            (130, 170), (190, 170), (370, 170), (550, 170), 
                            (610, 170),
                            (190, 210), (250, 210), (310, 210), (370, 210),
                            (430, 210), (490, 210), (550, 210), 
                            (130, 250), (250, 250), (490, 250), (610, 250), 
                            (70, 290), (250, 290), (310, 290), (370, 290),
                            (430, 290), (490, 290), (670, 290), 
                            (70, 330), (190, 330), (310, 330), (370, 330), 
                            (430, 330), (550, 330), (670, 330)
                            ] 
        
    def update_screen(self):
        # Draw the elements on the screen.
        self.screen.fill(self.bg_color)

        if not self.game_active and self.endscreen_visible:
            self.screen.blit(self.end_screen, (0, 0))
            self.play_button.draw_button()
            self.highscore.draw_highscore()
        elif not self.game_active and not self.endscreen_visible:
            self.screen.blit(self.title_screen, (0, 0))
            self.play_button.draw_button()

        if self.game_active and self.ball_lost:
            self.screen.blit(self.ball_lost_screen, (0, 0))

        if self.game_active and not self.ball_lost:
            self.scorelabel.draw_score()
            if (self.active_drop and not self.active_drop == "lifeup" and not
                self.active_drop == "multiball"):
                self.timer.drawme()           
            if self.pickup_visible:
                self.pickup.drawme()
            self.platform.drawme()
            for i in self.blocks:
                i.drawme()         
            for i in self.active_balls:        
                i.drawme()

        if self.game_active and self.level_up:
            self.screen.blit(self.levelup_screen, (0, 0))

        if self.game_active and self.winscreen_visible:
            self.screen.blit(self.winscreen_image, (0, 0))
            self.highscore.check_high_score()
            self.highscore.prep_high_score()

        pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()

