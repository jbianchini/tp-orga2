import argparse
import random
import threading
import time
from typing import Dict, List, Optional, Tuple

# ----- Código adaptado: representación en consola -----
COIN_PRESENT = "O"
COIN_TAKEN = "."


def render_state(initial_coins: int, coins_left: int) -> str:
    removed = initial_coins - coins_left
    coins = [
        COIN_TAKEN if idx < removed else COIN_PRESENT
        for idx in range(initial_coins)
    ]
    return "".join(coins)


# ----- Código original: lógica de CoinChest y concurrencia -----
class CoinChest:
    def __init__(self, coins: int, verbose: bool = True):
        self.coins = coins #se agrega config para cantidad de coins
        self.verbose = verbose
        self.lock = threading.Lock()

    def take_coin(self, player_name: str) -> Tuple[bool, int]: #Intenta sacar una moneda y devuelve (éxito, monedas restantes)
        with self.lock: # Asegura acceso exclusivo
            #inicio seccion crítica
            if self.coins > 0:
                time.sleep(random.uniform(0.01, 0.05))  # Simula retraso
                self.coins -= 1
                if self.verbose:
                    print(f"{player_name} tomó una moneda. Quedan {self.coins}.")
                return True, self.coins # además devuelve el número restante
            else:
                if self.verbose:
                    print(f"{player_name} no pudo tomar moneda: cofre vacío.")
                return False, self.coins # acá también
            #fin seccion crítica

# ----- Código adaptado: run de simulación en consola -----
def run_simulation(
    num_players: int = 5,
    initial_coins: int = 10,
    verbose: bool = True,
    collect_events: bool = False,
) -> Optional[List[Dict[str, object]]]:
    """Ejecuta la simulación y opcionalmente devuelve un log de eventos."""
    chest = CoinChest(initial_coins, verbose=verbose)
    events: Optional[List[Dict[str, object]]] = [] if collect_events else None

    def record_event(player_name: str, success: bool, remaining: int) -> None:
        if events is not None:
            events.append(
                {
                    "player": player_name,
                    "success": success,
                    "coins_left": remaining,
                }
            )

# ----- Código original: player action, threads -----
    def player_action(player_name: str) -> None:
        while True:
            success, remaining = chest.take_coin(player_name)
            record_event(player_name, success, remaining)
            if not success:
                break  # Evita seguir intentando cuando el cofre está vacío
            time.sleep(random.uniform(0.01, 0.05))  # Espera antes de reintentar

    threads = []
    for i in range(num_players):
        t = threading.Thread(target=player_action, args=(f"Jugador-{i+1}",))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return events


# ----- Código adaptado: animación textual en consola -----
def simulate_console(
    num_players: int,
    initial_coins: int,
    interval: float,
) -> None:
    events = run_simulation(
        num_players=num_players,
        initial_coins=initial_coins,
        verbose=False,
        collect_events=True,
    )

    if not events:
        print("No hay eventos que mostrar.")
        return

    success_events = [event for event in events if event["success"]]
    if not success_events:
        print("El cofre ya estaba vacío.")
        return

    print(
        f"Iniciando simulación con {num_players} jugadores y {initial_coins} monedas.\n"
    )

    for idx, event in enumerate(success_events, start=1):
        coins_left = event["coins_left"]
        state = render_state(initial_coins, coins_left)
        print(
            f"{idx:02d}. {event['player']} tomó una moneda -> {state} "
            f"({coins_left} restantes)"
        )
        time.sleep(interval)

    print("\nCofre vacío. Simulación finalizada.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Visualización simple en consola de la simulación."
    )
    parser.add_argument("--players", type=int, default=10, help="Cantidad de jugadores.")
    parser.add_argument("--coins", type=int, default=20, help="Monedas iniciales.")
    parser.add_argument(
        "--interval",
        type=float,
        default=0.1,
        help="Tiempo (en segundos) entre cada línea mostrada.",
    )
    args = parser.parse_args()

    simulate_console(
        num_players=args.players,
        initial_coins=args.coins,
        interval=max(0.0, args.interval),
    )
