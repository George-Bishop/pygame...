# importing all key functionailities for the game
import pygame, sys
from pygame.locals import *
import button
import math
import time

#initialising pygame so that the code can run
pygame.init()

#adding a time element to the game throught the pygame.time.clock function
clock = pygame.time.Clock()

#creating the fps that will be used for the player when playing the game
fps = 60

#creating the size of the screen width and screen height of the game
width = 1000 
height = 500  

#creating the screen and then setting the screen caption
screen = pygame.display.set_mode((width,height))  
pygame.display.set_caption("Ninja Runner")  

#defining game variables
#creating the tile size so that it matches my screen size
tile_size = 25
#creating a game over state of 0 that i can set to 1 if the player dies
game_over = 0
#setting the level state to equal -4 as this will be the enter name screen
levelstate = -4
#setting the time = 0 seconds
score = 0
#setting the screenstate variable = 0 so that I can change it if the screen is changing
screenstate = 0
#setting the score value for the player equal to 0
score_value = 0
#allowing my user to enter a name
name = ""

#creating the font for my game that will stay throughout the games design
font = pygame.font.Font(None, 32)
font_score = pygame.font.SysFont('corbel', 50)  
  
#creating a draw text function that will allow me to draw text to the screen if I need to call it
def draw_text(text,font, text_col, x, y):  
  img = font.render(text, True, text_col) 
  #drawing the text to the screen at the points x and y which can be entered when creating the function 
  screen.blit(img, (x,y))  
  
#creating colours that will be able to be used when making the game and the game design
white = (255, 255, 255)  
black = (0,0,0)
green = (0,255,0)
blue = (0,0,255)
red = (255,0,0)
grey = (30,30,30)

  
#loading images of background and buttons and title etc
bg_img = pygame.image.load('images/background.png').convert_alpha()
bg_img = pygame.transform.scale(bg_img,(1000,500))
bg2_img = pygame.image.load('images/bg2.jpg').convert_alpha()
bg2_img = pygame.transform.scale(bg2_img,(1000,500))
bg3_img = pygame.image.load('images/bg3.jpeg').convert_alpha()
bg3_img = pygame.transform.scale(bg3_img,(1000,500))
Play_img = pygame.image.load('images/button.png').convert_alpha()   
Exit_img = pygame.image.load('images/button.png').convert_alpha()  
Controls_img = pygame.image.load('images/button.png').convert_alpha()  
Highscore_img = pygame.image.load('images/button.png').convert_alpha()
Difficulty_img = pygame.image.load('images/button.png').convert_alpha()    
Title_img = pygame.image.load('images/logo.png').convert_alpha()  
fspicture_img = pygame.image.load('images/characters.png').convert_alpha() 
controls_img = pygame.image.load('images/controls.png').convert_alpha()
back_img = pygame.image.load('images/button.png').convert_alpha()
easy_img = pygame.image.load('images/button.png').convert_alpha() 
medium_img = pygame.image.load('images/button.png').convert_alpha() 
difficult_img = pygame.image.load('images/button.png').convert_alpha() 
extreme_img = pygame.image.load('images/button.png').convert_alpha() 
impossible_img = pygame.image.load('images/button.png').convert_alpha() 



#create button instances which will be using the images that were just created
Play_button = button.Button(300,200, Play_img, 2)  
Exit_button = button.Button(10,400, Exit_img, 1.5)  
Controls_button = button.Button(600,330, Controls_img, 2)
Highscore_button = button.Button(300,330, Highscore_img, 2)
Difficulty_button = button.Button(600,200, Difficulty_img, 2)
back_button = button.Button(0,0, back_img, 2)
easy_button = button.Button(300,200, easy_img, 2)
medium_button = button.Button(300,300, medium_img, 2)
difficult_button = button.Button(300,400, difficult_img, 2)
extreme_button = button.Button(600,300, extreme_img, 2)
impossible_button = button.Button(600,400, impossible_img, 2)


