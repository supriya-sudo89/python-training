import arcade
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "SPACE SHOOTER (FIXED)"

PLAYER_SPEED = 6
BULLET_SPEED = 8
ENEMY_SPEED = 3
MAX_HEALTH = 3


class SpaceShooter(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = None
        self.score = 0
        self.health = MAX_HEALTH
        self.game_over = False

    def setup(self):

        arcade.set_background_color(arcade.color.BLACK)

        self.player = arcade.SpriteSolidColor(50, 20, arcade.color.CYAN)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = 60
        self.player_list.append(self.player)

        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        for _ in range(6):
            enemy = arcade.SpriteSolidColor(40, 40, arcade.color.RED)
            enemy.center_x = random.randint(50, SCREEN_WIDTH - 50)
            enemy.center_y = random.randint(300, 550)
            self.enemy_list.append(enemy)

    def on_draw(self):
        self.clear()

        self.player_list.draw()
        self.enemy_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(f"Score: {self.score}", 10, 30, arcade.color.WHITE, 20)
        arcade.draw_text(f"Health: {self.health}", 10, 10, arcade.color.WHITE, 20)

        if self.game_over:
            arcade.draw_text(
                "GAME OVER\nPress R to Restart",
                320,
                300,
                arcade.color.RED,
                30
            )

    def on_update(self, delta_time):

        if self.game_over:
            return

        self.bullet_list.update()

        for bullet in self.bullet_list:
            if bullet.top > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

        for enemy in self.enemy_list:
            enemy.center_y -= ENEMY_SPEED

            if enemy.bottom < 0:
                enemy.center_y = random.randint(300, 550)
                enemy.center_x = random.randint(50, SCREEN_WIDTH - 50)
                self.health -= 1

                if self.health <= 0:
                    self.game_over = True

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)

            if hit_list:
                bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.center_y = random.randint(300, 550)
                enemy.center_x = random.randint(50, SCREEN_WIDTH - 50)
                self.score += 1

    def on_key_press(self, key, modifiers):

        # Restart game
        if self.game_over and key == arcade.key.R:
            self.setup()
            return

        if self.game_over:
            return

        if key == arcade.key.LEFT:
            self.player.center_x -= PLAYER_SPEED

        elif key == arcade.key.RIGHT:
            self.player.center_x += PLAYER_SPEED

        elif key == arcade.key.SPACE:
            bullet = arcade.SpriteSolidColor(5, 15, arcade.color.YELLOW)
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.top
            bullet.change_y = BULLET_SPEED
            self.bullet_list.append(bullet)


if __name__ == "__main__":
    game = SpaceShooter()
    game.setup()
    arcade.run()