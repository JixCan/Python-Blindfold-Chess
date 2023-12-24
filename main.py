import config
import methods
from stockfish import Stockfish

print(">>> Loading engine...", end=' ')

try:
    stockfish = Stockfish(path=config.ENGINE_EXECUTABLE_PATH)
except (FileNotFoundError, AttributeError) as e:
    print(f"{config.TerminalColors.RED}Error loading engine!{config.TerminalColors.END}")
    print("Place the executable in the specified directory in your \"config.py\" file!")
    exit()

print(f"{config.TerminalColors.GREEN}Done!{config.TerminalColors.END}")

while True:
    options_input = input(config.OPTIONS_TEXT)

    if options_input == "1":
        methods.play(stockfish=stockfish)
        continue
    elif options_input == "2":
        methods.settings()
        continue
    elif options_input == "3":
        methods.about()
        continue
    elif options_input == "0":
        methods.gameExit()
        break
    else:
        print(f"{config.TerminalColors.RED}Input Error! Please try again.{config.TerminalColors.END}")
