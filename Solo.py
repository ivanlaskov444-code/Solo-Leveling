import arcade

PART = 20
SCREEN_WIDTH = PART * 30
SCREEN_HEIGHT = PART * 30
SCREEN_TITLE = "Storks"


class MyMeny(arcade.Window):
    def __init__(self, width, height, title, part):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.GREEN)
        self.part = part

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled(self.center_x - 100/2, self.center_y - 100/2, 100, 100, arcade.color.WHITE)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.center_x <= x <= self.center_x + self.width and
                    self.center_y <= y <= self.center_y + self.height):
                print(5)


def setup_game(width=400, height=400, title="Storks", part=20):
    game = MyGame(width, height, title, part)
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, PART)
    arcade.run()


if __name__ == "__main__":
    main()