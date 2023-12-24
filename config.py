ENGINE_EXECUTABLE_PATH = "stockfish/stockfish-windows-x86-64-modern.exe"

DEFAULT_DIFFICULTY = 1200

CUSTOM_DIFFICULTY = 1200

BAR_ENABLED = True

RATING_FILE_PATH = 'player_rating.txt'

class TerminalColors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_YELLOW = '\033[93;1m'
    BLACK = '\033[30m'
    END = '\033[0m'


OPTIONS_TEXT = f'''{TerminalColors.LIGHT_YELLOW}
Welcome to Python Blindfold Chess!

{TerminalColors.YELLOW}Choose an option:
{TerminalColors.GREEN}1. Start the game!
{TerminalColors.END}2. Settings.
3. About the game.
{TerminalColors.RED}0. Exit the game.{TerminalColors.END}
Enter your choice: '''
