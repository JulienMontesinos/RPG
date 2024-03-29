from typing import SupportsIndex
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, p_id, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load("player.png")
        self.id = p_id
        self.image = self.get_image(0,0)
        self.image.set_colorkey([0,0,0])
        self.speed = 3
        self.x = x
        self.y = y
        self.position = [self.x, self.y]
        self.rect = self.image.get_rect(topleft=[x, y])
        self.frame_num = 0
        self.images = {
            'down': self.get_images(0), 
            'left': self.get_images(32), 
            'right': self.get_images(64),
            'up': self.get_images(96),
        }
        self.mask=pygame.mask.from_surface(self.image) 
        self.feet = pygame.Rect(0, 0, self.rect.width*0.5, 12)
        self.old_x = self.x
        self.old_y = self.y

        self.current_dir = "down"
        self.last_dir = self.current_dir
    
    def save_location(self): 
        self.old_x = self.x
        self.old_y = self.y

    def change_animation(self, name):    
        self.image = self.images[name][self.frame_num]
        self.image.set_colorkey([0,0,0])
        self.frame_num += 1
        if self.frame_num >= len(self.images[name]):
            self.frame_num =0

    def update_rect(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def move_right(self):
        self.x += self.speed
        self.update_rect()
    
    def move_left(self):
        self.x -= self.speed
        self.update_rect()

    def move_up(self):
        self.y -= self.speed
        self.update_rect()

    def move_down(self):
        self.y += self.speed
        self.update_rect()

    def action_key(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.move_left()
            self.current_dir = "left"
            self.change_animation('left')

        elif keys[pygame.K_RIGHT]:
            self.move_right()
            self.current_dir = "right"
            self.change_animation('right')

        elif keys[pygame.K_UP]:
            self.move_up()
            self.current_dir = "up"
            self.change_animation('up')

        elif keys[pygame.K_DOWN]:
            self.move_down()
            self.current_dir = "down"
            self.change_animation('down')

        self.last_dir = self.current_dir
    
    def action_mouse(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
         x_position, y_position = event.pos
         if x_position > self.x:
             while x_position > self.x:
                 self.move_right()  
                 self.current_dir = "right"
                 self.change_animation('right')
             if y_position > self.y:
                 while y_position > self.y:
                     self.move_up()
                     self.current_dir = "up"
                     self.change_animation('up')
             elif y_position < self.y:
                 while y_position < self.y:  
                     self.move_down()
                     self.current_dir = "down"
                     self.change_animation('down')
         elif x_position < self.x:
             while x_position < self.x:
                 self.move_left()  
                 self.current_dir = "left"
                 self.change_animation("left")
             if y_position > self.y:
                 while y_position > self.y:
                     self.move_up()
                     self.current_dir = "up"
                     self.change_animation('up')
             elif y_position < self.y:
                 while y_position < self.y: 
                     self.move_down()
                     self.current_dir = "down"
                     self.change_animation('down')


    def get_images(self,y):
        images =[]
        for i in range(0,3):
            x = i*32
            image = self.get_image(x,y)
            images.append(image)
        return images


    def get_image(self, x, y):
        image = pygame.Surface([32,32])
        image.blit(self.sprite_sheet, (0,0), (x,y,32,32))
        return image

    
    def update(self):
        self.rect.topleft = [self.x,self.y]
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.x = self.old_x
        self.y = self.old_y
        self.rect.topleft = [self.x,self.y]
        self.feet.midbottom = self.rect.midbottom