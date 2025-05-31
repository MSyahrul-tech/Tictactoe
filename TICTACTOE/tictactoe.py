import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 360, 480
LINE_WIDTH = 6
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = SQUARE_SIZE // 4

BG_COLOR = (245, 232, 192)
LINE_COLOR = (139, 69, 19)
CROSS_COLOR = (0, 0, 0)
CIRCLE_COLOR = (105, 105, 105)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (205, 133, 63)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('X O AI')

font = pygame.font.SysFont(None, 35)

board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
player_turn = True
game_over = False
winner_text = ""
difficulty_level = "Medium"

player_symbol = 'X'
ai_symbol = 'O'
player_starts = True  # True = player first pick, False = AI first pick
game_end_time = None  # Untuk delay tampilan hasil

game_state = "start_screen"
post_game_buttons = {}

def draw_lines():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

def check_winner(player):
    for row in board:
        if row == [player] * BOARD_COLS:
            return True
    for col in range(BOARD_COLS):
        if [board[row][col] for row in range(BOARD_ROWS)] == [player] * BOARD_ROWS:
            return True
    if [board[i][i] for i in range(BOARD_ROWS)] == [player] * BOARD_ROWS:
        return True
    if [board[i][BOARD_ROWS - i - 1] for i in range(BOARD_ROWS)] == [player] * BOARD_ROWS:
        return True
    return False

def is_board_full():
    for row in board:
        if None in row:
            return False
    return True

def minimax(board_state, depth, is_maximizing):
    if check_winner(ai_symbol):
        return 1
    elif check_winner(player_symbol):
        return -1
    elif is_board_full():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board_state[row][col] is None:
                    board_state[row][col] = ai_symbol
                    score = minimax(board_state, depth + 1, False)
                    board_state[row][col] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board_state[row][col] is None:
                    board_state[row][col] = player_symbol
                    score = minimax(board_state, depth + 1, True)
                    board_state[row][col] = None
                    best_score = min(score, best_score)
        return best_score

def ai_move_random():
    empty = [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]
    if empty:
        move = random.choice(empty)
        board[move[0]][move[1]] = ai_symbol

def ai_move():
    if difficulty_level == "Easy":
        ai_move_random()
    elif difficulty_level == "Medium":
        # Cek kemenangan AI dulu
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = ai_symbol
                    if check_winner(ai_symbol):
                        return
                    board[row][col] = None
        # Cegah kemenangan player
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    board[row][col] = player_symbol
                    if check_winner(player_symbol):
                        board[row][col] = ai_symbol
                        return
                    board[row][col] = None
        ai_move_random()
    else:
        best_score = -float('inf')
        move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = ai_symbol
                    score = minimax(board, 0, False)
                    board[row][col] = None
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        if move:
            board[move[0]][move[1]] = ai_symbol

def draw_text_center(text, y):
    label = font.render(text, True, TEXT_COLOR)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, y))

def restart_game():
    global board, player_turn, game_over, winner_text, player_starts, game_end_time
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    game_over = False
    winner_text = ""
    game_end_time = None
    player_turn = player_starts

    if not player_starts:
        ai_move()
        player_turn = True

def draw_start_screen():
    screen.fill(BG_COLOR)
    draw_text_center("X O AI", HEIGHT // 4)
    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 32, 150, 65)
    pygame.draw.rect(screen, BUTTON_COLOR, start_button, border_radius=10)
    label = font.render("Start Game", True, TEXT_COLOR)
    screen.blit(label, label.get_rect(center=start_button.center))
    return start_button

