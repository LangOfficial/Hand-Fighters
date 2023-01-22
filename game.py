import webbrowser

import pygame
from sys import exit


class Text:
    def __init__(self, text, pos, font, passive_color, active_color=""):
        self.display_surface = pygame.display.get_surface()
        self.pos = pos
        self.text = text
        self.color = passive_color
        self.passive_color = passive_color
        self.active_color = active_color
        self.font = font
        self.text_surf = self.font.render(text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.pos)

    def color_switch(self):
        if self.active_color:
            mouse_pos = pygame.mouse.get_pos()
            if self.text_rect.collidepoint(mouse_pos):
                self.color = self.active_color
            else:
                self.color = self.passive_color

    def draw_and_update(self):
        self.text_surf = self.font.render(self.text, True, self.color)
        self.text_rect = self.text_surf.get_rect(center=self.pos)
        self.color_switch()
        self.display_surface.blit(self.text_surf, self.text_rect)


class StaticImg(pygame.sprite.Sprite):
    def __init__(self, file_path, rotozoom_size, pos: tuple, active_img=False):
        super().__init__()
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, rotozoom_size)
        self.active_img = active_img
        if self.active_img:
            self.active_img = pygame.image.load(active_img).convert_alpha()
            self.active_img = pygame.transform.rotozoom(self.active_img, 0, rotozoom_size)
        self.passive_img = self.image
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)
        self.display_surface = pygame.display.get_surface()

    def hover_animation(self):
        if self.active_img:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.active_img
            else:
                self.image = self.passive_img

    def update(self):
        self.hover_animation()


