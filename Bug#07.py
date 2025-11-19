import threading
import time
import random

class CoinChest:
    def __init__(self, coins):
        self.coins = coins

    def take_coin(self, player_name):
        if self.coins > 0:
            time.sleep(random.uniform(0.01, 0.05))  # Simula retraso
            self.coins -= 1
            print(f"{player_name} tomó una moneda. Quedan {self.coins}.")
        else:
            print(f"{player_name} no pudo tomar moneda: cofre vacío.")

# Cofre compartido
chest = CoinChest(10)

# Cada jugador intentará tomar monedas varias veces
def player_action(player_name):
    while chest.coins > 0:
        chest.take_coin(player_name)
        time.sleep(random.uniform(0.01, 0.05))  # Espera aleatoria antes de volver a intentar

# Crear y lanzar hilos para 5 jugadores
threads = []
for i in range(5):
    t = threading.Thread(target=player_action, args=(f"Jugador-{i+1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
