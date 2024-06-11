import pygame
import random

# 画面サイズの設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)

# Pygameの初期化
pygame.init()

# 画面の設定
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("麻雀ゲーム")

# フォントの設定
font = pygame.font.Font(None, 36)

# 画像のロード
try:
    player_icon = pygame.image.load('images/player_icon.png')
except FileNotFoundError:
    player_icon = None

try:
    cpu_icon = pygame.image.load('images/cpu_icon.png')
except FileNotFoundError:
    cpu_icon = None

try:
    bonus_image = pygame.image.load('images/bonus.png')
except FileNotFoundError:
    bonus_image = None

# 音楽ファイルのロード
try:
    victory_sound = pygame.mixer.Sound('sounds/victory_sound.wav')
except FileNotFoundError:
    victory_sound = None

# 牌の生成
def generate_tiles():
    tiles = []
    suits = ['萬', '筒', '索']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    honors = ['東', '南', '西', '北', '白', '發', '中']

    for suit in suits:
        for number in numbers:
            for _ in range(4):
                tiles.append(number + suit)
    
    for honor in honors:
        for _ in range(4):
            tiles.append(honor)
    
    random.shuffle(tiles)
    return tiles

# 牌の配列を初期化
tiles = generate_tiles()

# プレイヤーとCPUの手牌を初期化
player_hand = tiles[:13]
cpu_hand = tiles[13:26]
deck = tiles[26:]  # 山札
player_discard = []
cpu_discard = []

# ゲーム状態
current_turn = "player"
selected_tile = None
winner = None

# スタート画面
def show_start_screen():
    screen.fill(GREEN)
    title_text = font.render("麻雀ゲーム", True, WHITE)
    start_button = font.render("スタート", True, WHITE)
    quit_button = font.render("終了", True, WHITE)
    screen.blit(title_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 100))
    screen.blit(start_button, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    screen.blit(quit_button, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50))
    pygame.display.flip()

    start_rect = start_button.get_rect(topleft=(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))
    quit_rect = quit_button.get_rect(topleft=(WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 + 50))

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    waiting = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# 勝敗判定関数
def is_winning_hand(hand):
    # 仮のロジック、実際には複雑な役の判定を実装する必要がある
    return False

def check_for_win():
    global winner
    if current_turn == "player" and is_winning_hand(player_hand):
        winner = "Player"
        if victory_sound:
            pygame.mixer.Sound.play(victory_sound)
    elif current_turn == "cpu" and is_winning_hand(cpu_hand):
        winner = "CPU"

# CPUの捨て牌ロジック
def cpu_discard_tile():
    return random.choice(cpu_hand)

# UIの更新
def update_ui():
    screen.fill(GREEN)

    # アイコンの表示
    if player_icon:
        screen.blit(player_icon, (700, 500))
    else:
        pygame.draw.rect(screen, WHITE, (700, 500, 50, 50))
        icon_text = font.render("P", True, BLACK)
        screen.blit(icon_text, (715, 515))
    
    if cpu_icon:
        screen.blit(cpu_icon, (700, 50))
    else:
        pygame.draw.rect(screen, WHITE, (700, 50, 50, 50))
        icon_text = font.render("C", True, BLACK)
        screen.blit(icon_text, (715, 65))

    for i, tile in enumerate(player_hand):
        tile_text = font.render(tile, True, WHITE)
        screen.blit(tile_text, (50 + i * 40, 500))

    for i, tile in enumerate(cpu_hand[:3]):  # CPUの手牌の一部のみ表示
        tile_text = font.render("?", True, WHITE)
        screen.blit(tile_text, (50 + i * 40, 50))

    for i, tile in enumerate(player_discard):
        tile_text = font.render(tile, True, WHITE)
        screen.blit(tile_text, (50 + i * 40, 400))

    for i, tile in enumerate(cpu_discard):
        tile_text = font.render(tile, True, WHITE)
        screen.blit(tile_text, (50 + i * 40, 150))

    if winner:
        if winner == "Player" and bonus_image:
            screen.blit(bonus_image, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 100))
        elif winner == "Player":
            bonus_text = font.render("Bonus!", True, WHITE)
            screen.blit(bonus_text, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2 - 50))
        winner_text = font.render(f"{winner} 勝利！", True, WHITE)
        screen.blit(winner_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2))

    pygame.display.flip()

# ターン終了処理
def end_turn():
    global current_turn
    current_turn = "cpu" if current_turn == "player" else "player"

# ゲームループ
def game_loop():
    global selected_tile, winner
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and current_turn == "player" and not winner:
                x, y = event.pos
                if 500 <= y <= 550:
                    for i in range(len(player_hand)):
                        if 50 + i * 40 <= x <= 90 + i * 40:
                            selected_tile = i
                            break
                if selected_tile is not None:
                    player_discard.append(player_hand.pop(selected_tile))
                    if deck:
                        player_hand.append(deck.pop(0))
                    check_for_win()
                    if not winner:
                        end_turn()
                    selected_tile = None
        
        if current_turn == "cpu" and not winner:
            discard_tile = cpu_discard_tile()
            cpu_discard.append(discard_tile)
            cpu_hand.remove(discard_tile)
            if deck:
                cpu_hand.append(deck.pop(0))
            check_for_win()
            if not winner:
                end_turn()

        update_ui()

    pygame.quit()

# スタート画面の表示
show_start_screen()

# ゲームの開始
game_loop()