# Used to scale the title to a size that I will like it to be
Title_img = pygame.transform.scale(Title_img,(450,300))
#function to draw the title onbto the screen
def title(x,y):
  screen.blit(Title_img, (x,y))

# Used to scale the frint screen picture to a size I would like 
fspicture_img = pygame.transform.scale(fspicture_img,(200,300))
#function to draw the front screen pictuer onbto the screen
def fspicture(x,y):
  screen.blit(fspicture_img, (x,y))

class Player():
    def __init__(self, x, y):
        # The images_right and images_left variables are lists of images
        # These images represent the player facing to the right and left
        #These will be iterated through in order to create an animation for the player
        self.images_right = []
        self.images_left = []

        # This loop loads the player images from file and scales them to the appropriate size
        # The images are added to the images_right and images_left lists
        #this will iterate thorugh i in the list and then use the images for run to create a running animation for the player
        for num in range(1, 3):
            img_right = pygame.image.load(f'Images/Run__00{num}.png').convert_alpha()
            img_right = pygame.transform.scale(img_right, (40,40))
            #fips the image
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)

        # The index and counter variables are used to keep track of the current image being displayed. this will be edited in the future code in order for me to chage the player index and characters
        self.index = 0
        self.counter = 0

        #creating the dead image of the player that will float up to the top of the screen when the player dies.
        self.dead_image = pygame.image.load('Images/death.png').convert_alpha()
        self.dead_image = pygame.transform.scale(self.dead_image, (70,70))

        # The current image displayed is set to the first image in images_right, then it will be transformed into the next image and so on
        self.image = self.images_right[self.index]

        # The x and y coordinates of the rect are set to the given x and y parameters so that they can be drawn to the screen with specific values that are set by myself.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        # The vel_y variable represents the player's vertical velocity
        self.vel_y = 0

        # Represents whether or not the player has jumped
        self.jumped = False

        # The direction variable is used to determine which way the player is facing
        # It is initialized to 1, which represents facing to the right
        self.direction = 1

    #function for resetting the jump
    def resetjump(self):
        self.jumped = False

    #function for update which will take game over as a parameter and go to the game over screen if the player dies
    def update(self, game_over):
        global levelstate #brings in the glocal variable levelstate
        global score #brings in the global variable score
        global score_value #brings in the global variable score_value

        dx = 0 # represents the change in x variable
        dy = 0 # represents the change in y variable
        #creates a cooldown for the player running
        run_cooldown = 10
        
        if game_over >= 0:
            # get keypresses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                #makes the player move left with a change in x of 3 
                dx -= 3
                self.counter += 1
                self.direction = -1

            if keys[pygame.K_RIGHT]:
                dx += 3
                #mnakes the player move right with a change in x of 3
                self.counter += 1
                self.direction = 1

            if keys[pygame.K_UP] and not self.jumped: #this changes the y variable when the player jumps in order to represent the jump
                #makes the player jump by chaning the y  by 16
                self.vel_y = -16
                self.jumped = True


            if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    #sets image = to the right images of the player
                    self.image = self.images_right[self.index]
                    #sets image = to the left images of the player
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animations for the player
            if self.counter > run_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                elif self.direction == -1:
                    self.image = self.images_left[self.index]

            # apply gravity
            self.vel_y += 1.3
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # check for collision
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground (jumping)
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground (falling)
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.resetjump()

            # check for collision with enemies
            if pygame.sprite.spritecollide(self, zombie_group, False):
                game_over = -1

            # check for collision with spikes
            if pygame.sprite.spritecollide(self, spikes_group, False):
                game_over = -1

            if pygame.sprite.spritecollide(self, spikesdown_group, False):
                game_over = -1
            
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1

            # check for collision with door
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            # keep player within screen boundaries so that they cannot run off the screen or fall of the screen
            if self.rect.top < 0:
                self.rect.top = 0
                self.vel_y = 0
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.vel_y = 0
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > width:
                self.rect.right = width

        #change the screen and output if the game is over
        elif game_over == -1:
            self.image = self.dead_image
            draw_text('YOU DIED', font, black, (width // 2) - 200, (height // 2) - 100)
            if self.rect.y > 0:
                self.rect.y -= 4
            else:
                #set everythihng back = to 0
                levelstate = 0
                game_over = 0
                score = 0
                score_value = 0

                

        # draw player on screen
        screen.blit(self.image, self.rect)
  

        return game_over

#creating the class for the door
class Door(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/door.png').convert_alpha()
        self.image = pygame.transform.scale(img, (int(tile_size * 3), int(tile_size * 4)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#creating the class for the enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Images/zombieidle.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y    
        self.move_direction = 1
        self.move_counter = 0

    #creating an updat function for the enemy
    def update(self):
        self.rect. x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 40:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


#creating a class for spikes
class Spikes(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/spikes.png').convert_alpha()
        imgdown = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.imagedown =  pygame.transform.scale(imgdown, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rectdown = self.imagedown.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/lava.png').convert_alpha()
        imgdown = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.imagedown =  pygame.transform.scale(imgdown, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rectdown = self.imagedown.get_rect()
        self.rect.x = x
        self.rect.y = y

#creating a class for spikedown
class Spikesdown(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/spikes.png').convert_alpha()
        img = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#creating a class for spikedown
class Stone(pygame.sprite.Sprite):
    def __init__(self, x, y,):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('Images/stone.jpeg').convert_alpha()
        img = pygame.transform.flip(img, False, True)
        self.image = pygame.transform.scale(img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        
        
#creating a class for the world and the world data
class World():
      def __init__(self, data):
        global player
        self.tile_list = []
        player = Player(30, height - 40)
        spikes_group.empty()
        spikesdown_group.empty()
        lava_group.empty()
        zombie_group.empty()
        door_group.empty()



     
        #load images
        floor_img = pygame.image.load('Images/lvl1floor.png').convert_alpha()
        stone_img = pygame.image.load('Images/stone.jpeg').convert_alpha()

        row_count = 0
        for row in data:
            col = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(floor_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    zombie = Enemy(col * tile_size, row_count * tile_size  - 12)
                    zombie_group.add(zombie)
                if tile == 3:
                    spikes = Spikes(col * tile_size, row_count * tile_size)
                    spikes_group.add(spikes)
                if tile == 4:
                    spikesdown = Spikesdown(col * tile_size, row_count * tile_size)
                    spikesdown_group.add(spikesdown)
                if tile == 5:
                    door = Door(col * tile_size - 20, row_count * tile_size - 50 )
                    door_group.add(door)
                if tile == 6:
                    lava = Lava(col * tile_size, row_count * tile_size)
                    spikes_group.add(lava)
                if tile == 7:
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img.set_alpha(None)  # Reset alpha channel if needed
                    img_rect = img.get_rect()
                    img_rect.x = col * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)


                col += 1
            row_count += 1

      def draw(self):
        for tile in self.tile_list:
          screen.blit(tile[0], tile[1])
          pygame.draw.rect(screen, (181,101,29), tile[1], 2)

levelnum1 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 1, 3, 3, 1, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

levelnum2 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3],
[5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 1, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 1],
[0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 3, 3, 3, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 1, 0, 0, 3, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 1, 3, 3, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 1, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

levelnum3 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 1],
[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 4, 4, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 3, 1, 3, 1, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 0, 0, 0, 3, 3, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 3, 3],
[0, 0, 0, 0, 0, 1, 0, 4, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 0, 0, 0, 1, 1, 0, 0, 1, 4, 4, 1, 1, 0, 0, 0, 1, 1, 1],
[0, 0, 0, 0, 3, 3, 3, 0, 0, 3, 3, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1, 1, 3, 3, 3, 1, 1, 3, 1, 0, 0, 0, 0, 1, 3, 3, 3, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
]

levelnum4 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
[0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 3, 0, 0, 0],
[1, 1, 0, 4, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0],
[0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 4, 4, 0, 0, 0, 0, 0],
[0, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
[0, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 1, 3, 1, 3, 1, 0, 0, 0, 4, 4, 4, 4, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 4, 4, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0],
[1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0],
[0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 4, 0, 3, 3, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 3, 3, 0, 0, 0, 1, 3, 3],
[0, 0, 0, 0, 0, 0, 0, 4, 4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 1, 0, 0, 0, 1, 1, 0, 1, 1, 4, 4, 1, 1, 0, 0, 0, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 3, 3, 1, 3, 3, 1, 3, 1, 1, 1, 1, 3, 3, 3, 1, 1, 3, 1, 0, 0, 0, 0, 1, 3, 3, 3, 1, 1, 1],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1],
]

levelnum5 = [
[6, 6, 6, 6, 6, 6, 6, 6, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 6, 6, 6, 6, 6, 6],
[6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 6, 6, 6, 6, 6, 6],
[6, 6, 6, 6, 6, 6, 6, 1, 4, 1, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 6, 6, 6, 6, 6],
[6, 6, 6, 6, 6, 6, 1, 4, 0, 1, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 4, 1, 6, 6, 6, 6],
[6, 6, 6, 6, 6, 6, 1, 0, 0, 1, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 6, 6, 6],
[6, 6, 6, 6, 1, 6, 1, 3, 0, 1, 1, 1, 1, 1, 6, 0, 0, 0, 0, 1, 3, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1, 6, 6],
[6, 6, 1, 1, 1, 6, 6, 1, 3, 4, 4, 4, 4, 1, 6, 6, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 6, 6],
[6, 1, 4, 0, 1, 6, 6, 6, 1, 0, 0, 0, 0, 1, 1, 6, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 1, 4, 0, 0, 0, 0, 0, 0, 0, 1, 6, 6],
[1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 6, 1, 1, 0, 0, 6, 6, 6, 6, 6, 1, 1, 1, 4, 0, 0, 0, 1, 1, 0, 0, 0, 4, 1, 6],
[4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 6, 6, 1, 1, 1, 4, 4, 4, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 1, 6],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 4, 4, 4, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1],
[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 6, 0, 0, 0, 0, 1, 3, 3, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 4],
[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0, 0, 0, 4, 1, 1, 4, 4, 0, 3, 1, 4, 0, 0, 0, 0, 0],
[1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 3, 1, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0],
[4, 1, 0, 0, 0, 0, 4, 4, 0, 0, 3, 0, 4, 4, 1, 1, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
[0, 4, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6],
[0, 0, 0, 0, 0, 0, 3, 0, 0, 4, 4, 0, 0, 0, 0, 6, 6, 6, 1, 1, 1, 1, 1, 1, 1, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6],
[0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 1, 4, 4, 0, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 6],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 1, 0, 0, 0, 0, 3, 3, 1, 6, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 1, 6, 6],
[1, 1, 1, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 1, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6, 6, 6],
]

zombie_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
spikesdown_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()



# Function for main menu
def mainmenu():
  global world
  global levelstate
  global name

  print(name)
  screen.fill((33, 33, 33)) 
  title(180,-50)
  fspicture(10,50)

  if Play_button.draw(screen):
    levelstate = 1
    world = World(levelnum1)
  if Exit_button.draw(screen):
    pygame.quit()
    sys.exit()
  if Highscore_button.draw(screen):
    levelstate = -1
  if Controls_button.draw(screen):
    print('Controls')
    levelstate = -2
  if Difficulty_button.draw(screen):
    print('Difficulty')
    levelstate = -3

  draw_text("Start",font, white, 300,200) 
  draw_text("Exit",font, white, 10,400) 
  draw_text("Controls",font, white, 600,330) 
  draw_text("High Score",font, white, 300,330) 
  draw_text("Difficulty",font, white, 600,200)  

def level1():
    global name
    global levelstate
    global score
    global game_over
    global world
    global player
    global score_value

    print(name)
    screen.blit(bg_img, (0,0))
    world.draw()
    zombie_group.draw(screen)
    spikes_group.draw(screen)
    spikesdown_group.draw(screen)
    door_group.draw(screen)
    lava_group.draw(screen)
    score_value += (1/60)
    show_score(400,10)
    if game_over == 0:
        zombie_group.update()
             # update score
    elif game_over == 1 :

       f = open("highscores.txt", "a")
       f.write( "1," + name + "," + str(score_value) + "\n")
       print(levelstate)
       f.close()
       levelstate = 2  
       player = Player(30, height - 40)
       game_over = 0
       score = 0
       score_value = 0
       world = World(levelnum2)
    game_over = player.update(game_over)
 
def level2():
    global name
    global levelstate
    global score
    global game_over
    global world
    global player
    global score_value


    screen.blit(bg_img, (0,0))
    world.draw()
    zombie_group.draw(screen)
    spikes_group.draw(screen)
    spikesdown_group.draw(screen)
    door_group.draw(screen)
    lava_group.draw(screen)
    score_value += (1/60)
    show_score(400,10)
    if game_over == 0:
        zombie_group.update()
             # update score
    elif game_over == 1:
       f = open("highscores.txt", "a")
       f.write( "2," + name + "," + str(score_value) + "\n")
       f.close()
       levelstate = 3  
       player = Player(30, height - 40)
       game_over = 0 
       score = 0
       score_value = 0
       world = World(levelnum3)
    game_over = player.update(game_over)

def level3():
    global name
    global levelstate
    global score
    global game_over
    global world
    global player
    global score_value

    screen.blit(bg_img, (0,0))
    world.draw()
    zombie_group.draw(screen)
    spikes_group.draw(screen)
    spikesdown_group.draw(screen)
    door_group.draw(screen)
    lava_group.draw(screen)
    score_value += (1/60)
    show_score(400,10)
    if game_over == 0:
        zombie_group.update()
             # update score
    elif game_over == 1:
       levelstate = 0
       f = open("highscores.txt", "a")
       f.write( "3," + name + "," + str(score_value) + "\n")
       f.close()
       levelstate = 4
       player = Player(30, height - 40)
       game_over = 0
       score = 0
       score_value = 0
       world = World(levelnum4)
    game_over = player.update(game_over)

def level4():
    global name
    global levelstate
    global score
    global game_over
    global world
    global player
    global score_value

    screen.blit(bg3_img, (0,0))
    world.draw()
    zombie_group.draw(screen)
    spikes_group.draw(screen)
    spikesdown_group.draw(screen)
    door_group.draw(screen)
    lava_group.draw(screen)
    score_value += (1/60)
    show_score(400,10)
    if game_over == 0:
        zombie_group.update()
             # update score
    elif game_over == 1:
       levelstate = 0
       f = open("highscores.txt", "a")
       f.write( "3," + name + "," + str(score_value) + "\n")
       f.close()
       levelstate = 5
       player = Player(30, height - 40)
       game_over = 0
       score = 0
       score_value = 0
       world = World(levelnum4)
    game_over = player.update(game_over)


def level5():
    global name
    global levelstate
    global score
    global game_over
    global world
    global player
    global score_value

    screen.blit(bg2_img, (0,0))
    world.draw()
    zombie_group.draw(screen)
    spikes_group.draw(screen)
    spikesdown_group.draw(screen)
    door_group.draw(screen)
    lava_group.draw(screen)
    score_value += (1/60)
    show_score(400,10)
    if game_over == 0:
        zombie_group.update()
             # update score


    elif game_over == 1:
       levelstate = 0
       f = open("highscores.txt", "a")
       f.write( "5," + name + "," + str(score_value) + "\n")
       f.close()
       player = Player(30, height - 40)
       game_over = 0
       score = 0
       world = World(levelnum4)
    game_over = player.update(game_over)

def highscores():
    global levelstate
    screen.fill((0, 150, 150))
    f = open("highscores.txt", "r")
    scores = {"1": [], "2": [], "3": [], "4": [], "5": []}  # Add level 5
    for line in f:
        line = line.strip()
        if len(line.split(",")) != 3:
            continue
        level, name, score = line.split(",")
        try:
            score = float(score)
        except ValueError:
            continue
        if level in scores:  # Check if the level is valid
            scores[level].append((name, score))
    f.close()

    draw_text('HIGH SCORES', font, white, 300, 40)

    y = 120
    for i_1, level in enumerate(sorted(scores.keys())):
        x = 200 * i_1
        draw_text(f"Level {level}", font, white, x, 120)
        y = 190
        level_scores = sorted(scores[level], key=lambda x: x[1])
        for i, (name, score) in enumerate(level_scores):
            draw_text(f"{i+1}. {name} - {score:.2f}", font, white, x, y)
            y += 40
        y += 50

    if back_button.draw(screen):
        levelstate = 0
    draw_text('back', font, white, 40, 10)




def controls():
    global levelstate
    screen.fill((150,150,0))
    screen.blit(controls_img, (200,200))
    draw_text(("Use arrow keys to move the player"), font, white, 100, 150)
    if back_button.draw(screen):
        levelstate = 0
    draw_text('back', font, white, 40, 10)



def difficulty():
    global levelstate, world

    screen.fill((150,0,150))
    if back_button.draw(screen):
        levelstate = 0
    if easy_button.draw(screen):
        levelstate = 1
        world = World(levelnum1)
    if medium_button.draw(screen):
        levelstate = 2
        world = World(levelnum2)
    if difficult_button.draw(screen):
        levelstate = 3
        world = World(levelnum3)
    if extreme_button.draw(screen):
        levelstate = 4
        world = World(levelnum4)
    if impossible_button.draw(screen):
        levelstate = 5
        world = World(levelnum5)

    draw_text('back', font, white, 40, 10)
    draw_text(("Easy"), font, white, 300, 200)
    draw_text(("Medium"), font, white, 300, 300)
    draw_text(("Difficult"), font, white, 300, 400)
    draw_text(("Extreme"), font, red, 600, 300)
    draw_text(("Impossible"), font, black, 600, 400)

def entername():
    global levelstate
    global font
    global name
    screen.fill((0,0,0))

    # create a text input box using pygame's Rect and Surface objects
    input_box = pygame.Rect(250, 250, 200, 32)
    input_box_color = white
    name = ""


    # run a loop to handle user input and update the screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # return the user's input if they press the Enter key
                    levelstate = 0
                    return name
                    

                elif event.key == pygame.K_BACKSPACE:
                    # remove the last character from the input text if the user presses Backspace
                    name = name[:-1]
                    print(name)
                    print("testing")
                else:
                    # add the typed character to the input text
                    name += event.unicode
        # update the input box color based on whether it has focus
        if input_box.collidepoint(pygame.mouse.get_pos()):
            input_box_color = ((30,30,30))
        else:
            input_box_color = white

        # draw the input box and text on the screen
        screen.fill((0,0,0))
        draw_text("Enter your name:", font, white, 250, 200)
        pygame.draw.rect(screen, input_box_color, input_box, 2)
        text_surface = font.render(name, True, white)
        screen.blit(text_surface, (input_box.x+5, input_box.y+5))


        # update the display
        pygame.display.update()

def show_score(x,y):
  score = font.render("Time :" + str(math.floor(score_value)),True, (255,0,0))
  screen.blit(score, (x,y))


def mainloop():
    global levelstate
    
    run = True
    while run:

        clock.tick(fps)
        if levelstate == -4:
            entername()
        if levelstate == -1:
            highscores()
        if levelstate == -2:
            controls()
        if levelstate == -3:
            difficulty()
        if levelstate == 0:
            mainmenu()
        elif levelstate == 1:
            level1()
        elif levelstate == 2:
            level2() 
        elif levelstate == 3:
            level3()
        elif levelstate == 4:
            level4()
        elif levelstate == 5:
            level5()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()
mainloop()