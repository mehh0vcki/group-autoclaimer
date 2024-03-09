import os, json
from rgbprint import gradient_print
from pyfiglet import Figlet

def get_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except:
        return 80  # default width

def middle_text(text: str, width: int) -> str:
    padding: int = (width - len(text)) // 2
    return " " * padding + text

def generate_logo() -> None:
    width: int = get_terminal_width()
    figlet = Figlet("elite", width=width)
    art: str = figlet.renderText("mehhovcki")
    center: str = "\n".join(middle_text(line, width) for line in art.splitlines())
    gradient_print(center, start_color="#fa5796", end_color="#99254f")

def generate_text(text: str, level: int) -> None:
    levels = {0: "default", 1: "account", 2: "default", 3: "debug"}
    width: int = get_terminal_width()

    with open("files/settings.json", "r") as file:
        data = json.load(file)
    colors = data["colors"][levels[level]]
    gradient_print(middle_text(text, width), start_color=colors[0], end_color=colors[1])