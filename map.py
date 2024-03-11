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
    
    def switch_map(self, map:str):
        #chargement de la carte
        self.tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data,self.screen.get_size())
        
        #dessiner le groupe de calques
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=3)
    
    def add_player(self,player):
        self.group.add(player)

    def update(self,player):
        self.group.update()# je sais pas encore
        player.action()# déplacement de joueur en fonction de touche clavier
        self.group.draw(self.screen.get_display())
    
    def remove_player(self, player): 
            self.group.remove(player)