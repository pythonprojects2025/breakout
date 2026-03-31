import pygame
from pygame.sprite import Sprite
from random import choice


class Ball(Sprite):
    """This class builds the ball and update the position."""

    def __init__(self, game, x):
        super().__init__()
        """Initialize ball attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.platform = game.platform
        self.settings = game.settings

        self.radius = 10
        self.x = x
        self.y = 538.99
        self.x = float(self.x)
        self.y = float(self.y)
        self.color = (200, 250, 200)
        self.image = pygame.image.load("images/ball.png")
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.mask = pygame.mask.from_surface(self.image)

        self.ball_speed = game.ball_speed
        self.speed_y = self.ball_speed + 0.132
        self.speed_x = 0
        self.direction_x = 1
        self.direction_y = -1
        self.dmg = 1

    # def start_pos(self):
    #     # Reset start position of ball and platform.
    #     self.x = 390
    #     self.y = 538.99
    #     self.speed_x = 0
    #     self.speed_y = 0
    #     self.direction_x = 1
    #     self.direction_y = -1
    #     self.platform.x = 350
    #     self.dmg = 1

    
    def start_pos(self):
        """
        Setzt Ball und Plattform in die Ausgangsposition zurück
        und löscht jede momentane Geschwindigkeit.
        """
        # Position
        self.x = 390
        self.y = 538.99
        self.rect.topleft = (int(self.x), int(self.y))

        # Geschwindigkeit zurücksetzen
        self.speed_x = 0
        self.speed_y = 0
        self.direction_x = 1          # Standard‑Richtung (nach rechts)
        self.direction_y = -1         # nach oben (y‑Achse wächst nach unten)

        # Plattform zurücksetzen
        self.platform.x = 350
        self.platform.rect.x = 350    # falls du das Rect separat nutzt

        # Sonstiges
        self.dmg = 1
        self.game.level_running = False   # Spiel wartet jetzt auf den Launch
    
    # def check_launch(self):
    #     # Waiting for a keyboard action, to launch the ball.
    #     if self.platform.moving_left or self.platform.moving_right:   
    #         if self.platform.moving_left:
    #             self.speed_y = self.ball_speed
    #             self.speed_x = self.ball_speed + 0.03
    #         elif self.platform.moving_right:
    #             self.speed_y = self.ball_speed
    #             self.speed_x = -self.ball_speed + 0.03
    #         self.game.level_running = True

    
    def check_launch(self):
        """
        Wartet, bis die Plattform nach links oder rechts bewegt wird,
        und startet dann den Ball mit konstanter Gesamttempo‑Geschwindigkeit.
        """
        # Nur aktiv, wenn das Level noch nicht läuft
        if self.game.level_running:
            return

        # Hat die Plattform irgendeine horizontale Bewegung?
        if self.platform.moving_left or self.platform.moving_right:
            # Grundbetrag, den du bereits als self.ball_speed definiert hast
            total_speed = self.ball_speed

            # Wir geben dem Ball einen kleinen seitlichen Impuls,
            # proportional zur Bewegungsrichtung der Plattform.
            # Der Faktor 0.2 ist frei wählbar – er bestimmt, wie stark
            # der Ball nach links/rechts abdriftet.
            side_factor = 0.2 * total_speed

            if self.platform.moving_left:
                self.speed_x = -side_factor          # leicht nach links
            elif self.platform.moving_right:
                self.speed_x = side_factor           # leicht nach rechts
            else:
                self.speed_x = 0

            # Vertikale Komponente: immer nach oben
            self.speed_y = total_speed

            # **Betrag‑Normalisierung**  
            # Wenn wir einen seitlichen Impuls hinzufügen, wird der Betrag
            # etwas größer als total_speed. Wir skalieren deshalb beide
            # Komponenten wieder zurück auf den gewünschten Betrag.
            current_mag = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
            if current_mag != 0:
                scale = total_speed / current_mag
                self.speed_x *= scale
                self.speed_y *= scale

            # Richtungen setzen (bei positivem speed_x => direction_x = 1, sonst -1)
            self.direction_x = 1 if self.speed_x >= 0 else -1
            self.direction_y = -1                     # immer nach oben starten

            # Spiel‑Status aktivieren – jetzt läuft das eigentliche Update‑Loop
            self.game.level_running = True
        
    
    def update(self):
        # Update the position and call methods for collisiontests.
        if not self.game.level_running:
            self.check_launch()
        if self.game.level_running:
            self.check_walls()
            self.check_platform()
            self.check_bottom()
            self.x += (self.speed_x * self.direction_x)
            self.y += (self.speed_y * self.direction_y)
            self.rect.x = self.x
            self.rect.y = self.y

    def check_walls(self):
        # Changes direction of ball, if a wall is touched.
        if self.x + self.rect.width >= self.screen_rect.right:
            self.direction_x *= -1
            # self.speed_x += 0.00133             
             
        if self.x <= self.screen_rect.left:
            self.direction_x *= -1
            # self.speed_x += 0.00131
                     
        if self.y <= self.screen_rect.top:  
            self.direction_y *= -1         
            # self.speed_y += 0.0027
            
    def check_platform(self):
        # Änderungen nur, wenn der Ball die Plattform berührt
        if self.rect.colliderect(self.platform.rect):
            # Verhindere, dass der Ball „unter“ der Plattform steckt
            if not self.rect.bottom >= self.screen_rect.bottom - 29.99:
                self._new_velocity_from_hit()          # <-- neue Logik
            else:
                # Wenn der Ball sehr tief sitzt, einfach horizontal abprallen
                self.direction_x *= -1

    def check_bottom(self):
        # Check if ball is lost.
        if self.y + self.radius > self.screen_rect.bottom:  
            if len(self.game.active_balls) >= 1:
                self.game.active_balls.remove(self)
            if len(self.game.active_balls) < 1:
                self.game.dead()  
              
    def drawme(self):
        # Draw the ball on the screen.
        self.screen.blit(self.image, (self.x, self.y))

    def _hit_offset(self):
        """
        Gibt den relativen Abstand des Aufpralls von der Mitte der Plattform zurück.
        Wertebereich: -1 … 1   (‑1 = äußerste linke Kante, 0 = Mitte, 1 = rechte Kante)
        """
        platform_center = self.platform.rect.centerx
        ball_center      = self.rect.centerx
        half_width       = self.platform.rect.width / 2.0

        # Normalisierter Abstand
        offset = (ball_center - platform_center) / half_width
        # Begrenzen, falls der Ball leicht außerhalb der Plattform liegt
        return max(-1.0, min(1.0, offset))

    def _new_velocity_from_hit(self):
        """
        Berechnet neue horizontal‑/vertikal‑Geschwindigkeiten.
        - speed_x  : nur der Betrag (positiv)
        - direction_x : Vorzeichen (‑1 links, +1 rechts)
        - speed_y  : immer nach oben (positiver Betrag)
        - Der Gesamttempo‑Betrag bleibt exakt self.ball_speed.
        """
        # --------------------------------------------------------------
        # 1️⃣ Vorherige Richtung merken (nur das Vorzeichen)
        old_dir_x = self.direction_x          # -1 oder 1

        # 2️⃣ Wo hat der Ball die Plattform getroffen?
        offset = self._hit_offset()            # -1 … 1  (links … rechts)

        # 3️⃣ Maximaler seitlicher Anteil (60 % des Gesamttempos)
        max_side = self.ball_speed * 0.6
        side_amount = max_side * abs(offset)   # Betrag, immer ≥ 0

        # 4️⃣ Mindest‑Seitengeschwindigkeit, damit der Ball nicht stehenbleibt
        min_side = 0.2 * self.ball_speed      # 5 % des Tempos
        if side_amount < min_side:
            side_amount = min_side

        # 5️⃣ Plattform‑Boost (optional)
        boost = self.ball_speed * 0.25
        if self.platform.moving_left:
            side_amount += boost
        elif self.platform.moving_right:
            side_amount -= boost

        # 6️⃣ Vorzeichen entscheiden:
        #    - Bei starkem Rand‑Treffer (> 0.6) setzen wir die Richtung
        #      eindeutig nach rechts bzw. links.
        #    - Sonst behalten wir die alte Richtung bei.
        if offset > 0.5:
            new_dir_x = 1
        elif offset < -0.5:
            new_dir_x = -1
        else:
            new_dir_x = old_dir_x

        # --------------------------------------------------------------
        # 7️⃣ **WICHTIG:** speed_x ist jetzt nur der Betrag (positiv!)
        self.speed_x = side_amount               # positiv
        self.direction_x = new_dir_x             # Vorzeichen separat

        # 8️⃣ Vertikale Komponente (immer nach oben)
        self.speed_y = self.ball_speed           # Betrag (positiv)

        # --------------------------------------------------------------
        # 9️⃣ Betrag‑Normalisierung – Gesamttempo = self.ball_speed
        #    Wir skalieren **nur die Beträge**, das Vorzeichen bleibt
        #    unverändert in direction_x / direction_y.
        cur_mag = (self.speed_x ** 2 + self.speed_y ** 2) ** 0.5
        if cur_mag != 0:
            scale = self.ball_speed / cur_mag
            self.speed_x *= scale               # bleibt positiv
            self.speed_y *= scale               # bleibt positiv

        # 10️⃣ Vertikale Richtung immer nach oben
        self.direction_y = -1



