def draw_symbol_selection():
    screen.fill(BG_COLOR)
    draw_text_center("Pilih Simbol:", 50)
    buttons = {
    "X": pygame.Rect(WIDTH // 2 - 75, 120, 150, 70),
    "O": pygame.Rect(WIDTH // 2 - 75, 210, 150, 70)
    }   

    for symbol, rect in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
        label = font.render(symbol, True, TEXT_COLOR)
        screen.blit(label, label.get_rect(center=rect.center))
    return buttons

def draw_turn_selection():
    screen.fill(BG_COLOR)
    draw_text_center("Siapa Main Duluan?", 50)
    buttons = {
    "First Pick": pygame.Rect(WIDTH // 2 - 100, 140, 200, 60),
    "Second Pick": pygame.Rect(WIDTH // 2 - 100, 230, 200, 60)
    }

    for label, rect in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
        text = font.render(label, True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))
    return buttons

def draw_level_selection():
    screen.fill(BG_COLOR)
    draw_text_center("Pilih Level:", 50)
    buttons = {
    "Easy": pygame.Rect(WIDTH // 2 - 90, 100, 180, 60),
    "Medium": pygame.Rect(WIDTH // 2 - 90, 180, 180, 60),
    "Hard": pygame.Rect(WIDTH // 2 - 90, 260, 180, 60)
    }

    for level, rect in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
        label = font.render(level, True, TEXT_COLOR)
        screen.blit(label, label.get_rect(center=rect.center))
    return buttons

def draw_post_game_menu():
    screen.fill(BG_COLOR)
    button_width = 200
    button_height = 50
    gap = 20
    start_y = HEIGHT // 2 - (button_height * 4 + gap * 3) // 2

    labels = ["Restart", "Replay Game", "Change Level", "Exit to Start"]
    buttons = {}

    for i, label in enumerate(labels):
        rect = pygame.Rect(WIDTH // 2 - button_width // 2, start_y + i * (button_height + gap), button_width, button_height)
        pygame.draw.rect(screen, BUTTON_COLOR, rect, border_radius=10)
        text = font.render(label, True, TEXT_COLOR)
        screen.blit(text, text.get_rect(center=rect.center))
        buttons[label] = rect

    return buttons

# ========== MAIN LOOP ==========

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            if game_state == "start_screen":
                if start_btn.collidepoint(pos):
                    game_state = "choose_symbol"

            elif game_state == "choose_symbol":
                for symbol, rect in symbol_buttons.items():
                    if rect.collidepoint(pos):
                        player_symbol = symbol
                        ai_symbol = 'O' if player_symbol == 'X' else 'X'
                        game_state = "choose_turn"

            elif game_state == "choose_turn":
                for label, rect in turn_buttons.items():
                    if rect.collidepoint(pos):
                        player_starts = (label == "First Pick")
                        player_turn = player_starts
                        restart_game()
                        game_state = "choose_level"

            elif game_state == "choose_level":
                for level, rect in level_buttons.items():
                    if rect.collidepoint(pos):
                        difficulty_level = level
                        restart_game()
                        game_state = "playing"

            elif game_state == "playing":
                if game_over and game_end_time:
                    elapsed = pygame.time.get_ticks() - game_end_time
                    if elapsed >= 5000:
                        for label, rect in post_game_buttons.items():
                            if rect.collidepoint(pos):
                                if label == "Restart":
                                    restart_game()
                                elif label == "Replay Game":
                                    restart_game()
                                    game_state = "playing"
                                elif label == "Change Level":
                                    game_state = "choose_level"
                                elif label == "Exit to Start":
                                    game_state = "start_screen"
                                    restart_game()
                        continue

                mouseX, mouseY = pos
                if mouseY < WIDTH and not game_over and player_turn:
                    clicked_row = mouseY // SQUARE_SIZE
                    clicked_col = mouseX // SQUARE_SIZE
                    if board[clicked_row][clicked_col] is None:
                        board[clicked_row][clicked_col] = player_symbol
                        if check_winner(player_symbol):
                            winner_text = "You Win!"
                            game_over = True
                            game_end_time = pygame.time.get_ticks()
                        elif is_board_full():
                            winner_text = "Draw!"
                            game_over = True
                            game_end_time = pygame.time.get_ticks()
                        else:
                            player_turn = False

    # AI move
    if game_state == "playing" and not player_turn and not game_over:
        ai_move()
        if check_winner(ai_symbol):
            winner_text = "You Lose!"
            game_over = True
            game_end_time = pygame.time.get_ticks()
        elif is_board_full():
            winner_text = "Draw!"
            game_over = True
            game_end_time = pygame.time.get_ticks()
        else:
            player_turn = True

    # DRAWING
    screen.fill(BG_COLOR)

    if game_state == "start_screen":
        start_btn = draw_start_screen()

    elif game_state == "choose_symbol":
        symbol_buttons = draw_symbol_selection()

    elif game_state == "choose_turn":
        turn_buttons = draw_turn_selection()

    elif game_state == "choose_level":
        level_buttons = draw_level_selection()

    elif game_state == "playing":
        draw_lines()
        draw_figures()

        if game_over:
            elapsed = pygame.time.get_ticks() - game_end_time
            countdown_seconds = max(0, 5 - elapsed // 1000)

            # Geser teks hasil dan countdown sedikit ke bawah
            draw_text_center(winner_text, HEIGHT // 2 + 135)
            countdown_text = f" {countdown_seconds} detik..."
            draw_text_center(countdown_text, HEIGHT // 2 + 176)


            # Setelah 5 detik muncul menu post game
            if elapsed >= 5000:
                post_game_buttons = draw_post_game_menu()
        else:
            draw_text_center("", HEIGHT // 4)

    pygame.display.update()