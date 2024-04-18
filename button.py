import pygame, sys

#create button class
class Button():  
  def __init__(self, x, y,image, scale ):  
    height  = image.get_height()
    width = image.get_width()
    self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    #shows where everything is positioned in the rectangle
    self.rect = self.image.get_rect()  
    self.rect.topleft = (x, y)  
    self.clicked = False
  
  def draw(self, surface):  
    action = False
    #get the mouse position
    pos= pygame.mouse.get_pos()

    #check mouseover and clicked conditions
    if self.rect.collidepoint(pos):
      surface.blit(self.image, (self.rect.x, self.rect.y))  
      self.top_colour = (50, 50, 50)
      if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
        self.clicked = True
        action = True
    else:
          surface.blit(self.image, (self.rect.x, self.rect.y))  

    if pygame.mouse.get_pressed()[0] == 0:
      self.clicked = False

    #blit is used to draw button on window 

    
    return action