class Settings:
    def __init__(self):
        self.lives = '3'  # set some default values
        self.hand_speed = '7'
        self.bullet_speed = '6'
        self.bullet_cooldown = '500'
        self.player_1 = "Player 1"
        self.player_2 = "Player 2"
        self.passive_color = WHITE
        self.active_color = LIGHT_GRAY

        # x,y,w,h rects
        self.lives_input_rect = pygame.Rect(WIN_WIDTH // 2 - 200, WIN_HEIGHT // 2 - 100, 150, 40)
        self.hand_speed_input_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2, 150, 40)
        self.bullet_speed_input_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 100, 150, 40)
        self.bullet_cooldown_input_rect = pygame.Rect(WIN_WIDTH // 2 - 80, WIN_HEIGHT // 2 + 200, 150, 40)
        self.player_1_input_rect = pygame.Rect(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50, 300, 30)
        self.player_2_input_rect = pygame.Rect(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 120, 300, 30)

        # lives
        self.lives_color = WHITE
        # hand speed
        self.hand_speed_color = WHITE
        # bullet speed
        self.bullet_speed_color = WHITE
        # bullet cooldown
        self.bullet_cooldown_color = WHITE
        # player_1
        self.player_1_color = WHITE
        # player 2
        self.player_2_color = WHITE

        # flags
        self.lives_pressed = False
        self.hands_speed_pressed = False
        self.bullet_speed_pressed = False
        self.bullet_cooldown_pressed = False
        self.player_1_pressed = False
        self.player_2_pressed = False

        # directions text
        self.direction_question_mark = StaticImg("Assets/directions.png", 0.1, (WIN_WIDTH - 50, 50))
        self.direction_reveal = StaticImg("Assets/directions_reveal.png", 0.8, (WIN_WIDTH - 200, 150))
class RightHand(pygame.sprite.Sprite):
    def __init__(self, hand_speed, pos, bullet_cooldown):
        super().__init__()
        self.image = pygame.image.load("Assets/Right_Hand.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = int(hand_speed)
        self.bullet_cooldown = int(bullet_cooldown)
        self.last_shot_time = 0
        self.ready = True
        self.bullet_group = pygame.sprite.Group()
        self.chair_group = pygame.sprite.Group()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_RALT] and self.ready:
            self.bullet_group.add(Bullets(settings.bullet_speed, 'right', "Assets/R_hand_punch.png", 0.2))
            run.shooting_sound.play()
            self.last_shot_time = pygame.time.get_ticks()
            self.ready = False

    def constraints(self):
        if self.rect.right > WIN_WIDTH:
            self.rect.right = WIN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        if WIN_WIDTH // 2 + 5 > self.rect.left:
            self.rect.left = WIN_WIDTH // 2 + 5

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.bullet_cooldown:
                self.ready = True

    def update(self):
        self.rect.center += self.direction * self.speed
        self.input()
        self.constraints()
        self.recharge()
        self.bullet_group.draw(WIN)
        self.bullet_group.update()


class LeftHand(pygame.sprite.Sprite):  # bullet speed, bullet_cooldown, hand_speed, lives, Player 1:, Player 2:
    def __init__(self, hand_speed, pos, bullet_cooldown):
        super().__init__()
        self.image = pygame.image.load("Assets/Left_Hand.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.2)
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.direction = pygame.math.Vector2()
        self.speed = int(hand_speed)
        self.bullet_cooldown = int(bullet_cooldown)
        self.ready = True
        self.last_shot_time = 0
        self.bullet_group = pygame.sprite.Group()
        self.chair_group = pygame.sprite.Group()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_LALT] and self.ready:
            self.bullet_group.add(Bullets(settings.bullet_speed, 'left', "Assets/L_hand_punch.png", 0.2))
            run.shooting_sound.play()
            self.last_shot_time = pygame.time.get_ticks()
            self.ready = False

    def constraints(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        if WIN_WIDTH // 2 - 5 < self.rect.right:
            self.rect.right = WIN_WIDTH // 2 - 5

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.bullet_cooldown:
                self.ready = True

    def update(self):
        self.rect.center += self.direction * self.speed
        self.input()
        self.constraints()
        self.recharge()
        self.bullet_group.draw(WIN)
        self.bullet_group.update()


class Bullets(pygame.sprite.Sprite):
    def __init__(self, bullet_speed, hand, filepath, rotozoom):
        super().__init__()
        self.bullet_speed = int(bullet_speed)
        self.hand = hand
        self.image = pygame.image.load(filepath)
        self.image = pygame.transform.rotozoom(self.image, 0, rotozoom)
        if self.hand == 'right':
            self.rect = self.image.get_rect(center=run.player_2_surf.rect.center)
        else:
            self.rect = self.image.get_rect(center=run.player_1_surf.rect.center)

    def destroy(self):
        if self.hand == 'right':
            if self.rect.x < -50:
                self.kill()

        else:
            if self.rect.x > WIN_WIDTH + 50:
                self.kill()

    def update(self):
        if self.hand != "right":
            self.rect.x += self.bullet_speed
        else:
            self.rect.x -= self.bullet_speed
        self.destroy()


class Run:
    def __init__(self, settings_obj):
        self.settings_obj = settings_obj
        # menu stuff
        self.title = Text("HAND FIGHTERS", (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 200), title_font, WHITE)
        self.start = Text("START", (WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50), arcade_font, WHITE, DARK_GRAY)
        self.answers = Text("PARAGRAPH", (WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50), arcade_font, WHITE, DARK_GRAY)
        self.name = Text("LANGLEY TIEU", (WIN_WIDTH - 200, WIN_HEIGHT - 50), title_font, WHITE)
        self.l_hand = StaticImg(file_path="Assets/L_hand_punch.png", rotozoom_size=1.2,
                                pos=(WIN_WIDTH // 2 - 250, WIN_HEIGHT // 2))
        self.r_hand = StaticImg(file_path="Assets/R_hand_punch.png", rotozoom_size=1.2,
                                pos=(WIN_WIDTH // 2 + 250, WIN_HEIGHT // 2))
        self.display_surf = pygame.display.get_surface()
        # back arrow
        self.back_arrow_group = pygame.sprite.Group()
        self.back_arrow = StaticImg("Assets/arrow.png", 0.6, (50, 50), "Assets/red_arrow.png")
        self.back_arrow_group.add(self.back_arrow)
        self.lives_display = Text("LIVES:", (WIN_WIDTH // 2 - 320, WIN_HEIGHT // 2 - 80), techno_race_font, WHITE)
        self.hand_speed_display = Text("HAND SPEED:", (WIN_WIDTH // 2 - 280, WIN_HEIGHT // 2 + 20), techno_race_font,
                                       WHITE)
        self.bullet_speed_display = Text("BULLET SPEED:", (WIN_WIDTH // 2 - 280, WIN_HEIGHT // 2 + 120),
                                         techno_race_font, WHITE)
        self.bullet_cooldown_display = Text("BULLET COOLDOWN:", (WIN_WIDTH // 2 - 250, WIN_HEIGHT // 2 + 220),
                                            techno_race_font, WHITE)
        self.player_1_display = Text("PLAYER 1", (WIN_WIDTH // 2 + 200, WIN_HEIGHT // 2 - 100), techno_race_font, WHITE)
        self.player_2_display = Text("PLAYER 2", (WIN_WIDTH // 2 + 200, WIN_HEIGHT // 2 + 70), techno_race_font, WHITE)
        #  hand_speed, pos, bullet_cooldown
        self.player_creating_ready = False
        self.game_ready = False
        self.needs_info = False

        # play option
        self.play_surf = Text("PLAY", (WIN_WIDTH // 2, 50), arcade_font_L, WHITE, ARCADE_GREEN)
        self.play_bg = pygame.image.load("Assets/punch_out_bg.jpeg")
        self.play_bg = pygame.transform.scale(self.play_bg, (WIN_WIDTH, WIN_HEIGHT)).convert_alpha()
        self.player_1_name_display = Text(self.settings_obj.player_1, (WIN_WIDTH // 4, 50), techno_race_font, WHITE)
        self.player_2_name_display = Text(self.settings_obj.player_2, (WIN_WIDTH // 1.2 - 60, 50), techno_race_font,
                                          WHITE)

        # play stage
        self.border = pygame.Rect(WIN_WIDTH // 2, 0, 5, WIN_HEIGHT)
        self.lives_2 = self.settings_obj.lives
        self.lives_game_display_1 = Text(f'Lives: {self.settings_obj.lives}', (WIN_WIDTH // 4, 120), techno_race_font,
                                         WHITE)
        self.lives_game_display_2 = Text(f'Lives: {self.lives_2}', (WIN_WIDTH // 1.2 - 60, 120), techno_race_font,
                                         WHITE)
        self.deactivate_shooting = False

        # groups
        self.player_1_group = pygame.sprite.GroupSingle()
        self.player_2_group = pygame.sprite.GroupSingle()

        # music
        self.collision_sound = pygame.mixer.Sound("Assets/explosion.wav")
        self.shooting_sound = pygame.mixer.Sound("Assets/Punch.wav")
        self.main_menu_song = pygame.mixer.Sound("Assets/MainMenuSong.mp3")
        self.active_game_song = pygame.mixer.Sound("Assets/In_the_Woods.mp3")
        self.victory_sound_effect = pygame.mixer.Sound("Assets/You Win (Street Fighter) - Sound Effect.mp3")
        self.main_menu_song.set_volume(0.2)
        self.shooting_sound.set_volume(0.3)
        self.collision_sound.set_volume(0.2)
        self.active_game_song.set_volume(0.1)
        self.victory_sound_effect.set_volume(0.1)
        self.main_menu_song.play(loops=-1)
        self.activate_game_song = False
        self.victory_sound_effect_done = False

    def settings_update(self):
        # lives setting
        pygame.draw.rect(WIN, settings.lives_color, settings.lives_input_rect)
        lives_text_surf = consolas_font.render(settings.lives, True, BLACK)
        WIN.blit(lives_text_surf, (settings.lives_input_rect.x + 5, settings.lives_input_rect.y + 5))
        settings.lives_input_rect.w = max(40, lives_text_surf.get_width() + 10)

        # bullet speed
        pygame.draw.rect(WIN, settings.bullet_speed_color, settings.bullet_speed_input_rect)
        bullet_speed_text_surf = consolas_font.render(settings.bullet_speed, True, BLACK)
        WIN.blit(bullet_speed_text_surf,
                 (settings.bullet_speed_input_rect.x + 5, settings.bullet_speed_input_rect.y + 5))
        settings.bullet_speed_input_rect.w = max(40, bullet_speed_text_surf.get_width() + 10)

        # bullet cooldown
        pygame.draw.rect(WIN, settings.bullet_cooldown_color, settings.bullet_cooldown_input_rect)
        bullet_cooldown_text_surf = consolas_font.render(settings.bullet_cooldown, True, BLACK)
        WIN.blit(bullet_cooldown_text_surf,
                 (settings.bullet_cooldown_input_rect.x + 5, settings.bullet_cooldown_input_rect.y + 5))
        settings.bullet_cooldown_input_rect.w = max(40, bullet_cooldown_text_surf.get_width() + 10)

        # hand speed
        pygame.draw.rect(WIN, settings.hand_speed_color, settings.hand_speed_input_rect)
        hand_speed_text_surf = consolas_font.render(settings.hand_speed, True, BLACK)
        WIN.blit(hand_speed_text_surf, (settings.hand_speed_input_rect.x + 5, settings.hand_speed_input_rect.y + 5))
        settings.hand_speed_input_rect.w = max(40, hand_speed_text_surf.get_width() + 10)

        # player 1
        pygame.draw.rect(WIN, settings.player_1_color, settings.player_1_input_rect)
        player_1_text_surf = consolas_font.render(settings.player_1, True, BLACK)
        WIN.blit(player_1_text_surf, (settings.player_1_input_rect.x + 5, settings.player_1_input_rect.y + 5))
        settings.player_1_input_rect.w = max(400, player_1_text_surf.get_width() + 10)

        # player 2
        pygame.draw.rect(WIN, settings.player_2_color, settings.player_2_input_rect)
        player_2_text_surf = consolas_font.render(settings.player_2, True, BLACK)
        WIN.blit(player_2_text_surf, (settings.player_2_input_rect.x + 5, settings.player_2_input_rect.y + 5))
        settings.player_2_input_rect.w = max(400, player_2_text_surf.get_width() + 10)

    def bullet_collisions(self):
        if pygame.sprite.groupcollide(self.player_1_group, self.player_2_surf.bullet_group, False, True):
            self.settings_obj.lives -= 1
            self.collision_sound.play()
        if pygame.sprite.groupcollide(self.player_2_group, self.player_1_surf.bullet_group, False, True):
            self.lives_2 -= 1
            self.collision_sound.play()

    def declare_winner(self):
        if int(self.lives_2) <= 0:
            winner_text = StaticImg("Assets/Winner_text.png", 0.3, (WIN_WIDTH // 4, WIN_HEIGHT - 100))
            WIN.blit(winner_text.image, winner_text.rect)
            self.deactivate_shooting = True

        elif int(self.settings_obj.lives) <= 0:
            winner_text = StaticImg("Assets/Winner_text.png", 0.3, (WIN_WIDTH - 200, WIN_HEIGHT - 100))
            WIN.blit(winner_text.image, winner_text.rect)
            self.deactivate_shooting = True

        if not self.victory_sound_effect_done and self.deactivate_shooting:
            self.victory_sound_effect.play()
            self.victory_sound_effect_done = True

    def update(self):
        if stage == 'menu':
            self.start.draw_and_update()
            self.answers.draw_and_update()
            self.name.draw_and_update()
            self.title.draw_and_update()
            WIN.blit(self.l_hand.image, self.l_hand.rect)
            WIN.blit(self.r_hand.image, self.r_hand.rect)
            self.l_hand.update()
            self.r_hand.update()

        elif stage == 'settings':
            self.back_arrow_group.draw(self.display_surf)
            WIN.blit(self.settings_obj.direction_question_mark.image, self.settings_obj.direction_question_mark.rect)
            self.settings_obj.direction_question_mark.update()
            self.back_arrow_group.update()
            self.lives_display.draw_and_update()
            self.hand_speed_display.draw_and_update()
            self.bullet_speed_display.draw_and_update()
            self.bullet_cooldown_display.draw_and_update()
            self.play_surf.draw_and_update()
            self.player_1_display.draw_and_update()
            self.player_2_display.draw_and_update()
            self.settings_update()
            if settings.direction_question_mark.rect.collidepoint(pygame.mouse.get_pos()):
                WIN.blit(settings.direction_reveal.image, settings.direction_reveal.rect)

        elif stage == 'play':
            if self.player_creating_ready:
                self.main_menu_song.stop()
                self.player_1_surf = LeftHand(settings.hand_speed, (WIN_WIDTH // 2 - 300, WIN_HEIGHT // 2),
                                              settings.bullet_cooldown)
                self.player_2_surf = RightHand(settings.hand_speed,
                                               (WIN_WIDTH // 2 + 300, WIN_HEIGHT // 2), settings.bullet_cooldown)
                self.player_1_group.add(self.player_1_surf)
                self.player_2_group.add(self.player_2_surf)
                self.game_ready = True
                self.activate_game_song = True
                self.player_creating_ready = False

            if self.game_ready:
                WIN.blit(self.play_bg, (0, 0))
                self.declare_winner()
                WIN.blit(self.player_1_surf.image, self.player_1_surf.rect)
                WIN.blit(self.player_2_surf.image, self.player_2_surf.rect)
                pygame.draw.rect(WIN, WHITE, self.border)
                self.back_arrow_group.draw(self.display_surf)
                self.back_arrow_group.update()
                self.player_1_name_display = Text(self.settings_obj.player_1, (WIN_WIDTH // 4, 50), techno_race_font,
                                                  WHITE)
                self.player_2_name_display = Text(self.settings_obj.player_2, (WIN_WIDTH // 1.2 - 60, 50),
                                                  techno_race_font,
                                                  WHITE)
                self.lives_game_display_1 = Text(f'Lives: {self.settings_obj.lives}', (WIN_WIDTH // 4, 90),
                                                 techno_race_font, WHITE)
                self.lives_game_display_2 = Text(f'Lives: {self.lives_2}', (WIN_WIDTH // 1.2 - 60, 90),
                                                 techno_race_font, WHITE)
                self.settings_obj.lives = int(self.settings_obj.lives)
                self.lives_2 = int(self.lives_2)
                self.lives_game_display_1.draw_and_update()
                self.lives_game_display_2.draw_and_update()
                self.player_1_surf.update()
                self.player_2_surf.update()
                self.player_1_name_display.draw_and_update()
                self.player_2_name_display.draw_and_update()
                if not self.deactivate_shooting:
                    self.bullet_collisions()
                    self.victory_sound_effect_done = False

            if self.activate_game_song:
                self.active_game_song.play(loops=-1)
                self.activate_game_song = False


pygame.init()
WIN_WIDTH, WIN_HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Hand Fighters")
icon = pygame.image.load(r"C:\Users\jamsb\Downloads\raised-fist-hand-power-pixel-art-line-icon-icon-illustration-vector-removebg-preview.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# colors
BLACK = (0, 0, 0)
DARK_GRAY = (39, 43, 43)
LIGHT_GRAY = (211, 211, 211)
WHITE = (255, 255, 255)
ARCADE_GREEN = "#77ff77"

# font
techno_race_font = pygame.font.Font("Assets/TechnoRace.otf", 35)
title_font = pygame.font.Font("Assets/ka1.ttf", 40)
arcade_font = pygame.font.Font("Assets/ARCADE.TTF", 60)
arcade_font_L = pygame.font.Font("Assets/ARCADE.TTF", 90)

consolas_font = pygame.font.SysFont("Consolas", 30)

settings = Settings()
run = Run(settings)
# text, pos, font, passive_color, active_color=""
stage = "menu"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if stage == "menu":
                if run.start.text_rect.collidepoint(mouse_pos):
                    stage = "settings"
                elif run.answers.text_rect.collidepoint(mouse_pos):
                    webbrowser.open(
                        r"https://docs.google.com/document/d/13xoAHEQOLxXUj5CGge1sZ1gXm4NCq4a95PbGEz6Q_n4/edit?usp=sharing")

            elif stage == "settings" or stage == "play":
                if run.back_arrow.rect.collidepoint(mouse_pos):
                    if stage == "play":
                        settings.lives = '3'
                        settings.hand_speed = '7'
                        settings.bullet_speed = '6'
                        settings.bullet_cooldown = '500'
                        run.deactivate_shooting = False
                        run.active_game_song.stop()
                        run.main_menu_song.play(loops=-1)
                    stage = "menu"

            if stage == "settings":
                if settings.lives_input_rect.collidepoint(mouse_pos):
                    settings.lives_color = settings.active_color
                    settings.lives_pressed = True
                else:
                    settings.lives_color = settings.passive_color
                    settings.lives_pressed = False

                if settings.bullet_speed_input_rect.collidepoint(mouse_pos):
                    settings.bullet_speed_color = settings.active_color
                    settings.bullet_speed_pressed = True

                else:
                    settings.bullet_speed_color = settings.passive_color
                    settings.bullet_speed_pressed = False

                if settings.hand_speed_input_rect.collidepoint(mouse_pos):
                    settings.hand_speed_color = settings.active_color
                    settings.hands_speed_pressed = True
                else:
                    settings.hand_speed_color = settings.passive_color
                    settings.hands_speed_pressed = False

                if settings.bullet_cooldown_input_rect.collidepoint(mouse_pos):
                    settings.bullet_cooldown_color = settings.active_color
                    settings.bullet_cooldown_pressed = True

                else:
                    settings.bullet_cooldown_color = settings.passive_color
                    settings.bullet_cooldown_pressed = False

                if settings.player_1_input_rect.collidepoint(mouse_pos):
                    settings.player_1_color = settings.active_color
                    settings.player_1_pressed = True

                else:
                    settings.player_1_color = settings.passive_color
                    settings.player_1_pressed = False

                if settings.player_2_input_rect.collidepoint(mouse_pos):
                    settings.player_2_color = settings.active_color
                    settings.player_2_pressed = True

                else:
                    settings.player_2_color = settings.passive_color
                    settings.player_2_pressed = False

                if run.play_surf.text_rect.collidepoint(mouse_pos):
                    all_inputs = (settings.lives, settings.bullet_cooldown,
                                  settings.bullet_speed, settings.hand_speed,
                                  settings.player_1, settings.player_2)
                    for info in all_inputs:
                        if not info:
                            run.needs_info = True
                            break
                    else:
                        run.needs_info = False

                    if not run.needs_info:
                        run.player_creating_ready = True
                        run.lives_2 = run.settings_obj.lives
                        stage = "play"

        if event.type == pygame.KEYDOWN:
            if stage == "settings":
                if event.key == pygame.K_BACKSPACE:
                    if settings.lives_pressed:
                        settings.lives = settings.lives[:-1]
                    if settings.hands_speed_pressed:
                        settings.hand_speed = settings.hand_speed[:-1]
                    if settings.bullet_speed_pressed:
                        settings.bullet_speed = settings.bullet_speed[:-1]
                    if settings.bullet_cooldown_pressed:
                        settings.bullet_cooldown = settings.bullet_cooldown[:-1]
                    if settings.player_1_pressed:
                        settings.player_1 = settings.player_1[:-1]
                    if settings.player_2_pressed:
                        settings.player_2 = settings.player_2[:-1]

                else:
                    if settings.lives_pressed:
                        if settings.lives.isdigit() or settings.lives == '':
                            settings.lives += event.unicode

                        if len([x for x in settings.lives if x.isdigit()]) != len(settings.lives):
                            settings.lives = settings.lives[:-1]
                        try:
                            if int(settings.lives) > 20 or int(settings.lives) <= 0:
                                settings.lives = settings.lives[:-1]
                        except:
                            pass
                    # hand speed
                    if settings.hands_speed_pressed:
                        if settings.hand_speed.isdigit() or settings.hand_speed == '':
                            settings.hand_speed += event.unicode

                        if len([x for x in settings.hand_speed if x.isdigit()]) != len(settings.hand_speed):
                            settings.hand_speed = settings.hand_speed[:-1]
                        try:
                            if int(settings.hand_speed) > 10 or int(settings.hand_speed) <= 0:
                                settings.hand_speed = settings.hand_speed[:-1]
                        except:
                            pass

                    # bullet speed
                    if settings.bullet_speed_pressed:
                        if settings.bullet_speed.isdigit() or settings.bullet_speed == '':
                            settings.bullet_speed += event.unicode

                        if len([x for x in settings.bullet_speed if x.isdigit()]) != len(settings.bullet_speed):
                            settings.bullet_speed = settings.bullet_speed[:-1]
                        try:
                            if int(settings.bullet_speed) > 20 or int(settings.bullet_speed) <= 0:
                                settings.bullet_speed = settings.bullet_speed[:-1]
                        except:
                            pass
                    # bullet cooldown
                    if settings.bullet_cooldown_pressed:
                        if settings.bullet_cooldown.isdigit() or settings.bullet_cooldown == '':
                            settings.bullet_cooldown += event.unicode

                        if len([x for x in settings.bullet_cooldown if x.isdigit()]) != len(settings.bullet_cooldown):
                            settings.bullet_cooldown = settings.bullet_cooldown[:-1]
                        try:
                            if int(settings.bullet_cooldown) > 2000 or int(settings.bullet_cooldown) <= 0:
                                settings.bullet_cooldown = settings.bullet_cooldown[:-1]
                        except:
                            pass
                    if settings.player_1_pressed:
                        settings.player_1 += event.unicode
                        if len(settings.player_1) > 23:
                            settings.player_1 = settings.player_1[:-1]
                    if settings.player_2_pressed:
                        settings.player_2 += event.unicode
                        if len(settings.player_2) > 23:
                            settings.player_2 = settings.player_2[:-1]

    WIN.fill(BLACK)
    run.update()
    pygame.display.update()
    clock.tick(60)
