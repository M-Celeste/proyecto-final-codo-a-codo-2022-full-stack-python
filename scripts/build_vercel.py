"""Publica los recursos estáticos en la CDN conservando sus URLs /static/."""
from pathlib import Path
from shutil import copytree


def main():
    root = Path(__file__).resolve().parent.parent
    copytree(root / "static", root / "public" / "static", dirs_exist_ok=True)
    print("Recursos estáticos preparados para Vercel.")


if __name__ == "__main__":
    main()
