import pygame
from sys import exit
import math
from random import randint, choice


pygame.init()


class Waldo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        waldo_walk = pygame.image.load('graphics/Waldo/waldo_walk.webp').convert_alpha()
        waldo_walk = pygame.transform.rotozoom(waldo_walk, 0, 0.1)
        self.image = waldo_walk
        self.rect = self.image.get_rect(center = (200, 100))
        self.attack_speed = 1

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += 5

    def update(self):
        self.player_input()

class Hit_Effect(pygame.sprite.Sprite):
    def __init__(self, type, frames, pos):
        super().__init__()
        if type == 'slash':
            slash_images = [pygame.image.load('graphics/Effects/slash_1.png').convert_alpha(),
                            pygame.image.load('graphics/Effects/slash_2.png').convert_alpha(),
                            pygame.image.load('graphics/Effects/slash_1.png').convert_alpha()]
            slash_img = slash_images[slash_index]

            # find angle between click and player position to rotate the slash png
            player_pos = (player.sprite.rect.center)
            click_x, click_y = pos
            player_x, player_y = player_pos
            self.radians = math.atan2(click_x - player_x, player_y - click_y)
            self.angle = math.degrees(self.radians)

            # must multiply angle value by -1 because the rotozoom function rotates counterclockwise
            slash_img = pygame.transform.rotozoom(slash_img, self.angle * -1, 0.1 * (slash_index + 1))
            image = slash_img
            self.image = image

            # now that we have the angle between the click and the player, we can transpose the slash 100 units away from the player in that direction
            # to get distance transposed in the x axis, multiply 100 by sin(angle). for y, cos(angle)
            transposed_pos = (player_x + 100 * math.sin(self.radians), player_y - 100 * math.cos(self.radians))
            self.rect = self.image.get_rect(center = transposed_pos)

            # add end lag frames to each slash
            if slash_index == 0: end_lag_timers['slash'] = 20
            elif slash_index == 1: end_lag_timers['slash'] = 25
            elif slash_index == 2: end_lag_timers['slash'] = 35

        self.frames_left = frames

    def destroy(self):
        if self.frames_left <= 0:
            self.kill()

    def update(self):
        player_pos = (player.sprite.rect.center)
        player_x, player_y = player_pos
        transposed_pos = (player_x + 100 * math.sin(self.radians), player_y - 100 * math.cos(self.radians))
        self.rect = self.image.get_rect(center = transposed_pos)
        # if self.frames_left == 30:
        #     print('angle', self.angle)
        #     print('math.cos(self.angle)', math.cos(self.angle))
        #     print('math.sin(self.angle)', math.sin(self.angle))
        self.frames_left -= 1
        if end_lag_timers['slash'] > 0:
            end_lag_timers['slash'] -= 1
        self.destroy()


def Main(screen, clock):
    bubble_font = pygame.font.Font('font/BabyPlums-6Y0AD.ttf', 50)
    game_active = False

    # Groups
    global player
    player = pygame.sprite.GroupSingle()
    player.add(Waldo())

    hit_effect_group = pygame.sprite.Group()
    slash_pos = (0, 0)

    # Effects
    global end_lag_timers
    end_lag_timers = {'slash': 0}
    global slash_index
    slash_index = 0

    # Intro Screen
    waldo_wave = pygame.image.load('graphics/Waldo/waldo_wave.png').convert_alpha()
    waldo_wave = pygame.transform.rotozoom(waldo_wave, 0, 0.5)
    waldo_wave_rect = waldo_wave.get_rect(center = (640, 360))

    title_font = pygame.font.Font('font/BabyPlums-6Y0AD.ttf', 100)
    title_surf = title_font.render("Waldo's Gate", False, 'Red')
    title_rect = title_surf.get_rect(center = (640, 180))

    start_surf = bubble_font.render('Press any key to start.', False, 'Red')
    start_rect = start_surf.get_rect(center = (640, 540))

    # Filler
    in_game_font = pygame.font.Font('font/FortuneBrother-jE5wy.ttf', 50)
    in_prog_labels = ["Waldo's Gate is a work in progress.", "Use W, A, S, D or up, down, left, right arrow keys to move.", 'Press spacebar to return to the title screen.']
    in_prog_surfs = [in_game_font.render(string, False, 'White') for string in in_prog_labels]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if game_active:
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_SPACE]:
                        game_active = False
                    # print('slash_index', slash_index)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        # time_since_last['lmb'] = 0
                        slash_pos = event.pos
                        # print('slash', player.sprite.rect)
                        # print('x', player.sprite.rect.x)
                        # print('y', player.sprite.rect.y)
                        if not end_lag_timers['slash'] or end_lag_timers['slash'] <= 10:
                            # create a slash effect lasting different # of frames depending on slash_index
                            if slash_index == 0:
                                hit_effect_group.add(Hit_Effect('slash', 30, slash_pos))
                            elif slash_index == 1:
                                hit_effect_group.add(Hit_Effect('slash', 35, slash_pos))
                            else:
                                hit_effect_group.add(Hit_Effect('slash', 40, slash_pos))
                            # increment slash_index after each new slash and reset it to 0 at the end of the combo
                            if slash_index < 2: slash_index += 1
                            else: slash_index = 0
                        # print('slash_index', slash_index)

            else:
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    game_active = True

        if game_active:
            screen.fill((55, 55, 55))
            in_prog_y = 540
            for surf in in_prog_surfs:
                screen.blit(surf, surf.get_rect(center = (640, in_prog_y)))
                in_prog_y += 60

            player.draw(screen)
            player.update()

            hit_effect_group.draw(screen)
            hit_effect_group.update()

            # for key, value in time_since_last.items():
            #     value += 1
            # if time_since_last['lmb'] >= 300:
            #     slash_index = 0

        else:
            screen.fill('Black')
            screen.blit(waldo_wave, waldo_wave_rect)
            screen.blit(title_surf, title_rect)
            screen.blit(start_surf, start_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ in "__main__":
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Waldo's Gate")
    clock = pygame.time.Clock()
    Main(screen, clock)
