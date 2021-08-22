# importing all our modules
import pygame
import os
import random

# Initilizing pygame
pygame.init()

# adding our window width and height
win_height = 400
win_width = 800

#window fill and dimensions
win = pygame.display.set_mode((win_width, win_height))

# Importing Hero images
standing = pygame.image.load(os.path.join("Assets/Hero", "standing.png"))

left = [pygame.image.load(os.path.join("Assets/Hero", "L1.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L2.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L3.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L4.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L5.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L6.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L7.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L8.png")),
        pygame.image.load(os.path.join("Assets/Hero", "L9.png"))]

right = [pygame.image.load(os.path.join("Assets/Hero", "R1.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R2.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R3.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R4.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R5.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R6.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R7.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R8.png")),
        pygame.image.load(os.path.join("Assets/Hero", "R9.png"))]

# Importing enemy images
Eleft = [pygame.image.load(os.path.join("Assets/Enemy", "L1E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L2E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L3E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L4E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L5E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L6E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L7E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L8E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L9P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L10P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "L11P.png"))]

Eright = [pygame.image.load(os.path.join("Assets/Enemy", "R1E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R2E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R3E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R4E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R5E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R6E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R7E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R8E.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R9P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R10P.png")),
        pygame.image.load(os.path.join("Assets/Enemy", "R11P.png"))]

# Importing Bullet images
bullet_img = pygame.image.load(os.path.join("Assets/Bullets", "light_bullet.png"))

# Scaling our bullet image
bi = pygame.transform.scale(bullet_img, (15, 15))

# Background image
bg_img = pygame.image.load("background.png")

# Scaling our background image
bg = pygame.transform.scale(bg_img, (win_width, win_height))

# Loading our music
music = pygame.mixer.music.load("Desert-Caravan-Aaron-Kenny.mp3")
pygame.mixer.music.play(-1)

# Creating our Hero class
class Hero:

    # initulizing all our variables
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = 10
        self.vel_y = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.jump = False
        self.bullets = []
        self.cool_down_count = 0
        self.hitBox = (self.x, self.y, 42, 55)
        self.health = 30
        self.lives = 3
        self.alive = True
        self.score = 0

    # Movement function for our Hero
    def movement(self, userInput):
        if (userInput[pygame.K_RIGHT]) and self.x <= win_width - 60:
            self.x += self.vel_x
            self.face_right = True
            self.face_left = False
        elif (userInput[pygame.K_LEFT]) and self.x >= 0:
            self.x -= self.vel_x
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    # Drawing our Hero
    def draw_character(self, win):
        self.hitBox = (self.x + 10, self.y + 10, 42, 55) # So the hitbox can be drawn again
        pygame.draw.rect(win, (255, 0, 0), (self.x + 15, self.y - 5, 30, 10))
        if self.health >= 0:
            pygame.draw.rect(win, (23, 107, 0), (self.x + 15, self.y - 5, self.health, 10))

        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    # adding the Jumping function for Hero
    def Jump(self, userInput):
        if userInput[pygame.K_UP] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vel_y * 4
            self.vel_y -= 1
        if self.vel_y < -10:
            self.jump = False
            self.vel_y = 10

    # Making sure that the Hero is facing the right direction
    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1

    # Adding delay to the shooting of the bullet
    def Cool_Down(self):
        if self.cool_down_count >= 7:
            self.cool_down_count = 0
        elif self.cool_down_count > 0:
            self.cool_down_count += 1

    # Shooting the bullets
    def shoot_bullet(self):
        self.hit()
        self.Cool_Down()
        if (userInput[pygame.K_SPACE] and self.cool_down_count == 0):
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
            self.cool_down_count = 1
        for bullet in self.bullets:
            bullet.move_bullet()

            # removes the bullet when they are off the screen
            if bullet.off_screen():
                self.bullets.remove(bullet)

    # If the Hero hits the enemy: Prints, enemy health gets lower, and the bullet gets remove after hitting enemy
    def hit(self):
        for enemy in enemies:
            for bullet in self.bullets:
                if enemy.hitBox[0] < bullet.x < enemy.hitBox[0] + enemy.hitBox[2] and enemy.hitBox[1] < bullet.y < enemy.hitBox[1] + enemy.hitBox[3]:
                    print("You have hit the enemy!")
                    enemy.health -= 5
                    music_hit = pygame.mixer.music.load("pop.wav")
                    pygame.mixer.music.play(1)
                    player.bullets.remove(bullet)
                    if (enemy.health == 0):
                        enemies.remove(enemy)
                        self.score += 5

                    
# Creating the Bullet class
class Bullet:
    # Initulizing our varuables for the Bullet
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction

    # Drawing the Bullet
    def draw_bullet(self):
        win.blit(bi, (self.x, self.y))

    # Moving the bullet
    def move_bullet(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15

    # checks if the bullet is of off the sceen or not (fixes the memory leak issue)
    def off_screen(self):
        return not(self.x >= 0 and self.x <= win_width)

# Creating the Enemy class
class Enemy():

    # Initulizing the varables for the Enemy
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.step_index = 0
        self.hitBox = (self.x, self.y, 42, 55)
        self.health = 30

    # Resetting the animation for the enemy
    def step(self):
        #using 33 instead of 11 because runs smoother and without glitch
        if self.step_index >= 33:
            self.step_index = 0
    
    # Drawing the enemy
    def draw_enemy(self, win):
        self.step()
        self.hitBox = (self.x + 15, self.y - 10, 50, 70)
        # Draws the health Bar
        pygame.draw.rect(win,(255,0 , 0), (self.x + 20, self.y - 10, 30, 10)) 
        if self.health >= 0:
            # Draws the health Bar
            pygame.draw.rect(win, (23, 107, 0), (self.x + 20, self.y - 10, self.health, 10))

        # Checking the direction of the Enemy
        if self.direction == left:
            win.blit(Eleft[self.step_index//3],(self.x,self.y))
        if self.direction == right:
            win.blit(Eright[self.step_index//3],(self.x,self.y))
        self.step_index += 1

    # Adding the movement for the enemy
    def move_enemy(self):
        self.hit_hero()
        if self.direction == left:
            self.x -= 3
        if self.direction == right:
            self.x += 3

    # Checking to see if the enemy if off the screen and deleting the enemy if it is
    def off_screen(self):
        return not(self.x >= -50 and self.x <= win_width + 50)

    # Checking to see if the enemy hits the Hero
    def hit_hero(self):
        if player.hitBox[0] < enemy.x + 32 < player.hitBox[0] + player.hitBox[2] and player.hitBox[1] < enemy.y + 32 < player.hitBox[1] + player.hitBox[3]:
            print("Enemy has hit you!")
            if player.health > 0:
                player.health -= 1
                if player.health == 0 and player.lives > 0:
                    player.lives -= 1
                    player.health = 30
                    # If there is no more lives/health --> player.alive is False
                elif player.health == 0 and player.lives == 0:
                    player.alive = False

# main funciton
def game():
    win.fill((0, 0, 0))
    win.blit(bg, (0, 0))
    player.draw_character(win)

    for bullet in player.bullets:
        bullet.draw_bullet()
    for enemy in enemies:
        enemy.draw_enemy(win)
    # Checking if the player if dead or not
    if player.alive == False:
        win.fill((74, 8, 8))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render("GAME OVER PRESS 'R' TO RESTART", True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (win_width // 6 , win_height // 2)
        win.blit(text, (textRect.center))
        if userInput[pygame.K_r]:
            player.alive = True
            player.lives = 3
            player.health = 30
            player.score = 0
    # Displaying player lives
    font = pygame.font.Font('freesansbold.ttf', 32)
    # '+' string Concatenation
    text = font.render("Lives: " + str (player.lives), True, (0, 0, 0))
    win.blit(text, (650, 20))
    # Displaing player's score
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("Score: " + str (player.score), True, (0, 0, 0))
    win.blit(text, (50, 20))

    pygame.time.delay(30)
    pygame.display.update()


# Instance of Hero-Class
player = Hero(250, 300)

#Instance of Enemy-Class
enemies = []

#main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #name spacing
    userInput = pygame.key.get_pressed()

    #calling all our functions
    player.movement(userInput)
    player.Jump(userInput)
    player.shoot_bullet()

    # call all functions of enemy
    if len(enemies) == 0:
        rand_n = random.randint(0,1)
        if rand_n == 1:
            enemy = Enemy(750, 300, left)
            enemies.append(enemy)
        if rand_n == 0:
            enemy = Enemy(50, 300, right)
            enemies.append(enemy)
    for enemy in enemies:
        enemy.move_enemy()
        if enemy.off_screen():
            enemies.remove(enemy)

    game()