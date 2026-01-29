import arcade
import random
import time
from database import Database
from pyglet.graphics import Batch
import constants as const

monster_sword_strike = arcade.load_sound(const.SOUND_MONSTER_SWORD)
air_sword_strike = arcade.load_sound(const.SOUND_AIR_SWORD)


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


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(3, 7)
        self.life = random.uniform(0.7, 1.2)
        self.max_life = self.life
        self.radius = random.randint(2, 5)
        self.color = color

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.4
        self.vx *= 0.98
        self.life -= dt
        return self.life > 0

    def draw(self):
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (self.color[0], self.color[1], self.color[2], alpha)
        arcade.draw_circle_filled(self.x, self.y, self.radius, color_with_alpha)

class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Solo Leveling", self.center_x, self.center_y + 75, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center")

        arcade.draw_lbwh_rectangle_filled(self.center_x - 100, self.center_y - 50, 200, 50, arcade.color.WHITE)
        arcade.draw_text("Регистрация", self.center_x, self.center_y - 25, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center")

        arcade.draw_lbwh_rectangle_filled(self.center_x - 100, self.center_y - 150, 200, 50, arcade.color.WHITE)
        arcade.draw_text("Вход", self.center_x, self.center_y - 120, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.center_x - 100 <= x <= self.center_x + 100 and
                    self.center_y - 50 <= y <= self.center_y):
                self.window.show_view(RegisterView())

            elif (self.center_x - 100 <= x <= self.center_x + 100 and
                  self.center_y - 150 <= y <= self.center_y - 100):
                self.window.show_view(LoginView())


class RegisterView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.login_text = ""
        self.password_text = ""
        self.error = False
        self.active_field = "login"
        self.player = None
        self.back_button = arcade.LRBT(10, 100, 565, 595)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Регистрация", 400, 500, arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Логин:", 250, 420, arcade.color.WHITE)
        arcade.draw_text(self.login_text, 350, 420, arcade.color.YELLOW)

        arcade.draw_text("Пароль:", 250, 380, arcade.color.WHITE)
        arcade.draw_text(self.password_text, 350, 380, arcade.color.YELLOW)

        arcade.draw_text("Назад", 10, 580, arcade.color.WHITE)

        if self.error:
            arcade.draw_text("Логин уже занят", 250, 200, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            self.active_field = "password" if self.active_field == "login" else "login"

        elif key == arcade.key.BACKSPACE:
            if self.active_field == "login":
                self.login_text = self.login_text[:-1]
            else:
                self.password_text = self.password_text[:-1]

        elif key == arcade.key.ENTER:
            success = self.db.register_player(self.login_text, self.password_text)
            if success:
                self.player = Player(700, 1470)
                self.player.login = self.login_text
                self.player.credits = 100
                self.player.level = 1

                player_data = self.db.login(self.login_text, self.password_text)
                if player_data:
                    self.player.credits = player_data[2]
                    self.player.level = player_data[3]

                start_window = StartWindow(self.player, self.db)
                self.window.show_view(start_window)
            else:
                self.error = True

        else:
            char = chr(key)
            if char.isalnum():
                if self.active_field == "login":
                    self.login_text += char
                else:
                    self.password_text += char

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Проверяем, попал ли клик в область текста
            if (self.back_button.left <= x <= self.back_button.right and
                self.back_button.bottom <= y <= self.back_button.top):
                main_menu = MainMenu()
                self.window.show_view(main_menu)



class LoginView(arcade.View):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.login_text = ""
        self.password_text = ""
        self.error = False
        self.active_field = "login"
        self.player = None
        self.back_button = arcade.LRBT(10, 100, 565, 595)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Вход", 400, 500, arcade.color.WHITE, 30, anchor_x="center")

        arcade.draw_text("Логин:", 250, 420, arcade.color.WHITE)
        arcade.draw_text(self.login_text, 350, 420, arcade.color.YELLOW)

        arcade.draw_text("Пароль:", 250, 380, arcade.color.WHITE)
        arcade.draw_text(self.password_text, 350, 380, arcade.color.YELLOW)

        arcade.draw_text("Назад", 10, 580, arcade.color.WHITE)

        if self.error:
            arcade.draw_text("Неправильный логин или пароль", 250, 200, arcade.color.WHITE)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.TAB:
            self.active_field = "password" if self.active_field == "login" else "login"

        elif key == arcade.key.BACKSPACE:
            if self.active_field == "login":
                self.login_text = self.login_text[:-1]
            else:
                self.password_text = self.password_text[:-1]

        elif key == arcade.key.ENTER:
            player_data = self.db.login(self.login_text, self.password_text)
            if player_data:
                self.player = Player(700, 1470)
                self.player.login = self.login_text
                self.player.credits = player_data[2]
                self.player.level = player_data[3]

                start_window = StartWindow(self.player, self.db)
                self.window.show_view(start_window)
            else:
                self.error = True

        else:
            char = chr(key)
            if char.isalnum():
                if self.active_field == "login":
                    self.login_text += char
                else:
                    self.password_text += char

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.back_button.left <= x <= self.back_button.right and
                self.back_button.bottom <= y <= self.back_button.top):
                main_menu = MainMenu()
                self.window.show_view(main_menu)


