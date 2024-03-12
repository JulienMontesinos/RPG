import pygame
import pytmx
import pyscroll
from screen import Screen
from player import Player


class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.group = None
        self.switch_map("map0")
        self.font = pygame.font.Font(None, 36)
    
    def switch_map(self, map:str):
        #chargement de la carte
        self.tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data,self.screen.get_size())
        
        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.obstacles = []
        self.panneau = []
        for obj in self.tmx_data.objects:
             if obj.type == "collision":
                  self.obstacles.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
             elif obj.type == "sign":
                 self.panneau.append({
                    "rect": pygame.Rect(obj.x, obj.y, obj.width, obj.height),
                    "message": obj.properties.get("message", "Bienvenue dans le monde RPG!")  
                })
        
    def display_sign_message(self, message):
        text_surface = self.font.render(message, True, (255, 255, 255))
        self.screen.get_display().blit(text_surface, (100, 100))        
    
    def add_player(self,player):
        self.group.add(player)

    def update(self,player):
        keys_pressed = pygame.key.get_pressed()
        print(keys_pressed[pygame.K_RETURN])
        panneau_rects = [panneau["rect"] for panneau in self.panneau]
        self.group.update()
        for sprite in self.group.sprites():
             if sprite.feet.collidelist(self.obstacles) >-1:
                  sprite.move_back() 
             
             collided_index = sprite.feet.collidelist(panneau_rects)
             if collided_index > -1:
                 sprite.move_back() 
                 print("yo")
                 if keys_pressed[pygame.K_RETURN]:
                    self.display_sign_message(self.panneau[collided_index]["message"])
                    print("hello")
            
        player.save_location()         
        player.action_key()
        player.action_mouse()
        self.group.draw(self.screen.get_display())
    
    def remove_player(self, player): 
            self.group.remove(player)