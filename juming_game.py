import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def remove_pipes(pipes):
    for pipe in pipes:
        if pipe.centerx == -600:
            pipes.remove(pipe)
    return pipes


def check_collision(pipes):
    for pipe in pipes:
        if santa_rect.colliderect(pipe):
            bg_sound.stop()
            return False

    if santa_rect.top <= -100 or santa_rect.bottom >= 900:
        bg_sound.stop()
        return False

    return True


def rotate_santa(santa):
    new_santa = pygame.transform.rotozoom(santa, -santa_movement * 3, 1)
    return new_santa


def santa_animation():
    new_santa = santa_frames[santa_index]
    new_santa_rect = new_santa.get_rect(center=(100, santa_rect.centery))
    return new_santa, new_santa_rect


def score_display(game_state):
    if game_state == 'main':
        score_surface = game_font.render(str(int(score)), True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (0, 0, 0))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
pygame.display.set_caption("JUMPING GAME")
clock = pygame.time.Clock()
game_font = pygame.font.Font('font/04B_19.ttf', 40)
programIcon = pygame.image.load('image/santa.png')
pygame.display.set_icon(programIcon)

# Game Variables
gravity = 0.25
santa_movement = 0
game_active = True
score = 0
high_score = 0

bg_surface = pygame.image.load('image/jumping_bg.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('image/floor.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

santa_downflap = pygame.transform.scale2x(pygame.image.load('image/santa.png').convert_alpha())
santa_midflap = pygame.transform.scale2x(pygame.image.load('image/santa.png').convert_alpha())
santa_upflap = pygame.transform.scale2x(pygame.image.load('image/santa.png').convert_alpha())
santa_frames = [santa_downflap, santa_midflap, santa_upflap]
santa_index = 0
santa_surface = santa_frames[santa_index]
santa_rect = santa_surface.get_rect(center=(100, 512))

santaFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(santaFLAP, 200)

pipe_surface = pygame.image.load('image/pipe.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

game_over_surface = pygame.image.load('image/bg_title.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 512))

bg_sound = pygame.mixer.Sound('sound/bgm1.wav')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                santa_movement = 0
                santa_movement -= 7
            if event.key == pygame.K_KP_ENTER and game_active == False:
                bg_sound.play()
                game_active = True
                pipe_list.clear()
                santa_rect.center = (100, 512)
                santa_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == santaFLAP:
            if santa_index < 2:
                santa_index += 1
            else:
                santa_index = 0

            santa_surface, santa_rect = santa_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # santa
        santa_movement += gravity
        rotated_santa = rotate_santa(santa_surface)
        santa_rect.centery += santa_movement
        screen.blit(rotated_santa, santa_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        pipe_list = remove_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.2
        score_display('main')

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 2
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.flip()
    clock.tick(120)