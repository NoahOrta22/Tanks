
import pygame as py
import random
import os
from tankClass import Tank

py.init()
 
WIDTH = 1400
HEIGHT = 800

screen = py.display.set_mode([WIDTH, HEIGHT])
py.display.set_caption('TANKS')
screen.fill('deepskyblue4')
explodesound = py.mixer.Sound('Chunky Explosion.mp3')
battlesound = py.mixer.Sound('battle.mp3')
# set a limit for the cpu
clock = py.time.Clock()
clock.tick(20)
timer = py.time




#--------------------------------------------fonts with size, for text_object function----------------
smallfont = py.font.SysFont("comicsansms", 25)
medfont = py.font.SysFont("comicsansms", 50)
largefont = py.font.SysFont("Yu Mincho Demibold", 85)
vsmallfont = py.font.SysFont("Yu Mincho Demibold", 25)

#--------------------------------------------defining score function----------------------------------
def score(score):
    text = smallfont.render("Score: " + str(score), True, 'white')
    py.blit(text, [0, 0])

#---defining function to get the fonts and sizes assigned with them by size names by default size="small"--
def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    if size == "vsmall":
        textSurface = vsmallfont.render(text, True, color)

    return textSurface, textSurface.get_rect()

#---------------------fuction for texts that has to appear over button----------------------------------------
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="vsmall"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth / 2)), buttony + (buttonheight / 2))
    screen.blit(textSurf, textRect)

#--------------------fuction for texts that has to appear over screen----------------------------------------
def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (int(WIDTH / 2), int(HEIGHT / 2) + y_displace)
    screen.blit(textSurf, textRect)


#--------------function for buttons having action calls and text on it callings---------------------------
def button(text, x, y, width, height, inactive_color, active_color, action=None,size=" "):
    cur = py.mouse.get_pos()
    click = py.mouse.get_pressed()
    # print(click)
    if x + width > cur[0] > x and y + height > cur[1] > y:
        py.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                py.quit()
                quit()
            if action == "play":
                gameloop()

    else:
        py.draw.rect(screen, inactive_color, (x, y, width, height))

    text_to_button(text, 'black', x, y, width, height)
#---------------------------function for players win screen--------------------------------------------------
def you_win(playernum):
    win = True

    while win:
        for event in py.event.get():
            # print(event)
            if event.type == py.QUIT:
                py.quit()
                quit()

        screen.fill('red')
        message_to_screen(f"Player {playernum} won!", 'white', -100, size="large")
        message_to_screen("Congratulations!", 'wheat', -30)

        button("Play Again", 550, 500, 150, 50, 'wheat', 'light_green', action="play")
        button("Quit", 950, 500, 100, 50, 'wheat', 'light_red', action="quit")

        py.display.update()

        clock.tick(30)


# get a random floor level and wall height
left_floor_y = random.randint(210, 700)
right_floor_y = random.randint(210, 700)
high_wall = min(left_floor_y, right_floor_y)
low_wall = max(left_floor_y, right_floor_y)
wall_y = random.randint(200, high_wall-50)


# draws the floor for the left and right sides
def draw_left_floor():
    py.draw.rect(screen, 'springgreen4', [0, left_floor_y, WIDTH/2, HEIGHT])
def draw_right_floor():
    py.draw.rect(screen, 'springgreen4', [WIDTH/2, right_floor_y, WIDTH/2, HEIGHT])

# draws the wall in the middle
wall_rect = py.rect.Rect([(WIDTH/2)-20, wall_y, 40, low_wall-wall_y])
def draw_wall():
    py.draw.rect(screen, 'dimgrey', wall_rect)

# Create the left and right tank
left_tank = Tank(screen, 'red', [40, left_floor_y-40, 70, 40], wall_rect, timer, 'left')
right_tank = Tank(screen, 'blue', [WIDTH-110, right_floor_y-40, 70, 40], wall_rect, timer, 'right')


# checks if the bullet is colliding with the world. 
def bullet_colliding(bullet,enemyTank):
    # making sure bullet is on screen
    if (bullet.x > -1 and bullet.x < WIDTH + 10):
        # bullet is not colliding with wall
        if not (bullet.x >= wall_rect.left-bullet.radius and bullet.x <= wall_rect.right+bullet.radius and bullet.y > wall_rect.top-bullet.radius):
            # bullet is not colliding with the floor
            if (bullet.x <= WIDTH/2 and bullet.y < left_floor_y-bullet.radius) or (bullet.x >= WIDTH/2 and bullet.y < right_floor_y-bullet.radius):
                #bullet is colliding with tank
                if not (bullet.collides_with(enemyTank)):      
                    return False
    

    return True, 

#Returns if tank has been hit or not
def hit(bullet,enemyTank):
    if (bullet.collides_with(enemyTank)):
        return True
    return False

# Displays power level of the bullet **** UPDATED ****
def bulletpower(tank):
    text = py.font.SysFont("Roboto-Bold", 25).render("Power: " + str(int(tank.get_power())) + "%", True, 'wheat')
    if tank.side == 'right':
        screen.blit(text, [WIDTH * .75, 0])
    if tank.side == 'left':
        screen.blit(text, [WIDTH * .25, 0])

