import pygame
from reflexy.helpers import (
    get_image_path,
    calc_acceleration,
)
from reflexy.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    COOLDOWN_PLAYER_SWORD,
    TIME_PLAYER_BLINK,
    PLAYER_ACCELERATION,
    PLAYER_ACCELERATION_FUNC,
    PLAYER_DECELERATION,
    PLAYER_DECELERATION_FUNC,
)


class Player(pygame.sprite.Sprite):
    def __init__(self, time):
        pygame.sprite.Sprite.__init__(self)

        self.time = time

        self.images = [
            self.get_surface(filename)
            for filename in (
                [
                    "player-w-sword-00.png",
                    "player-w-sword-01.png",
                    "player-w-sword-02.png",
                    "player-w-sword-03.png",
                    "player-w-sword-04.png",
                    "player-w-sword-05.png",
                    "player-w-sword-06.png",
                    "player-w-sword-07.png",
                ]
            )
        ]
        self.current_image = 0
        self.image = self.images[self.current_image]

        self.set_spawn()

        self.mouse = pygame.mouse.get_pos()
        self.hp = 3
        self.score = 0

        self.cd_attack = 0

        self.dead = False
        self.blinking_damage = False
        self.count_blinking = 0
        self.attacking = False

        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False

        self.horizontal_acc = None
        self.vertical_acc = None

        self.speed = 0
        self.current_speed = None
        self.acc_tracker = None
        self.state_of_moviment = "accelerating"
        self.last_state_of_moviment = None

    def update(self, time):
        self.time = time
        self.image = self.images[self.current_image]
        self.set_velocity()
        self.move_player()

        self.center = (
            self.rect[0] + PLAYER_WIDTH / 2,
            self.rect[1] + PLAYER_HEIGHT / 2,
        )

        if self.attacking:
            self.attack()

    def set_spawn(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.center = (self.x - PLAYER_WIDTH / 2, self.y - PLAYER_HEIGHT / 2)
        self.rect = pygame.Rect(self.x, self.y, PLAYER_WIDTH, PLAYER_HEIGHT)

    def blink_damage(self):
        if self.count_blinking == 0:
            self.count_blinking = self.time

        if self.time - self.count_blinking > TIME_PLAYER_BLINK:
            self.blinking_damage = not self.blinking_damage
            self.count_blinking = self.time

            if self.blinking_damage:
                self.image = self.get_surface("player-w-sword-damage.png")

    def attack(self):
        if self.attacking or self.time - self.cd_attack > COOLDOWN_PLAYER_SWORD:
            self.attacking = True
            self.current_image += 1

            if self.current_image > len(self.images) - 1:
                self.current_image = 0
                self.attacking = False
                self.cd_attack = self.time

            self.image = self.images[self.current_image]

    def keydown(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.move_right = False
            self.move_left = True
            self.horizontal_acc = "left"
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.move_left = False
            self.move_right = True
            self.horizontal_acc = "right"

        if key == pygame.K_UP or key == pygame.K_w:
            self.move_down = False
            self.move_up = True
            self.vertical_acc = "up"
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.move_up = False
            self.move_down = True
            self.vertical_acc = "down"

        if (
            True
            in [
                self.move_left,
                self.move_right,
                self.move_up,
                self.move_down,
            ]
            and self.state_of_moviment in ["stoped", "decelerating"]
        ):
            self.state_of_moviment = "accelerating"

    def keyup(self, key):
        if key == pygame.K_LEFT or key == pygame.K_a:
            self.move_left = False
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            self.move_right = False

        if key == pygame.K_UP or key == pygame.K_w:
            self.move_up = False
        elif key == pygame.K_DOWN or key == pygame.K_s:
            self.move_down = False

        if not True in [
            self.move_left,
            self.move_right,
            self.move_up,
            self.move_down,
        ]:
            self.state_of_moviment = "decelerating"

    def set_velocity(self):
        if not (self.move_up or self.move_down) and (self.move_left or self.move_right):
            self.vertical_acc = None

        if not (self.move_left or self.move_right) and (self.move_up or self.move_down):
            self.horizontal_acc = None

        if self.state_of_moviment == "accelerating" and self.speed < PLAYER_SPEED:
            if not self.acc_tracker or self.last_state_of_moviment == "decelerating":
                self.acc_tracker = self.time

            if not self.speed:
                self.current_speed = PLAYER_SPEED

            elif self.speed != PLAYER_SPEED and self.current_speed == None:
                self.current_speed = self.speed

            elif self.current_speed == None:
                self.current_speed = PLAYER_SPEED

            self.speed = (
                calc_acceleration(
                    PLAYER_ACCELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    PLAYER_ACCELERATION,
                )
                * self.current_speed
            )

            self.last_state_of_moviment = "accelerating"

        if self.speed > PLAYER_SPEED or self.state_of_moviment == "keep":
            self.speed = PLAYER_SPEED
            self.state_of_moviment = "keep"
            self.acc_tracker = None
            self.current_speed = None
            self.last_state_of_moviment = "keep"

        elif self.state_of_moviment == "decelerating":
            if not self.acc_tracker or self.last_state_of_moviment == "accelerating":
                self.acc_tracker = self.time

            if self.speed != PLAYER_SPEED and self.current_speed == None:
                self.current_speed = self.speed
            elif self.current_speed == None:
                self.current_speed = PLAYER_SPEED

            self.speed = (
                1
                - calc_acceleration(
                    PLAYER_DECELERATION_FUNC,
                    self.time,
                    self.acc_tracker,
                    PLAYER_DECELERATION,
                )
            ) * self.current_speed

            self.last_state_of_moviment = "decelerating"

        if self.speed < 0 and self.state_of_moviment == "decelerating":
            self.state_of_moviment = "stoped"
            self.speed = 0
            self.acc_tracker = None
            self.current_speed = None
            self.horizontal_acc = None
            self.vertical_acc = None
            self.last_state_of_moviment = "stoped"

    def move_player(self):
        if self.rect.bottom < SCREEN_HEIGHT and (
            self.move_down
            or (
                self.state_of_moviment == "decelerating" and self.vertical_acc == "down"
            )
        ):
            self.rect.top += self.speed

        if self.rect.top > -18 and (
            self.move_up
            or (self.state_of_moviment == "decelerating" and self.vertical_acc == "up")
        ):
            self.rect.top -= self.speed

        if self.rect.left > -30 and (
            self.move_left
            or (
                self.state_of_moviment == "decelerating"
                and self.horizontal_acc == "left"
            )
        ):
            self.rect.left -= self.speed

        if self.rect.right < SCREEN_WIDTH and (
            self.move_right
            or (
                self.state_of_moviment == "decelerating"
                and self.horizontal_acc == "right"
            )
        ):
            self.rect.right += self.speed

    def get_surface(self, filename, angle=0, scale=1.2):
        return pygame.transform.rotozoom(
            pygame.image.load(get_image_path(filename)).convert_alpha(),
            angle,
            scale,
        )
