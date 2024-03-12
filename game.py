import sys
import pygame
import pickle
import socket
from player import Player
from random import randint
from screen import Screen
from map import Map

class Game:
    def __init__(self):
        pygame.init()
        self.other_players = {}
        self.screen = Screen()
        self.map = Map(self.screen)
        self.player = Player(
                             p_id=None, 
                             x=randint(35, 310),
                             y=randint(300, 430),            
                             )
        self.map.add_player(self.player)
        self.port = 5555
        self.host = "10.0.94.50"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(4096).decode("utf-8")

    def send_player_data(self):
        data = {
            "id": self.player.id,
            #"position": self.player.position,
            "x": self.player.x,
            "y": self.player.y,
            "old_x": self.player.old_x,
            "old_y": self.player.old_y,
            "frame_num": self.player.frame_num,
            "current_dir": self.player.current_dir
        }
        self.sock.send(pickle.dumps(data))
        response = self.sock.recv(4096)
        return response

    def update_other_players_data(self, data):
     received_data = pickle.loads(data)
     current_active_ids = set(received_data.keys())

     for player_id in list(self.other_players.keys()):
         if player_id not in current_active_ids and player_id != self.player.id:
             self.map.remove_player(self.other_players[player_id])  
             del self.other_players[player_id]

     for player_id, (x , y, old_x, old_y, frame_num,current_dir) in received_data.items():
         if player_id == self.player.id:
            continue  
         if player_id in self.other_players:
            existing_player = self.other_players[player_id]
            existing_player.x = x
            existing_player.y =y
            existing_player.old_x = old_x
            existing_player.old_y = old_y
            existing_player.frame_num = frame_num
            existing_player.current_dir = current_dir
            existing_player.change_animation(current_dir)
            existing_player.rect.topleft = [x,y]
            existing_player.save_location()
            #if pygame.sprite.collide_circle(self.player, existing_player):
            if pygame.sprite.collide_mask(self.player, existing_player):
                #print("hello")
                self.player.move_back()
                self.player.save_location()
                
         else:
            new_player = Player(p_id=player_id, x = x, y = y)
            self.other_players[player_id] = new_player
            self.map.add_player(new_player)


    def update_screen(self):
        self.map.update(self.player)
        other_players_data = self.send_player_data()
        self.update_other_players_data(other_players_data)
        self.screen.update()

    def start(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_screen()