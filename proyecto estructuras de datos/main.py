import sys
from pathlib import Path

# Agrega la raiz del proyecto al path para que los imports funcionen
base = Path(__file__).resolve().parent
if str(base) not in sys.path:
    sys.path.append(str(base))

from UX.Menu import iniciar_menu


def main():
    iniciar_menu()


if __name__ == "__main__":
    main()
