import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Solo Leveling"

SPEED = 10
MONSTER_SPEED = 2
RADIUS = 300

TILE_SCALING = 1.0
CAMERA_LERP = 0.12

player_damage = 3

# Функция рисования HP-баров
def draw_hp_bar(sprite, width=40, height=6):
    hp_ratio = max(sprite.hp / sprite.max_hp, 0)  # чтобы не было отрицательного HP

    bar_x = sprite.center_x
    bar_y = sprite.top + 10

    arcade.draw_rect_filled(
        arcade.rect.XYWH(bar_x, bar_y, width, height),
        arcade.color.DARK_RED
    )

    arcade.draw_rect_filled(
        arcade.rect.XYWH(bar_x - (width * (1 - hp_ratio)) / 2, bar_y, width * hp_ratio, height),
        arcade.color.GREEN
    )

# Класс Игрока
class Player(arcade.AnimatedWalkingSprite):
    def __init__(self, x, y):
        super().__init__(scale=2.0)

        base = "player_run/"
        base_attack = "player_run_attack/"

        # вниз
        self.stand_down_textures = [
            arcade.load_texture(base + "player_stands_down.png")
        ]
        self.walk_down_textures = [
            arcade.load_texture(base + "player_left_down.png"),
            arcade.load_texture(base + "player_right_down.png"),
        ]

        # вверх
        self.stand_up_textures = [
            arcade.load_texture(base + "player_stands_up.png")
        ]
        self.walk_up_textures = [
            arcade.load_texture(base + "player_left_up.png"),
            arcade.load_texture(base + "player_right_up.png"),
        ]

        # влево
        self.stand_left_textures = [
            arcade.load_texture(base + "player_stands_left.png")
        ]
        self.walk_left_textures = [
            arcade.load_texture(base + "player_left_left.png"),
            arcade.load_texture(base + "player_right_left.png"),
        ]

        # вправо
        self.stand_right_textures = [
            arcade.load_texture(base + "player_stands_right.png")
        ]
        self.walk_right_textures = [
            arcade.load_texture(base + "player_left_right.png"),
            arcade.load_texture(base + "player_right_right.png"),
        ]

        # атака вниз
        self.attack_down_textures = [
            arcade.load_texture(base_attack + "player_down_1.png"),
            arcade.load_texture(base_attack + "player_down_2.png"),
            arcade.load_texture(base_attack + "player_down_3.png"),
            arcade.load_texture(base_attack + "player_down_4.png"),
        ]

        # атака вверх
        self.attack_up_textures = [
            arcade.load_texture(base_attack + "player_up_1.png"),
            arcade.load_texture(base_attack + "player_up_2.png"),
            arcade.load_texture(base_attack + "player_up_3.png"),
            arcade.load_texture(base_attack + "player_up_4.png"),
        ]

        # атака влево
        self.attack_left_textures = [
            arcade.load_texture(base_attack + "player_left_1.png"),
            arcade.load_texture(base_attack + "player_left_2.png"),
            arcade.load_texture(base_attack + "player_left_3.png"),
            arcade.load_texture(base_attack + "player_left_4.png"),
        ]

        # атака вправо
        self.attack_right_textures = [
            arcade.load_texture(base_attack + "player_right_1.png"),
            arcade.load_texture(base_attack + "player_right_2.png"),
            arcade.load_texture(base_attack + "player_right_3.png"),
            arcade.load_texture(base_attack + "player_right_4.png"),
        ]


        self.center_x = x
        self.center_y = y
        self.max_hp = 100
        self.hp = 100

        self.is_attacking = False
        self.attack_cooldown = 0.0 # Перезарядка
        self.attack_timer = 0.0 # нужен чтобы кадры атаки не менялись мгновенно
        self.attack_frame = 0 # Текущий кадр анимации атаки
        self.attack_speed = 0.09 # скорость этой анимации когда он атакует

        self.facing_direction = arcade.FACE_DOWN # Текущее направление взгляда игрока


    def attack(self):
        if self.attack_timer > 0 or self.is_attacking:
            return

        self.is_attacking = True
        self.attack_timer = self.attack_cooldown
        self.attack_frame = 0

    def update_animation(self, delta_time: float = 1 / 60):

        # таймер перезарядки
        if self.attack_timer > 0:
            self.attack_timer -= delta_time

        # если атака
        if self.is_attacking:
            self.attack_frame += delta_time

            frame = int(self.attack_frame / self.attack_speed)

            if self.facing_direction == arcade.FACE_UP:
                textures = self.attack_up_textures
            elif self.facing_direction == arcade.FACE_DOWN:
                textures = self.attack_down_textures
            elif self.facing_direction == arcade.FACE_LEFT:
                textures = self.attack_left_textures
            else:
                textures = self.attack_right_textures

            if frame >= len(textures):
                self.is_attacking = False
                self.attack_frame = 0
                return

            self.texture = textures[frame]
            return

        # если не атакует то включаем обычную ходьбу
        super().update_animation(delta_time)



