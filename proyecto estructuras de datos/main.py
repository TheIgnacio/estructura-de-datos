import sys
from pathlib import Path

# Agrega la raiz del proyecto al path para que los imports funcionen
sys.path.append(str(Path(__file__).resolve().parent))

if __name__ == "__main__":
    import UX.Menu
