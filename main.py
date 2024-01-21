import pygame
from sys import exit
import math
from random import randint, choice

# # class Waldo(pygame.sprite.Sprite()):
#     def __init__(self):
#         super().__init__()


pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Waldo's Gate")
clock = pygame.time.Clock()
bubble_font = pygame.font.Font('font/BabyPlums-6Y0AD.ttf', 50)
game_active = False

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
bubble_font_xs = pygame.font.Font('font/BabyPlums-6Y0AD.ttf', 35)
in_prog_labels = ["Waldo's Gate is a work in progress.", 'Press spacebar to return to the title screen.']
in_prog_surfs = [bubble_font_xs.render(string, False, 'White') for string in in_prog_labels]

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
        in_prog_y = 330
        for surf in in_prog_surfs:
            screen.blit(surf, surf.get_rect(center = (640, in_prog_y)))
            in_prog_y += 60

    else:
        screen.fill('Black')
        screen.blit(waldo_wave, waldo_wave_rect)
        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)

    pygame.display.update()
    clock.tick(60)