class Goblin(arcade.AnimatedWalkingSprite):
    def __init__(self, x, y):
        super().__init__(scale=2.0)

        base = "goblin_run/"

        # вниз
        self.stand_down_textures = [
            arcade.load_texture(base + "goblin_stands_down.png")
        ]
        self.walk_down_textures = [
            arcade.load_texture(base + "goblin_left_down.png"),
            arcade.load_texture(base + "goblin_right_down.png"),
        ]

        # вверх
        self.stand_up_textures = [
            arcade.load_texture(base + "goblin_stands_up.png")
        ]
        self.walk_up_textures = [
            arcade.load_texture(base + "goblin_left_up.png"),
            arcade.load_texture(base + "goblin_right_up.png"),
        ]

        # влево
        self.stand_left_textures = [
            arcade.load_texture(base + "goblin_stands_left.png")
        ]
        self.walk_left_textures = [
            arcade.load_texture(base + "goblin_left_left.png"),
            arcade.load_texture(base + "goblin_right_left.png"),
        ]

        # вправо
        self.stand_right_textures = [
            arcade.load_texture(base + "goblin_stands_right.png")
        ]
        self.walk_right_textures = [
            arcade.load_texture(base + "goblin_left_right.png"),
            arcade.load_texture(base + "goblin_right_right.png"),
        ]

        self.center_x = x
        self.center_y = y

        self.max_hp = 80
        self.hp = 80
        self.damage = 0.5
        self.speed = MONSTER_SPEED
        self.aggro_radius = RADIUS

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled(self.center_x - 100, self.center_y - 50, 200, 100, arcade.color.WHITE)
        arcade.draw_text("START GAME", self.center_x, self.center_y, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center"
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.center_x - 50 <= x <= self.center_x -50 + self.width and
                    self.center_y - 50 <= y <= self.center_y - 50 + self.height):
                player = Player(700, 1470)
                city = City(player, spawn_x=700, spawn_y=1470)
                city.setup()
                self.window.show_view(city)

# Класс города
class City(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

    def setup(self):
        self.tile_map = arcade.load_tilemap("map_city.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        # Порталы в подземелье
        self.portal_list = self.tile_map.sprite_lists["dungeon"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))
        walls.extend(self.scene.get_sprite_list("house border"))

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw()
        draw_hp_bar(self.player)  # хп игрока

    def on_update(self, dt):
        self.physics_engine.update()
        if self.player.change_x > 0:
            self.player.facing_direction = arcade.FACE_RIGHT
        elif self.player.change_x < 0:
            self.player.facing_direction = arcade.FACE_LEFT
        elif self.player.change_y > 0:
            self.player.facing_direction = arcade.FACE_UP
        elif self.player.change_y < 0:
            self.player.facing_direction = arcade.FACE_DOWN
        self.player.update_animation(dt)

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player.center_x, self.player.center_y),
            CAMERA_LERP
        )

        # переход в подземелье
        if arcade.check_for_collision_with_list(self.player, self.portal_list):
            dungeon = Dungeon1(self.player, spawn_x=590, spawn_y=500)
            dungeon.setup()
            self.window.show_view(dungeon)



    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.player.change_y = SPEED
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.player.change_y = -SPEED
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.player.change_x = -SPEED
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.player.change_x = SPEED
        elif key == arcade.key.ENTER:
            self.player.attack()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0