class StartWindow(arcade.View):
    def __init__(self, player=None, db=None):
        super().__init__()
        self.player = player
        self.db = db
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled(self.center_x - 100, self.center_y + 50, 200, 50, arcade.color.WHITE)
        arcade.draw_text("START GAME", self.center_x, self.center_y + 75, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center")

        arcade.draw_lbwh_rectangle_filled(self.center_x - 120, self.center_y - 40, 240, 50, arcade.color.WHITE)
        arcade.draw_text("Сменить аккаунт", self.center_x, self.center_y - 10, arcade.color.BLACK, font_size=24,
                         anchor_x="center", anchor_y="center")

        if self.player and self.player.login:
            arcade.draw_text(f"Игрок: {self.player.login}", 50, 550, arcade.color.WHITE, 16)
            arcade.draw_text(f"Кредиты: {self.player.credits}", 50, 520, arcade.color.WHITE, 16)
            arcade.draw_text(f"Уровень: {self.player.level}", 50, 490, arcade.color.WHITE, 16)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.center_x - 100 <= x <= self.center_x + 100 and
                    self.center_y + 50 <= y <= self.center_y + 100):

                city = City(self.player, spawn_x=700, spawn_y=1470)
                city.setup()
                self.window.show_view(city)


            elif button == arcade.MOUSE_BUTTON_LEFT:
                if (self.center_x - 120 <= x <= self.center_x + 120 and
                        self.center_y - 40 <= y <= self.center_y + 10):
                    main_menu = MainMenu()
                    self.window.show_view(main_menu)



