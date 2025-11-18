import re
import subprocess
import sys
import time
from pathlib import Path
import unittest

SCRIPT_PATH = Path(__file__).with_name("Bug07.py")


def run_simulation():
    """Executes the main script and returns stdout plus elapsed time."""
    start = time.perf_counter()
    completed = subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        check=True,
    )
    duration = time.perf_counter() - start
    return completed.stdout, duration


def extract_sequences(output):
    """Returns per-chest sequences of remaining-coin counts from the script output."""
    matches = re.findall(r"en (Cofre [AB]).+?Quedan (\d+)", output)
    chest_data = {}
    for chest, value in matches:
        chest_data.setdefault(chest, []).append(int(value))
    return chest_data


class CoinChestTests(unittest.TestCase):
    def test_performance_under_threshold(self):
        """The simulation with 10 coins should finish in less than 2 secs."""
        _, duration = run_simulation()
        self.assertLess(
            duration,
            2.0,
            msg=f"La simulación tardó demasiado: {duration:.2f}s",
        )

    def test_repeated_runs_same_coin_sequence(self):
        """Multiple executions should depleat the chest in the same pattern."""
        expected_a = list(range(9, -1, -1))  # 9..0
        expected_b = list(range(4, -1, -1))  # 4..0

        for run in range(10):
            output, _ = run_simulation()
            sequences = extract_sequences(output)
            print(
                f"Run {run + 1}: Cofre A -> {' '.join(map(str, sequences.get('Cofre A', [])))} "
                f"| Cofre B -> {' '.join(map(str, sequences.get('Cofre B', [])))}"
            )
            self.assertEqual(sequences.get("Cofre A"), expected_a)
            self.assertEqual(sequences.get("Cofre B"), expected_b)


if __name__ == "__main__":
    unittest.main()