def health_bars(player1_health, player2_health):
    if player1_health > 75:
        player1_health_color = 'green'
    elif player1_health > 50:
        player1_health_color = 'yellow'
    else:
        player1_health_color = 'red'

    if player2_health > 75:
        player2_health_color = 'green'
    elif player2_health > 50:
        player2_health_color = 'yellow'
    else:
        player2_health_color = 'red'

    py.draw.rect(screen, player2_health_color, (1220, 25,player2_health , 25))
    py.draw.rect(screen, player1_health_color, (20, 25, player1_health, 25))
    

# draw all back screen stuff and tanks
def draw_stuff():
    screen.fill('deepskyblue4') 
    left_tank.draw()
    right_tank.draw()
    draw_left_floor()
    draw_right_floor()
    draw_wall()
    health_bars(left_tank.health,right_tank.health)


left_shoot = False
start_left_power = False

power_increase = 0
power_increase2 = 0
fire_power = 0
fire_power2 = 0
angle = 0


# Load explosion images
explosion_images = []
for i in range(1,7):
    filename = os.path.join('Explosions/', f'Explosion{i}.png')
    image = py.image.load(filename).convert()
    explosion_images.append(image)

# Set up explosion animation
explosion_animation = py.sprite.Group()
for i in range(0,6):
    explosion_sprite = py.sprite.Sprite()
    explosion_sprite.image = explosion_images[i]
    explosion_sprite.rect = explosion_sprite.image.get_rect()
    explosion_animation.add(explosion_sprite)




run = True
battlesound.play()
while run:
    clock.tick(40)
    draw_stuff() 
    left_tank.draw_bullet(bullet_colliding(left_tank.bullet,right_tank.rect))
    right_tank.draw_bullet(bullet_colliding(right_tank.bullet,left_tank.rect))
    


    # if left_shoot: 
    #     bullet = left_tank.bullet
    #     if bullet.y < 700 - bullet.radius:
    #         bullet.time += 0.25
    #         bullet.x, bullet.y = bullet.path(bullet.power, bullet.angle, bullet.time)
    #         bullet.draw()
    #     else:
    #         left_shoot = False
    #         start_left_power = False




    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            run = False
            quit()

        # check if one of the arrow keys was pressed
        if event.type == py.KEYDOWN:
            # doing the power for the left player
            if event.key == py.K_x:
                left_tank.start_shoot()
                power_increase2 = 2
                fire_power2 += power_increase2
                # bulletpower(fire_power2,2)
            if event.key == py.K_SPACE:
                right_tank.start_shoot()
                power_increase = 2
                fire_power += power_increase
                # bulletpower(fire_power,1)
                # if left_shoot == False: 
                #     if start_left_power == False:
                #         start_t = timer.get_ticks()
                #         start_left_power = True 
                #     else:
                #         left_tank.bullet.power = (timer.get_ticks()-start_t)/8
                #         left_shoot = True
                #         print(left_tank.bullet.power)
                #         # getting the starting position for the bullet
                #         left_tank.bullet.startx = left_tank.rect.midtop[0]
                #         left_tank.bullet.starty = left_tank.rect.midtop[1]
                #         left_tank.bullet.x = left_tank.bullet.startx
                #         left_tank.bullet.y = left_tank.bullet.starty
                #         # setting the start times to zero
                #         left_tank.bullet.time = 0
                #         left_tank.bullet.angle = 1.0

        elif event.type == py.KEYUP:
            if event.key == py.K_SPACE or event.key == py.K_x:
                    power_increase = 0
                    power_increase2 = 0

    leftHit = hit(right_tank.bullet,left_tank.rect)
    rightHit = hit(left_tank.bullet,right_tank.rect)
    fire_power += power_increase
    fire_power2 += power_increase2

    if fire_power > 100:
        fire_power = 100
    if fire_power2 > 100:
        fire_power2 =100

    if right_tank.shoot:
        fire_power=0
        if leftHit:
            # Start explosion animation
            explosion_animation_pos = right_tank.bullet.x, right_tank.bullet.y
            explodesound.play()
            for i in range(0,6):
                explosion_sprite = explosion_animation.sprites()[i]
                explosion_sprite.rect.center = explosion_animation_pos
                screen.blit(explosion_sprite.image, explosion_sprite.rect)
                py.display.flip()
                py.time.wait(50)
            left_tank.health=left_tank.health-25
            print("left hit boi")
            leftHit = False
            if left_tank.health <= 0:
                you_win(1)



    if left_tank.shoot:
        fire_power2=0
        if rightHit:
            # Start explosion animation
            explosion_animation_pos = left_tank.bullet.x, left_tank.bullet.y
            explodesound.play()
            for i in range(0,6):
                explosion_sprite = explosion_animation.sprites()[i]
                explosion_sprite.rect.center = explosion_animation_pos
                screen.blit(explosion_sprite.image, explosion_sprite.rect)
                py.display.flip()
                py.time.wait(50)
            right_tank.health = right_tank.health-25
            print("right hit boi")
            rightHit = False
            if right_tank.health <= 0:
                you_win(2)

    
    bulletpower(right_tank)
    bulletpower(left_tank)
    right_tank.handle_keys()
    left_tank.handle_keys()
    py.display.flip()
        
            