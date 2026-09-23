import sys
from pathlib import Path

# Ensures `from src.taskN import ...` resolves when pytest is run
# from anywhere (repo root, homework1/, or inside tests/).
sys.path.insert(0, str(Path(__file__).resolve().parent))
