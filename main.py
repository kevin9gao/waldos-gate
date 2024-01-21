import pygame
from sys import exit
import math
from random import randint, choice


class Waldo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        waldo_walk = pygame.image.load('graphics/Waldo/waldo_walk.webp').convert_alpha()
        waldo_walk = pygame.transform.rotozoom(waldo_walk, 0, 0.1)
        self.image = waldo_walk
        self.rect = self.image.get_rect(center = (200, 100))

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



pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Waldo's Gate")
clock = pygame.time.Clock()
bubble_font = pygame.font.Font('font/BabyPlums-6Y0AD.ttf', 50)
game_active = False

# Groups
player = pygame.sprite.GroupSingle()
player.add(Waldo())

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

    else:
        screen.fill('Black')
        screen.blit(waldo_wave, waldo_wave_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)

    pygame.display.update()
    clock.tick(60)
