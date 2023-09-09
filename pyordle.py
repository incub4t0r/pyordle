from GameBoard import GameBoard

if __name__ == "__main__":
    game = GameBoard()
    while True:
        game.clear_screen()
        if game.guess_count == 6:
            game.lose_screen()
            break
        game.display_previous_guesses()
        game.print_keyboard()
        game.get_user_input()
        game.validate_user_input()
        if game.check_user_input():
            game.win_screen()
            break
