import pygame
import random

pygame.init()

# Screen
screen_width, screen_height = 600, 512
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird Settings Edition")

# Load assets
background = pygame.image.load("assets/background-day.png").convert()
ground = pygame.image.load("assets/base.png").convert_alpha()
bird_img = pygame.image.load("assets/yellowbird-midflap.png").convert_alpha()
pipe_img = pygame.image.load("assets/pipe-green.png").convert_alpha()
pipe_top_img = pygame.transform.flip(pipe_img, False, True)

# Resize
bird_img = pygame.transform.scale(bird_img, (34, 24))
pipe_img = pygame.transform.scale(pipe_img, (52, 320))
pipe_top_img = pygame.transform.flip(pipe_img, False, True)
ground_y = screen_height - ground.get_height()

# Sounds
point_sound = pygame.mixer.Sound("sounds/point.wav")
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
pygame.mixer.music.load("sounds/background.mp3")

# Font
font = pygame.font.Font('freesansbold.ttf', 24)

# High score functions
def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_highscore(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

highscore = load_highscore()

# Settings
settings = {
    "pipe_mode": "dynamic",
    "sound": True,
    "music": True
}

# Game State
state = "menu"
clock = pygame.time.Clock()
score = 0

# Buttons
def draw_button(text, x, y, w, h, selected=False):
    color = (200, 0, 0) if selected else (0, 100, 200)
    pygame.draw.rect(screen, color, (x, y, w, h))
    txt = font.render(text, True, (255, 255, 255))
    screen.blit(txt, (x + w // 2 - txt.get_width() // 2, y + h // 2 - txt.get_height() // 2))

def draw_menu():
    screen.fill((0, 150, 255))
    draw_button("Play", 220, 180, 160, 50)
    draw_button("Settings", 220, 260, 160, 50)

    high_txt = font.render(f"High Score: {highscore}", True, (255, 255, 255))
    screen.blit(high_txt, (screen_width - high_txt.get_width() - 10, 10))


def draw_settings():
    screen.fill((50, 50, 50))
    draw_button(f"Pipes: {settings['pipe_mode'].capitalize()}", 180, 120, 240, 50)
    draw_button(f"Sound: {'On' if settings['sound'] else 'Off'}", 180, 190, 240, 50)
    draw_button(f"Music: {'On' if settings['music'] else 'Off'}", 180, 260, 240, 50)
    draw_button("Back", 180, 330, 240, 50)

# Pipe creation
def create_pipe_group():
    gap = random.randint(120, 180)
    spacing = random.randint(180, 300)
    height = random.randint(80, screen_height - gap - 120)

    top_only = random.random() < 0.2
    bottom_only = random.random() < 0.2
    both = not (top_only or bottom_only)

    pipe_group = {"top": None, "bottom": None, "scored": False}

    x_pos = screen_width + spacing

    if top_only or both:
        top = pygame.Rect(x_pos, height - pipe_img.get_height(), 52, 320)
        pipe_group["top"] = top
    if bottom_only or both:
        bottom = pygame.Rect(x_pos, height + gap, 52, 320)
        pipe_group["bottom"] = bottom

    return pipe_group


def create_pipe_pair():
    height = random.randint(100, 300)
    gap = 150
    top = {"rect": pygame.Rect(screen_width, height - pipe_img.get_height(), 52, 320), "scored": False, "type": "top"}
    bottom = {"rect": pygame.Rect(screen_width, height + gap, 52, 320), "scored": False, "type": "bottom"}
    return [top, bottom]

# Gameplay
def run_game():
    global state, score
    score = 0
    pipes = []
    pipe_timer = 0
    bird_x, bird_y = 50, 200
    bird_velocity = 0
    gravity = 0.5
    jump_strength = -7

    if settings["music"]:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    running = True
    while running:
        for x in range(0, screen_width, background.get_width()):
            screen.blit(background, (x, 0))
        for x in range(0, screen_width, ground.get_width()):
            screen.blit(ground, (x, ground_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = jump_strength

        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect = pygame.Rect(bird_x, bird_y, 34, 24)

        # Pipe generation
        pipe_timer += 1
        if pipe_timer > 100:
            if settings["pipe_mode"] == "consistent":
                # Consistent
                gap = 150
                height = random.randint(100, 300)
                pipe_group = {
                    "top": pygame.Rect(screen_width, height - pipe_img.get_height(), 52, 320),
                    "bottom": pygame.Rect(screen_width, height + gap, 52, 320),
                    "scored": False
                }
            else:
                # Dynamic
                pipe_group = create_pipe_group()

            pipes.append(pipe_group)
            pipe_timer = 0


        for group in pipes:
            if group["top"]:
                group["top"].x -= 2
            if group["bottom"]:
                group["bottom"].x -= 2

    # Collision check
            if (group["top"] and group["top"].colliderect(bird_rect)) or (group["bottom"] and group["bottom"].colliderect(bird_rect)):
                if settings["sound"]:
                    hit_sound.play() 
                running = False

        for group in pipes:
            ref_pipe = group["bottom"] or group["top"]
            pipe_center = ref_pipe.x + ref_pipe.width // 2
            bird_center = bird_x + 34 // 2

            if not group["scored"] and pipe_center < bird_center:
                group["scored"] = True
                score += 1
                if settings["sound"]:
                    point_sound.play()




        pipes = [g for g in pipes if (g["top"] and g["top"].x > -52) or (g["bottom"] and g["bottom"].x > -52)]

        for group in pipes:
            if group["top"]:
                screen.blit(pipe_top_img, (group["top"].x, group["top"].y))
            if group["bottom"]:
                screen.blit(pipe_img, (group["bottom"].x, group["bottom"].y))

        screen.blit(bird_img, (bird_x, bird_y))
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        if bird_y > ground_y - 24 or bird_y < 0:
            if settings["sound"]:
                hit_sound.play()
            running = False

        pygame.display.update()
        clock.tick(60)

    # Update highscore
    global highscore
    if score > highscore:
        highscore = score
    save_highscore(score)

    pygame.mixer.music.stop() 

    state = "menu"

# Main loop
while True:
    if state == "menu":
        draw_menu()
    elif state == "settings":
        draw_settings()
    elif state == "playing":
        run_game()
        continue  # skip rest of loop after game ends

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if state == "menu":
                if 220 <= x <= 380 and 180 <= y <= 230:
                    state = "playing"
                elif 220 <= x <= 380 and 260 <= y <= 310:
                    state = "settings"
            elif state == "settings":
                if 180 <= x <= 420 and 120 <= y <= 170:
                    settings["pipe_mode"] = "consistent" if settings["pipe_mode"] == "dynamic" else "dynamic"
                elif 180 <= x <= 420 and 190 <= y <= 240:
                    settings["sound"] = not settings["sound"]
                elif 180 <= x <= 420 and 260 <= y <= 310:
                    settings["music"] = not settings["music"]
                elif 180 <= x <= 420 and 330 <= y <= 380:
                    state = "menu"

    pygame.display.update()
    clock.tick(60)
