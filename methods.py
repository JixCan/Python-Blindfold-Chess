import config
import chess


def generate_lichess_analysis_link(fen):
    base_url = "https://lichess.org/analysis/"
    return f"Analysis: {base_url}{fen.replace(' ', '_')}"


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + config.TerminalColors.BLACK + '█' * (length - filledLength)
    return f'{prefix} |{bar}{config.TerminalColors.END}| {suffix}'


def print_evaluation(stockfish):
    evaluation = stockfish.get_evaluation()
    iteration = evaluation["value"] / 20 + 50
    if evaluation["type"] == "cp":
        return printProgressBar(iteration=evaluation["value"] / 20 + 50, total=100, suffix=f"{evaluation['value'] / 100}",
                         length=10)
    elif evaluation["type"] == "mate":
        return printProgressBar(iteration=0 if evaluation["value"] < 0 else 100, total=100,
                         suffix=f"Mate in {abs(evaluation['value'])}", length=10)



def check_board(board, player_color):
    if board.is_checkmate():
        print(f"{config.TerminalColors.RED}Checkmate! The game is over.{config.TerminalColors.END}")
        return True
    elif board.is_stalemate():
        print(f"{config.TerminalColors.YELLOW}Stalemate! The game is a draw.{config.TerminalColors.END}")
        return True
    elif board.is_insufficient_material():
        print(
            f"{config.TerminalColors.YELLOW}Insufficient material! The game is a draw.{config.TerminalColors.END}")
        return True
    elif board.is_fifty_moves():
        print(
            f"{config.TerminalColors.YELLOW}Insufficient material! The game is a draw.{config.TerminalColors.END}")
        return True
    elif board.is_fivefold_repetition():
        print(
            f"{config.TerminalColors.YELLOW}Fivefold repetition! The game is a draw.{config.TerminalColors.END}")
        return True
    return False


def get_user_move_san(board):
    while True:
        user_move = input(f"{config.TerminalColors.YELLOW}> {config.TerminalColors.END}Enter your move (in SAN format, e.g., e4): ")
        if user_move.lower() == "exit":
            return None
        elif user_move.lower() == "fen":
            print(generate_lichess_analysis_link(board.fen()))
            continue
        else:
            try:
                move = chess.Move.from_uci(board.parse_san(user_move).uci())  # Преобразование SAN в UCI
                if move in board.legal_moves:
                    return move
                else:
                   print("Invalid move! Try again.")
            except ValueError:
                print("Invalid input! Enter a move in SAN format (e.g., e4) or 'exit' to quit.")


def play(stockfish):
    while True:
        print("\nSelect your color:")
        print("1. White")
        print("2. Black")
        print("3. Random")
        print("0. Go back")

        color_choice = input("Enter your choice: ")

        if color_choice == "1":
            player_color = chess.WHITE
            break
        elif color_choice == "2":
            player_color = chess.BLACK
            break
        elif color_choice == "3":
            import random
            player_color = random.choice([chess.WHITE, chess.BLACK])
            break
        elif color_choice == "0":
            return
        else:
            print(f"{config.TerminalColors.RED}Invalid input! Please try again.{config.TerminalColors.END}")

    print()
    print(f"{config.TerminalColors.YELLOW}Difficulty: {config.TerminalColors.END}{config.CUSTOM_DIFFICULTY}")
    stockfish.set_elo_rating(config.CUSTOM_DIFFICULTY)

    if player_color == chess.WHITE:
        print(f"You are playing as {config.TerminalColors.YELLOW}White.{config.TerminalColors.END}")
        board = chess.Board()
    else:
        print(f"You are playing as {config.TerminalColors.YELLOW}Black.{config.TerminalColors.END}")
        board = chess.Board()
    print(f"{config.TerminalColors.YELLOW}To analyze the position, enter \"fen\". To exit, enter \"exit\".{config.TerminalColors.END}")
    while True:
        if player_color == chess.WHITE:
            user_move = get_user_move_san(board)
            if user_move is None:
                break

            board.push(user_move)

            stockfish.set_fen_position(board.fen())

            engine_move_uci = chess.Move.from_uci(stockfish.get_best_move())
            engine_move_san = board.san(engine_move_uci)
            print(f"Engine's move: {engine_move_san} " + print_evaluation(
                stockfish=stockfish) if config.BAR_ENABLED else "")

            board.push(engine_move_uci)
            if check_board(board=board):
                break
        else:
            stockfish.set_fen_position(board.fen())
            engine_move_uci = chess.Move.from_uci(stockfish.get_best_move())
            engine_move_san = board.san(engine_move_uci)
            print(f"Engine's move: {engine_move_san} " + print_evaluation(
                stockfish=stockfish) if config.BAR_ENABLED else "")
            board.push(engine_move_uci)
            user_move = get_user_move_san(board)
            if user_move is None:
                break

            board.push(user_move)
            if check_board(board=board):
                break



def settings():
    while True:
        print("\nSettings:")
        print("1. Set difficulty level.")
        print("2. Reset to default difficulty level.")
        print(f"3. Toggle evaluation bar (ENABLED: {config.BAR_ENABLED}).")
        print("0. Go back.")

        choice = input("Enter your choice: ")

        if choice == "1":
            set_difficulty()
        elif choice == "2":
            reset_to_default()
        elif choice == "3":
            config.BAR_ENABLED = not config.BAR_ENABLED
        elif choice == "0":
            break
        else:
            print(f"{config.TerminalColors.RED}Invalid input! Please try again.{config.TerminalColors.END}")


def set_difficulty():
    while True:
        elo_rating = input("Enter the difficulty level in Elo rating (from 400 to 3000): ")

        if elo_rating.isdigit():
            rating = int(elo_rating)
            if 400 <= rating <= 3000:
                config.CUSTOM_DIFFICULTY = rating
                print(f"{config.TerminalColors.GREEN}Difficulty level set successfully!{config.TerminalColors.END}")
                break
            else:
                print(
                    f"{config.TerminalColors.RED}Please enter a number between 400 and 3000.{config.TerminalColors.END}")
        else:
            print(f"{config.TerminalColors.RED}Please enter a valid number.{config.TerminalColors.END}")


def reset_to_default():
    config.CUSTOM_DIFFICULTY = config.DEFAULT_DIFFICULTY
    print(f"{config.TerminalColors.GREEN}Difficulty level reset to default.{config.TerminalColors.END}")


def about():
    print(f"{config.TerminalColors.YELLOW}Welcome to Python Blindfold Chess!{config.TerminalColors.END}")


def gameExit():
    print(f"{config.TerminalColors.YELLOW}Thanks for playing!{config.TerminalColors.END}")
    pass
