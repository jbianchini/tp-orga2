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


def extract_coin_sequence(output):
    """Returns the ordered list of remaining-coin counts emitted by the script."""
    return [int(match) for match in re.findall(r"Quedan (\d+)", output)]


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
        sequences = []
        expected_sequence = list(range(9, -1, -1))  # 9 down to 0

        for run in range(10):
            output, _ = run_simulation()
            sequence = extract_coin_sequence(output)
            sequences.append(sequence)
            print(f"Run {run + 1}: {' '.join(map(str, sequence))}")
            self.assertEqual(
                sequence,
                expected_sequence,
                msg=f"Secuencia inesperada: {sequence}",
            )

        # All recorded sequences must be identical
        unique_sequences = {tuple(seq) for seq in sequences}
        self.assertEqual(
            len(unique_sequences),
            1,
            msg="Las ejecuciones no fueron deterministas en el patrón de monedas.",
        )


if __name__ == "__main__":
    unittest.main()