#Подземелье со слизнями
class Dungeon(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

    def setup(self):
        self.tile_map = arcade.load_tilemap("map_dungeon.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        self.portal_list1 = self.tile_map.sprite_lists["portal"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))

        # Монстры слизь
        self.mobs_list = arcade.SpriteList()
        for obj in self.tile_map.object_lists.get("mobs1", []):
            monster = arcade.Sprite(":resources:images/enemies/slimeBlue.png", 0.5)
            monster.center_x = obj.shape[0]
            monster.center_y = obj.shape[1]

            monster.max_hp = 50
            monster.hp = 50

            self.mobs_list.append(monster)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

    def on_draw(self):
        self.clear()
        self.world_camera.use()

        self.scene.draw()
        self.mobs_list.draw()

        # хп монстров
        for monster in self.mobs_list:
            draw_hp_bar(monster)

        # хп игрока
        draw_hp_bar(self.player)

        self.gui_camera.use()

    def on_update(self, dt):
        self.physics_engine.update()
        if self.player.change_x > 0:
            self.player.facing_direction = arcade.FACE_RIGHT
        elif self.player.change_x < 0:
            self.player.facing_direction = arcade.FACE_LEFT
        elif self.player.change_y > 0:
            self.player.facing_direction = arcade.FACE_UP
        elif self.player.change_y < 0:
            self.player.facing_direction = arcade.FACE_DOWN
        self.player.update_animation(dt)

        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player.center_x, self.player.center_y),
            CAMERA_LERP
        )

        # возврат в город
        if arcade.check_for_collision_with_list(self.player, self.portal_list1):
            city = City(self.player, spawn_x=1200, spawn_y=2000)
            city.setup()
            self.window.show_view(city)
            return

        # логика монстров
        for monster in self.mobs_list:
            distance = arcade.get_distance_between_sprites(monster, self.player)

            if distance > RADIUS:
                monster.change_x = 0
                monster.change_y = 0
                continue

            # Простое преследование игрока
            monster.change_x = MONSTER_SPEED if self.player.center_x > monster.center_x else -MONSTER_SPEED
            monster.change_y = MONSTER_SPEED if self.player.center_y > monster.center_y else -MONSTER_SPEED

        self.mobs_list.update()

        # проверка столкновений и нанесение урона игроку
        for monster in self.mobs_list:
            if arcade.check_for_collision(self.player, monster):
                self.player.hp -= 0.3  # монстр наносит урон игроку
                if self.player.hp <= 0:
                    print("умер") # экран смерти сделаь

            # удаление убитых монстров
            if monster.hp <= 0:
                monster.kill()

        # урон слизню
        if self.player.is_attacking:
            for monster in self.mobs_list:
                if arcade.get_distance_between_sprites(self.player, monster) < 60:
                    monster.hp -= player_damage

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.player.change_y = SPEED
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.player.change_y = -SPEED
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.player.change_x = -SPEED
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.player.change_x = SPEED
        elif key == arcade.key.ENTER:
            self.player.attack()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0

# подземелье гоблинами
class Dungeon1(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)

        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()

    def setup(self):
        self.tile_map = arcade.load_tilemap("map_dungeon.tmx", scaling=TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        self.portal_list = self.tile_map.sprite_lists["portal"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

        # гоблины
        self.mobs_list = arcade.SpriteList()

        for obj in self.tile_map.object_lists.get("mobs1", []):
            goblin = Goblin(obj.shape[0], obj.shape[1])
            self.mobs_list.append(goblin)

    def on_draw(self):
        self.clear()
        self.world_camera.use()

        self.scene.draw()
        self.mobs_list.draw()

        for goblin in self.mobs_list:
            draw_hp_bar(goblin)

        draw_hp_bar(self.player)

    def on_update(self, dt):
        self.physics_engine.update()
        if self.player.change_x > 0:
            self.player.facing_direction = arcade.FACE_RIGHT
        elif self.player.change_x < 0:
            self.player.facing_direction = arcade.FACE_LEFT
        elif self.player.change_y > 0:
            self.player.facing_direction = arcade.FACE_UP
        elif self.player.change_y < 0:
            self.player.facing_direction = arcade.FACE_DOWN
        self.player.update_animation(dt)

        self.world_camera.position = (
            self.player.center_x,
            self.player.center_y
        )

        # возврат в город
        if arcade.check_for_collision_with_list(self.player, self.portal_list):
            city = City(self.player, spawn_x=1200, spawn_y=2000)
            city.setup()
            self.window.show_view(city)
            return

        for goblin in self.mobs_list:
            distance = arcade.get_distance_between_sprites(goblin, self.player)

            if distance <= RADIUS:
                dx = self.player.center_x - goblin.center_x
                dy = self.player.center_y - goblin.center_y

                if abs(dx) > abs(dy):
                    goblin.change_x = goblin.speed if dx > 0 else -goblin.speed
                    goblin.change_y = 0
                else:
                    goblin.change_y = goblin.speed if dy > 0 else -goblin.speed
                    goblin.change_x = 0
            else:
                goblin.change_x = 0
                goblin.change_y = 0

            # урон игроку
            if arcade.check_for_collision(goblin, self.player):
                self.player.hp -= goblin.damage
                self.player.hp = max(self.player.hp, 0)

            # урон гоблину
            if self.player.is_attacking:
                for monster in self.mobs_list:
                    if arcade.get_distance_between_sprites(self.player, monster) < 60:
                        monster.hp -= player_damage

        self.mobs_list.update()
        self.mobs_list.update_animation(dt)

        for goblin in self.mobs_list:
            if goblin.hp <= 0:
                goblin.kill()

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.UP):
            self.player.change_y = SPEED
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.player.change_y = -SPEED
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.player.change_x = -SPEED
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.player.change_x = SPEED
        elif key == arcade.key.ENTER:
            self.player.attack()

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.player.change_x = 0


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    menu = MainMenu()
    window.show_view(menu)

    arcade.run()


if __name__ == "__main__":
    main()
