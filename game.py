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
        self.other_players = {}

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(4096).decode("utf-8")

    def send_player_data(self):
        data = {
            "id": self.player.id,
            "position": self.player.position,
            "frame_num": self.player.frame_num,
            "current_dir": self.player.current_dir
        }
        self.sock.send(pickle.dumps(data))
        response = self.sock.recv(4096)
        return response

    #def update_other_players_data(self, data):
        received_data = pickle.loads(data)
        current_active_ids = set(received_data.keys())

        # supprimer les joueurs deconnecte
        for player_id in list(self.other_players.keys()):
            if player_id not in current_active_ids and player_id != self.player.id:
               self.map.remove_player(self.other_players[player_id])  
               del self.other_players[player_id]
        # update ou ajoueter nouveau joueurs
        for player_id, value in received_data.items():
            if player_id == self.player.id:
                continue  
            if player_id in self.other_players:
               existing_player = self.other_players[player_id]
               existing_position = value[0]
               existing_player.frame_num = value[1]
               existing_player.current_dir = value[2]
               existing_player.rect.topleft = value[0]
            else:
               new_player = Player(p_id=player_id, x=value["position"][0], y=value["position"][1])
               self.other_players[player_id] = new_player
               self.map.add_player(new_player)

    def update_other_players_data(self, data):
     received_data = pickle.loads(data)
     current_active_ids = set(received_data.keys())

     for player_id in list(self.other_players.keys()):
         if player_id not in current_active_ids and player_id != self.player.id:
             self.map.remove_player(self.other_players[player_id])  
             del self.other_players[player_id]

     for player_id, (position, frame_num, current_dir) in received_data.items():
         if player_id == self.player.id:
            continue  
         if player_id in self.other_players:
            existing_player = self.other_players[player_id]
            existing_player.position = position
            existing_player.frame_num = frame_num
            existing_player.current_dir = current_dir
            existing_player.rect.topleft = position
         else:
            new_player = Player(p_id=player_id, x=position[0], y=position[1])
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
            clock.tick(20)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_screen()

if __name__ == "__main__":
    game = Game()
    game.start()