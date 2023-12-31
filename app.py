import pygame, sys, random, button
from pygame.math import Vector2
from pygame import mixer
from os import path


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.running_score = 0

    def load_data(self):
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, "highscore.txt"), "r") as f:
                self.highscore = int(f.read())
        except:
            with open(path.join(self.dir, "highscore.txt"), "w") as f:
                self.highscore = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()
        self.draw_highscore()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if (
            not 0 <= self.snake.body[0].x <= cell_number - 1
            or not 0 <= self.snake.body[0].y <= cell_number - 1
        ):
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        if self.running_score > self.highscore:
            self.highscore = self.running_score
            with open(path.join(self.dir, "highscore.txt"), "w") as f:
                f.write(str(self.running_score))

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 6,
            apple_rect.height,
        )

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

        self.running_score = int(score_text)

    def draw_highscore(self):
        highscore_text = "HIGH SCORE: " + str(self.highscore)
        highscore_surface = game_font.render(highscore_text, True, (0, 0, 0))
        highscore_x = int(cell_size * (cell_number / 2))
        highscore_y = 60
        highscore_rect = highscore_surface.get_rect(center=(highscore_x, highscore_y))
        screen.blit(highscore_surface, highscore_rect)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load(
            "Graphics/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            "Graphics/body_horizontal.png"
        ).convert_alpha()

        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()
        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                if previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (
                        previous_block.x == -1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == -1
                    ):
                        screen.blit(self.body_tl, block_rect)
                    if (
                        previous_block.x == -1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == -1
                    ):
                        screen.blit(self.body_bl, block_rect)
                    if (
                        previous_block.x == 1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == 1
                    ):
                        screen.blit(self.body_tr, block_rect)
                    if (
                        previous_block.x == 1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == 1
                    ):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()
        self.crunch_sound.set_volume(0.2)

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size
        )
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


# initialize pygame and mixer
pygame.init()
mixer.init()

mixer.music.load("Sound/Neon-Metaphor.ogg")
mixer.music.play()
music_volume = 0.1
pygame.mixer.music.set_volume(music_volume)

# create game window
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption("wish.com snake game")

# game variables
main_game = MAIN()
game_paused = False
menu_state = "main"
clicked = False
clock = pygame.time.Clock()
apple = pygame.image.load("Graphics/apple.png").convert_alpha()

# define fonts
game_font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)

# load button images
resume_img = pygame.image.load("Graphics/button_resume.png").convert_alpha()
options_img = pygame.image.load("Graphics/button_options.png").convert_alpha()
quit_img = pygame.image.load("Graphics/button_quit.png").convert_alpha()
video_img = pygame.image.load("Graphics/button_video.png").convert_alpha()
audio_img = pygame.image.load("Graphics/button_audio.png").convert_alpha()
keys_img = pygame.image.load("Graphics/button_keys.png").convert_alpha()
back_img = pygame.image.load("Graphics/button_back.png").convert_alpha()

# create button instances
resume_button = button.Button(304, 225, resume_img, 1)
options_button = button.Button(297, 350, options_img, 1)
quit_button = button.Button(336, 475, quit_img, 1)
video_button = button.Button(226, 175, video_img, 1)
audio_button = button.Button(225, 300, audio_img, 1)
keys_button = button.Button(246, 425, keys_img, 1)
back_button = button.Button(332, 550, back_img, 1)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

# load scores beforehand
main_game.load_data()

# game loop
run = True
while run:
    screen.fill((175, 215, 70))

    # check if paused
    if game_paused == True:
        # check menu state
        if menu_state == "main":
            if resume_button.draw(screen) and clicked == False:
                game_paused = False
                clicked = True
            if options_button.draw(screen) and clicked == False:
                menu_state = "options"
                clicked = True
            if quit_button.draw(screen) and clicked == False:
                run = False
                clicked = True
        if menu_state == "options":
            if video_button.draw(screen) and clicked == False:
                print("Video settings")
                clicked = True
            if audio_button.draw(screen) and clicked == False:
                music_volume -= 0.01
                pygame.mixer.music.set_volume(music_volume)
                clicked = True
            if keys_button.draw(screen) and clicked == False:
                print("Bindings")
                clicked = True
            if back_button.draw(screen) and clicked == False:
                menu_state = "main"
                clicked = True
    else:
        main_game.draw_elements()

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_paused = True
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)

    pygame.display.update()
    clock.tick(60)
