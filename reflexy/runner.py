import pygame
import os
import sys
import time
from typing import List, Tuple, Dict
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAPTION,
    GAME_SPEED,
    CLOCK_TICK_GAME_SPEED,
    CLOCK_TICK_REFERENCE,
    FONT_SIZE,
    SPIDER_VISION,
    SPAWN_SPIDER,
    PLAYER_SPEED,
    COOLDOWN_PLAYER_IMMUNE,
)
from reflexy.helpers import get_image_path, create_pygame_font
from reflexy.models.player import Player
from reflexy.models.laser_spider import LaserSpider
from reflexy.main import start


class Runner:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(CAPTION)

        self.clock = pygame.time.Clock()
        self.background = self.create_background()

        self.time = time.time()
        self.last_time = self.time
        self.time_game()

        self.text = create_pygame_font(FONT_SIZE, bold=True)

        self.allow_restart = True

        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.laser_draw_group = pygame.sprite.Group()
        self.laser_hit_group = pygame.sprite.Group()
        self.effect_group = pygame.sprite.Group()

        self.player = Player(self.time)
        self.enemy_group.add(LaserSpider(self.time))
        self.player_group.add(self.player)
        self.player_hit = False
        self.cd_player_hit = 0
        self.cd_spawn_spider = self.time

    @staticmethod
    def create_background():
        bg = pygame.image.load(get_image_path("background-field.png"))
        return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def time_game(self):
        self.time = (
            self.time
            + (time.time() - self.last_time)
            * CLOCK_TICK_GAME_SPEED
            / CLOCK_TICK_REFERENCE
        )
        self.last_time = time.time()

    def create_text(self, text):
        return self.text.render(text, True, (255, 255, 255))

    def has_collision(self):
        if self.player.attacking:
            [
                self.kill_spider(sprite)
                for sprite in self.enemy_group.sprites()
                if pygame.sprite.spritecollide(
                    sprite,
                    self.player_group,
                    False,
                    pygame.sprite.collide_mask,
                )
            ]

            return False

        [
            self.kill_spider(sprite)
            for sprite in self.enemy_group.sprites()
            if pygame.sprite.spritecollide(
                sprite,
                self.laser_hit_group,
                False,
                pygame.sprite.collide_mask,
            )
            and not sprite.ray
        ]

        return pygame.sprite.groupcollide(
            self.player_group,
            self.enemy_group,
            False,
            False,
            pygame.sprite.collide_mask,
        )

    def has_hit(self):
        for enemy in self.enemy_group.sprites():
            if enemy.ray:
                if enemy.ray not in self.enemy_group.sprites():
                    self.laser_draw_group.add(enemy.ray)

                if enemy.ray not in self.enemy_group.sprites() and (
                    int(enemy.ray.current_image) >= 5
                ):
                    self.laser_hit_group.add(enemy.ray)

        hit = pygame.sprite.groupcollide(
            self.laser_hit_group,
            self.player_group,
            False,
            False,
            pygame.sprite.collide_mask,
        )
        return hit

    def hp(self):
        if self.enemy_group.sprites():
            if (self.has_collision() or self.has_hit()) and not self.player_hit:
                self.player.hp -= 1
                self.player_hit = True
                self.cd_player_hit = self.time
                self.player.set_spawn()
                self.player.dead = True

            if self.player.dead:
                self.player.blink_damage()

            if (
                self.player_hit
                and self.time - self.cd_player_hit > COOLDOWN_PLAYER_IMMUNE
            ):
                self.player.dead = False
                self.player.blinking_damage = False
                self.player_hit = False
                self.player.blinking_damage = 0

    def respawn_spider(self):
        self.enemy_group.add(LaserSpider(self.time))

    def kill_spider(self, sprite):
        if sprite.ray:
            sprite.ray.kill()
            sprite.ray

        sprite.kill()
        self.player.score += 1

    def check_events(self):
        if self.time - self.cd_spawn_spider > SPAWN_SPIDER:
            self.respawn_spider()
            self.cd_spawn_spider = self.time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                self.player.keydown(event.key)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_SPACE:
                    self.player.attack()

                self.player.keyup(event.key)

    def update_score(self):
        self.screen.blit(
            self.create_text("Lifes = " + str(self.player.hp)),
            (FONT_SIZE, SCREEN_HEIGHT / 8),
        )
        self.screen.blit(
            self.create_text(str(self.player.score)),
            ((SCREEN_WIDTH - (FONT_SIZE / 2)) / 2, SCREEN_HEIGHT / 8),
        )

    def update_frame(self):
        self.screen.blit(self.background, (0, 0))
        self.time_game()

        for group in [self.enemy_group, self.player_group, self.laser_draw_group]:
            group.draw(self.screen)

        self.enemy_group.update(self.screen, self.player.center, self.time)
        self.player_group.update(self.time)

        self.update_score()
        pygame.display.update()

    def restart(self):
        if not self.allow_restart:
            pygame.quit()
            sys.exit()

        restart_game = False

        self.screen.fill((0, 0, 0))
        text = self.create_text(
            f"You Died! Press R to restart\nScore: {self.player.score}"
        )
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        while not restart_game:
            self.clock.tick(CLOCK_TICK_GAME_SPEED)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(text, textRect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game = True
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

        start()

    def run(self):
        while self.player.hp > 0:
            self.clock.tick(CLOCK_TICK_GAME_SPEED)
            self.check_events()
            self.update_frame()
            self.hp()

        self.restart()
