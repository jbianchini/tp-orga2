import threading
import time
import random

class CoinChest:
    def __init__(self, name, coins):
        self.name = name
        self.coins = coins
        self.lock = threading.Lock()

    def take_coin(self, player_name):
        with self.lock: # Asegura acceso exclusivo
            #inicio seccion crítica
            if self.coins > 0:
                time.sleep(random.uniform(0.01, 0.05))  # Simula retraso
                self.coins -= 1
                print(f"{player_name} tomó una moneda en {self.name}. Quedan {self.coins}.")
                return True  # Informe de éxito
            else:
                print(f"{player_name} no pudo tomar moneda en {self.name}: cofre vacío.")
                return False  # Informe de fracaso
            #fin seccion crítica

# Cofres compartidos
chest_a = CoinChest("Cofre A", 10)
chest_b = CoinChest("Cofre B", 5)

# Cada jugador intentará tomar monedas varias veces
def player_action(player_name, chest):
    while True:
        if not chest.take_coin(player_name):
            break  # Evita seguir intentando cuando el cofre está vacío
        time.sleep(random.uniform(0.01, 0.05))  # Espera aleatoria antes de volver a intentar

# Crear y lanzar hilos para 5 jugadores por cofre
threads = []
for i in range(5):
    t = threading.Thread(target=player_action, args=(f"A-Jugador-{i+1}", chest_a))
    threads.append(t)
    t.start()

for i in range(3):
    t = threading.Thread(target=player_action, args=(f"B-Jugador-{i+1}", chest_b))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("programa terminado")