class Player(arcade.AnimatedWalkingSprite):
    def __init__(self, x, y):
        super().__init__(scale=2.0)
        self.db = Database()
        self.login = ""
        self.credits = 0
        self.level = 1


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
        self.max_hp = const.PLAYER_MAX_HP
        self.hp = const.PLAYER_HP
        self.damage = const.PLAYER_DAMAGE
        self.speed = const.PLAYER_SPEED

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

        air_sword_strike.play()
        self.hit_registered = False


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

        # если не атакует то обычную ходьбу
        super().update_animation(delta_time)

    def on_key_press(self, key):
        if key in (arcade.key.W, arcade.key.UP):
            self.change_y = const.PLAYER_SPEED
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.change_y = -const.PLAYER_SPEED
        elif key in (arcade.key.A, arcade.key.LEFT):
            self.change_x = -const.PLAYER_SPEED
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.change_x = const.PLAYER_SPEED
        elif key == arcade.key.ENTER:
            self.attack()

    def on_key_release(self, key):
        if key in (arcade.key.W, arcade.key.S, arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
        elif key in (arcade.key.A, arcade.key.D, arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0



class Goblin(arcade.AnimatedWalkingSprite):
    def __init__(self, x, y):
        super().__init__(scale=2.0)
        self.db = Database()


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
        self.blood_particles = []
        self.blood_color = arcade.color.RED

        self.center_x = x
        self.center_y = y

        self.damage = const.GOBLIN_DAMAGE
        self.hp = const.GOBLIN_HP
        self.max_hp = const.GOBLIN_MAX_HP
        self.speed = const.GOBLIN_SPEED
        self.aggro_radius = const.RADIUS
        self.attack_radius = const.GOBLIN_ATTACK_RADIUS

    def goblin_logic(self, player, dt):
        distance = arcade.get_distance_between_sprites(self, player)

        if distance <= self.aggro_radius:
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y

            if abs(dx) > abs(dy):
                self.change_x = self.speed if dx > 0 else -self.speed
                self.change_y = 0
            else:
                self.change_y = self.speed if dy > 0 else -self.speed
                self.change_x = 0
        else:
            self.change_x = 0
            self.change_y = 0

        # урон игроку
        if arcade.check_for_collision(self, player) and distance < self.attack_radius:
            player.hp -= self.damage
        # урон гоблину
        if player.is_attacking and distance < 60:
            self.hp -= player.damage
            if not player.hit_registered:
                monster_sword_strike.play()
                player.hit_registered = True
                # делаем кровь
                for _ in range(8):
                    particle = Particle(self.center_x, self.center_y, self.blood_color)
                    self.blood_particles.append(particle)

            # обновляем частицы
        self.blood_particles = [p for p in self.blood_particles if p.update(dt)]
        if self.hp <= 0:
            self.kill()
            self.db.add_credits_goblin(player.login)

    def draw_blood(self):
        for particle in self.blood_particles:
            particle.draw()


class Mucus(arcade.AnimatedWalkingSprite):
    def __init__(self, x, y):
        super().__init__(scale=0.5)
        self.db = Database()
        self.blood_particles = []
        self.mucus_color = (0, 150, 255)
        self.texture = arcade.load_texture(":resources:images/enemies/slimeBlue.png")

        self.center_x = x
        self.center_y = y

        self.max_hp = const.MUCUS_MAX_HP
        self.hp = const.MUCUS_HP
        self.speed = const.MUCUS_SPEED
        self.damage = const.MUCUS_DAMAGE
        self.aggro_radius = const.AGGRO_RADIUS_MUCUS
        self.attack_radius = const.MUCUS_ATTACK_RADIUS

    def mucus_logic(self, player, dt):
        distance = arcade.get_distance_between_sprites(self, player)

        if distance <= self.aggro_radius:
            dx = player.center_x - self.center_x
            dy = player.center_y - self.center_y

            if abs(dx) > abs(dy):
                self.change_x = self.speed if dx > 0 else -self.speed
                self.change_y = 0
            else:
                self.change_y = self.speed if dy > 0 else -self.speed
                self.change_x = 0
        else:
            self.change_x = 0
            self.change_y = 0

        # урон игроку
        if arcade.check_for_collision(player, self) and distance < self.attack_radius:
            player.hp -= self.damage


        # урон слизню
        if player.is_attacking and distance < 60:
            self.hp -= player.damage
            if not player.hit_registered:
                monster_sword_strike.play()
                player.hit_registered = True
                # делаем кровь
                for _ in range(5):
                    particle = Particle(self.center_x, self.center_y,self.mucus_color)
                    self.blood_particles.append(particle)

            # обновляем частицы
        self.blood_particles = [p for p in self.blood_particles if p.update(dt)]

        if self.hp <= 0:
            self.kill()
            self.db.add_credits_mucus(player.login)

    def draw_blood(self):
        for particle in self.blood_particles:
            particle.draw()


# Класс города
class City(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.db = Database()
        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()

        self.gui_camera = arcade.camera.Camera2D()

    def setup(self):
        self.tile_map = arcade.load_tilemap("map_city.tmx", scaling=const.TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        # Порталы
        self.portal_list = self.tile_map.sprite_lists["dungeon"]
        self.portal_list2 = self.tile_map.sprite_lists["dungeon2"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))
        walls.extend(self.scene.get_sprite_list("house border"))

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.scene.draw()
        draw_hp_bar(self.player)  # хп игрока
        self.gui_camera.use()
        arcade.draw_lbwh_rectangle_filled(0, 570, 60, 80, arcade.color.WHITE)
        arcade.draw_text("Выход", 0, 580, arcade.color.BLACK, font_size=15)



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
            const.CAMERA_LERP
        )

        # переход в подземелье
        if arcade.check_for_collision_with_list(self.player, self.portal_list):
            dungeon = Dungeon(self.player, spawn_x=590, spawn_y=500)
            dungeon.setup()
            self.window.show_view(dungeon)

        elif arcade.check_for_collision_with_list(self.player, self.portal_list2):
            dungeon1 = Dungeon1(self.player, spawn_x=590, spawn_y=500)
            dungeon1.setup()
            self.window.show_view(dungeon1)

    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            button_left = 0
            button_right = 60
            button_bottom = 570
            button_top = 650

            if (button_left <= x <= button_right and button_bottom <= y <= button_top):
                start_window = StartWindow(self.player, self.db)
                self.window.show_view(start_window)

#Подземелье со слизнями
class Dungeon(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.db = Database()
        self.total_kills = 0

        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.killing = 0

        # Батч для текста
        self.batch = Batch()
        self.killing_info = arcade.Text(
            f"killing: {self.killing}",
            10, 580, arcade.color.RED, 14, batch=self.batch
        )


    def setup(self):
        self.tile_map = arcade.load_tilemap("map_dungeon.tmx", scaling=const.TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        self.portal_list1 = self.tile_map.sprite_lists["portal"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

        # слизь
        self.mucus_list = arcade.SpriteList()

        for obj in self.tile_map.object_lists.get("mobs1", []):
            mucus = Mucus(obj.shape[0], obj.shape[1])
            self.mucus_list.append(mucus)

        #self.restores_health = arcade.SpriteList()

        #for obj in self.tile_map.object_lists.get("health", []):
            #goblin = Goblin(obj.shape[0], obj.shape[1])
            #self.restores_health.append(goblin)

    def on_draw(self):
        self.clear()
        self.world_camera.use()

        self.scene.draw()
        self.mucus_list.draw()
        #self.restores_health.draw()

        # хп слизня
        for mucus in self.mucus_list:
            draw_hp_bar(mucus)
            mucus.draw_blood()

        # хп игрока
        draw_hp_bar(self.player)

        self.gui_camera.use()
        self.batch.draw()


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
        if arcade.check_for_collision_with_list(self.player, self.portal_list1):
            city = City(self.player, spawn_x=1200, spawn_y=2000)
            city.setup()
            self.window.show_view(city)
            return

        mucus_count_before = len(self.mucus_list)

        # логика слизней
        for mucus in self.mucus_list:
            mucus.mucus_logic(self.player, dt)

        self.mucus_list.update()

        mucus_count_after = len(self.mucus_list)
        if mucus_count_after < mucus_count_before:
            kills = mucus_count_before - mucus_count_after
            self.killing += kills
            self.total_kills += 1
            self.killing_info.text = f"killing: {self.killing}"
            if self.total_kills == 25:
                self.db.up_level(self.player.login)
                victory_screen = VictoryScreen(self.player.login, self.db, self, total_kills=self.killing)
                self.window.show_view(victory_screen)




        if self.player.hp <= 0:
            if "Player" in self.scene:
                self.scene.remove_sprite_list_by_name("Player")
            self.physics_engine = None
            death_screen = DeathScreen(self.player.login, self.db, self,  total_kills=self.killing)
            self.window.show_view(death_screen)



    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)

# подземелье гоблинами
class Dungeon1(arcade.View):
    def __init__(self, player, spawn_x, spawn_y):
        super().__init__()
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.total_kills = 0

        self.db = Database()

        self.player = player
        self.player.center_x = spawn_x
        self.player.center_y = spawn_y

        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.killing = 0
        self.batch = Batch()
        self.killing_info = arcade.Text(
            f"killing: {self.killing}",
            10, 580, arcade.color.RED, 14, batch=self.batch
        )

    def setup(self):
        self.tile_map = arcade.load_tilemap("map_dungeon2.tmx", scaling=const.TILE_SCALING)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("Player", self.player)

        self.portal_list = self.tile_map.sprite_lists["portal"]

        walls = arcade.SpriteList()
        walls.extend(self.scene.get_sprite_list("border"))
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls)

        # гоблины
        self.goblin_list = arcade.SpriteList()

        for obj in self.tile_map.object_lists.get("mobs1", []):
            goblin = Goblin(obj.shape[0], obj.shape[1])
            self.goblin_list.append(goblin)

    def on_draw(self):
        self.clear()
        self.world_camera.use()

        self.scene.draw()
        self.goblin_list.draw()

        for goblin in self.goblin_list:
            draw_hp_bar(goblin)
            goblin.draw_blood()

        draw_hp_bar(self.player)

        self.gui_camera.use()
        self.batch.draw()

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
            city = City(self.player, spawn_x=1600, spawn_y=2000)
            city.setup()
            self.window.show_view(city)
            return

        goblin_count_before = len(self.goblin_list)

        for goblin in self.goblin_list:
            goblin.goblin_logic(self.player, dt)

        self.goblin_list.update()
        self.goblin_list.update_animation(dt)

        goblin_count_after = len(self.goblin_list)
        if goblin_count_after < goblin_count_before:
            kills = goblin_count_before - goblin_count_after
            self.killing += kills
            self.total_kills += 1
            self.killing_info.text = f"killing: {self.killing}"
            if self.total_kills == 25:
                self.db.up_level(self.player.login)
                victory_screen = VictoryScreen(self.player.login, self.db, self, total_kills=self.killing)
                self.window.show_view(victory_screen)

        if self.player.hp <= 0:
            if "Player" in self.scene:
                self.scene.remove_sprite_list_by_name("Player")
            self.physics_engine = None
            death_screen = DeathScreen(self.player.login, self.db, self, total_kills=self.killing)
            self.window.show_view(death_screen)


    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key)


class DeathScreen(arcade.View):
    def __init__(self, player_login, db, parent_view,  total_kills=0):
        super().__init__()
        self.player_login = player_login
        self.db = db
        self.total_kills = total_kills
        self.parent_view = parent_view
        self.start_time = time.time()

    def on_draw(self):
        self.parent_view.on_draw()

        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 160)
        )


        arcade.draw_text("ВЫ УМЕРЛИ",
                         self.center_x, self.center_y + 150,
                         arcade.color.RED, 50,
                         bold=True, anchor_x="center", anchor_y="center", )

        if self.player_login:
            arcade.draw_text(f"Игрок: {self.player_login}",
                             self.center_x, self.center_y + 50,
                             arcade.color.WHITE, 30,
                             bold=True, anchor_x="center", anchor_y="center")

            arcade.draw_text(f"Убито врагов: {self.total_kills}",
                             self.center_x, self.center_y,
                             arcade.color.WHITE, 28,
                             bold=True, anchor_x="center", anchor_y="center")

        arcade.draw_text("Нажмите ESC для выхода в главное меню",
                         self.center_x, self.center_y - 120,
                         arcade.color.WHITE, 20,
                         bold=True, anchor_x="center", anchor_y="center")

    def on_update(self, dt):
        elapsed = time.time() - self.start_time
        if elapsed >= 1000000000000000000000000000000000000:
            self.window.show_view(self.parent_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if self.player_login:
                player_data = self.db.restart(self.player_login)
                if player_data:
                    player = Player(700, 1470)
                    player.login = self.player_login
                    player.credits = player_data[2]
                    player.level = player_data[3]
                    start_window = StartWindow(player, self.db)

                    self.window.show_view(start_window)


class VictoryScreen(arcade.View):

    def __init__(self, player_login, db, parent_view, total_kills):
        super().__init__()
        self.player_login = player_login
        self.db = db
        self.parent_view = parent_view
        self.start_time = time.time()
        self.total_kills = total_kills


    def on_draw(self):
        self.parent_view.on_draw()


        arcade.draw_lbwh_rectangle_filled(
            0, 0,
            self.window.width,
            self.window.height,
            (0, 0, 0, 160)
        )

        arcade.draw_text(
            "Вы убили всех монстров!",
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.GOLD,
            30,
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )

        if self.player_login:
            arcade.draw_text(f"Игрок: {self.player_login}",
                             self.center_x, self.center_y - 50,
                             arcade.color.WHITE, 30,
                             bold=True, anchor_x="center", anchor_y="center")

            arcade.draw_text(f"Убито врагов: {self.total_kills}",
                             self.center_x, self.center_y - 100,
                             arcade.color.WHITE, 28,
                             bold=True, anchor_x="center", anchor_y="center")


    def on_update(self, dt):
        elapsed = time.time() - self.start_time
        if elapsed >= 3:
            self.window.show_view(self.parent_view)


def main():
    window = arcade.Window(const.SCREEN_WIDTH, const.SCREEN_HEIGHT, const.SCREEN_TITLE)
    menu = MainMenu()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()


