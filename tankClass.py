import pygame as py
import math

WIDTH = 1400
GRAVITY = -9.8

class Tank():
    def __init__(self, screen, color, coordinates, wall, timer, side):
        self.health = 100
        self.screen = screen
        self.color = color
        self.rect = py.rect.Rect(coordinates)
        self.wall = wall
        self.timer = timer

        # canon length
        self.canon_length = 35

        # for bullet stuff
        self.bullet = Bullet(screen, self.rect.midtop)
        self.shoot = False
        self.start_power = False
        self.start_t = 0

        # knowing which side the tank is on
        self.side = side
        

    # handles key input and movements
    def handle_keys(self):
        key = py.key.get_pressed()
        speed = 6
        angle_speed = .03

        # TANK ON RIGHT
        if self.side == 'right':
            # for moving
            if key[py.K_LEFT] and not self.rect.colliderect(self.wall):    # move left
                self.rect.move_ip(-speed, 0)
            if key[py.K_RIGHT] and self.rect.right <= WIDTH:               # move right
                self.rect.move_ip(speed, 0)
             # if a bullet is not being shot then you can change the angle
            if not self.shoot:
                if key[py.K_UP]:
                    self.bullet.change_angle(-angle_speed)
                if key[py.K_DOWN]:
                    self.bullet.change_angle(angle_speed)

        # TANK ON LEFT
        elif self.side == 'left':
            # for moving
            if key[py.K_a] and self.rect.left >= 0:                       # move left
                self.rect.move_ip(-speed, 0)
            if key[py.K_d] and not self.rect.colliderect(self.wall):       # move right
                self.rect.move_ip(speed, 0)
            # if a bullet is not being shot then you can change the angle
            if not self.shoot:
                if key[py.K_w]:
                    self.bullet.change_angle(angle_speed)
                if key[py.K_s]:
                    self.bullet.change_angle(-angle_speed)
        # if key[py.K_UP]:
        #    self.rect.move_ip(0, -1)
        # if key[py.K_DOWN]:
        #    self.rect.move_ip(0, 1)

    # draw the bullet if it's been shot
    def draw_bullet(self, colliding):
        if self.shoot: 
            bullet = self.bullet
            if not colliding:
                bullet.time += 0.18
                bullet.x, bullet.y = bullet.path()
                bullet.draw()
                self.draw()
            else:
                self.shoot = False
                self.start_power = False

    # getting the power of the button from how long the user waits until the second button press
    def start_shoot(self):
        # it hasn't shot
        if self.shoot == False:
            # it hasn't started the power up
            if self.start_power == False:
                self.start_t = self.timer.get_ticks()
                self.start_power = True
            # it has started the power up
            else:
                self.bullet.power = (self.timer.get_ticks()-self.start_t)/12
                self.shoot = True
                # getting the starting position for the bullet
                self.bullet.startx = self.rect.midtop[0]
                self.bullet.starty = self.rect.midtop[1]
                self.bullet.x = self.bullet.startx
                self.bullet.y = self.bullet.starty
                # setting the start times to zero
                self.bullet.time = 0

    # drawing the tank
    def draw(self):
        py.draw.rect(self.screen, self.color, self.rect, 0, 5)
        py.draw.circle(self.screen, self.color, self.rect.midtop, 20) 
        line_end = tuple(map(sum, zip(self.rect.midtop, law_of_sines(self.bullet.angle, self.canon_length))))
        py.draw.line(
            self.screen, 
            self.color, 
            self.rect.midtop,
            line_end,
            15)


class Bullet():
    def __init__(self, screen, coord):
        self.startx = coord[0]
        self.starty = coord[1]
        self.x = coord[0]
        self.y = coord[1]
        self.screen = screen
        self.radius = 7
        self.color = 'black'
        self.time = 0
        self.power = 100
        if self.x < (WIDTH/2):
            self.angle = 0.1
        else:
            self.angle = math.pi-0.1

    def draw(self):
        py.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)

    # Description: 
    #       changes the angle of the 'canon'
    # Params:
    #       val - float = by how much we want to change the angle
    def change_angle(self, val):
        if (val > 0 and self.angle < 3) or (val < 0 and self.angle >= .1):
            self.angle += val
        

    # Description: 
    #       finding the new x and y coordinates for the bullet
    # Params:
    #       startx : int   - starting x coordinate
    #       starty : int   - starting y coordinate
    #       power  : float - the power of the shot
    #       angle  : float - angle of the bullet
    #       time   : float - time since bullet was shot

    # @staticmethod
    def path(self):
        velx = math.cos(self.angle) * self.power
        vely = math.sin(self.angle) * self.power
        
        distX = velx * self.time
        distY = (vely * self.time) + ((GRAVITY * (self.time)**2)/2)

        newx = round(self.startx + distX)
        newy = round(self.starty - distY)

        return newx, newy


# Description:
#       Left angle is A, Top angle is B, right angle is C
#  Params:
#       canon_length - the length of the canonf
#       
def law_of_sines(angleA, canon_length):
    angleB = (math.pi/2) - angleA
    angleC = math.pi/2
    side_c = canon_length


    side_a = side_c * (math.sin(angleA) / math.sin(angleC))
    side_b = side_a * (math.sin(angleB) / math.sin(angleA))

    return (side_b, -side_a)
