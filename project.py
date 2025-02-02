import random
from datetime import datetime
import pygame
import os
import sqlite3

# Инициализация Pygame
pygame.init()

level = 1

conn = sqlite3.connect("Leaders.db")
cursor = conn.cursor()

# Устанавливаем размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови фрукты")

image_big_path = "../data/zucchini.png"  # Путь к изображению для большого объекта
image_medium_path = "../data/pear.png"  # Путь к изображению для среднего объекта
image_small_path = "../data/apple.png"  # Путь к изображению для маленького объекта
image_player_path = "../data/snake.png"  # Путь к изображению для игрока

# Загружаем изображения
big_obj_image = pygame.image.load(image_big_path).convert_alpha()
medium_obj_image = pygame.image.load(image_medium_path).convert_alpha()
small_obj_image = pygame.image.load(image_small_path).convert_alpha()
player_image = pygame.image.load(image_player_path).convert_alpha()

# Определяем размеры объектов
size_large = 90  # Размер большого объекта
size_medium = 80  # Размер среднего объекта
size_small = 60  # Размер маленького объекта
player_size = 80  # Размер игрока (изменено на 80 пикселей)
# Уменьшаем изображения до нужных размеров
big_obj_image = pygame.transform.scale(big_obj_image, (size_large, size_large))
medium_obj_image = pygame.transform.scale(medium_obj_image, (size_medium, size_medium))
small_obj_image = pygame.transform.scale(small_obj_image, (size_small, size_small))
player_image = pygame.transform.scale(
    player_image, (player_size, player_size)
)  # Масштабируем изображение игрока

max_objects = 10  # Определяем максимальное количество падающих объектов на экране

#  Кнопка выхода в главное меню после завершения игры
button_rect = pygame.Rect(300, 300, 200, 100)  # x, y, ширина, высота
fone = pygame.font.Font(None, 36)
button_text = fone.render("Главное меню", True, (255, 255, 255))

#  Поле ввода имени
input_box = pygame.Rect(300, 170, 300, 40)
color_inactive = (0, 0, 0)
color_active = (0, 0, 255)
color = (255, 0, 0)
nick = ""
active = False
show_input = True
font_nick = pygame.font.Font(None, 32)


#  Данные для таблицы
table_font = pygame.font.Font(None, 36)
cell_width = 180
cell_height = 40
table_x = 40
table_y = 350
table_header = ["Имя", "1 уровень", "2 уровень", "3 уровень"]


# Класс для падающих объектов
class FallingObject:
    def __init__(self, obj_type):
        images = [
            big_obj_image,
            medium_obj_image,
            small_obj_image,
        ]  # Изображения объектов
        self.image = images[obj_type]
        self.size = self.image.get_size()  # Используем размеры изображения

        self.x = random.randint(0, WIDTH - self.size[0])  # Ширина изображения
        self.y = -self.size[1]  # Начало выше экрана

        # Скорость падения
        self.speed = [3, 2.5, 2][obj_type]  # Скорость падения: увеличена
        self.obj_type = obj_type  # Сохраняем тип объекта

    def fall(self, lvl):
        if lvl == 1:
            self.y += self.speed
        elif lvl == 2:
            self.y += self.speed * 1.5
        elif lvl == 3:
            self.y += self.speed * 2
        print(lvl, level)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))  # Рисуем изображение


# Класс для управляемого объекта
class Player:
    def __init__(self):
        self.size = player_size  # Размер игрока
        self.x = (WIDTH - self.size) // 2  # Начальная позиция по центру
        self.y = HEIGHT - self.size - 10  # Немного выше низа экрана
        self.speed = 5  # Скорость движения

    def move(self, dx):
        self.x += dx
        # Ограничиваем движение в пределах экрана
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH - self.size:
            self.x = WIDTH - self.size

    def draw(self, surface):
        surface.blit(player_image, (self.x, self.y))  # Рисуем изображение игрока

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


all_sprites = pygame.sprite.Group()


def load_image(name, color_key=None):
    fullname = os.path.join("../data", name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print("Cannot load image:", name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(
            20, -60, sheet.get_width() // columns, sheet.get_height() // rows
        )
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                )

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


dragon = AnimatedSprite(
    load_image("gamasha.png", color_key=(71, 113, 77)), 8, 5, 350, 300
)


# Функция для перезапуска игры
def reset_game():
    return [], Player(), 0, False, False, level  # Возвращаем начальные значения


def next_level(lvl):
    return [], Player(), 0, False, False, lvl


def ret_zero(a):
    return a[0]


def draw_table(data):
    # Рисуем заголовок таблицы
    for col_index, title in enumerate(table_header):
        rect = pygame.Rect(
            table_x + col_index * cell_width, table_y, cell_width, cell_height
        )
        pygame.draw.rect(
            window, (173, 216, 230), rect
        )  # Светло-голубой фон для заголовка
        pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Черная рамка
        title_surface = table_font.render(title, True, (0, 0, 0))
        text_rect = title_surface.get_rect(center=rect.center)
        window.blit(title_surface, text_rect)

    # Рисуем строки таблицы
    for row_index, row in enumerate(data):
        for col_index, item in enumerate(row):
            rect = pygame.Rect(
                table_x + col_index * cell_width,
                table_y + (row_index + 1) * cell_height,
                cell_width,
                cell_height,
            )
            pygame.draw.rect(window, (255, 255, 255), rect)  # Белый цвет фона ячейки
            pygame.draw.rect(window, (0, 0, 0), rect, 2)  # Черная рамка
            text = table_font.render(str(item), True, (0, 0, 0))  # Черный текст
            text_rect = text.get_rect(center=rect.center)
            window.blit(text, text_rect)


def get_top_players():
    conn_1 = sqlite3.connect("Leaders.db")
    cursor_1 = conn.cursor()
    # Запрос для получения топ-5 игроков по каждому уровню
    players = cursor_1.execute(
        """
        SELECT nick, level_1, level_2, level_3
        FROM leaders_list
        ORDER BY level_1 DESC, level_2 DESC, level_3 DESC
    """
    ).fetchall()
    # Оставляем только 5 лучших результатов
    top_players = players[:5]

    conn_1.close()
    return top_players


# Основной игровой цикл


def main():
    clock = pygame.time.Clock()
    global active, nick, font_nick
    falling_objects, player, score, game_over, player_win, level_g = reset_game()
    running = True
    game_started = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левую кнопку мыши
                    if button_rect.collidepoint(
                        event.pos
                    ):  # Проверка, нажатие внутри кнопки
                        game_started = False
                        (
                            falling_objects,
                            player,
                            score,
                            game_over,
                            player_win,
                            level_g,
                        ) = reset_game()
                if input_box.collidepoint(event.pos):
                    active = not active  # Пробел для активации ввода
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if (
                    keys[pygame.K_RETURN] and nick != ""
                ):  # Проверяем нажатие клавиши Enter
                    # show_input = False
                    print(f"Имя: {nick}")
                    nicks = cursor.execute(
                        """SELECT nick FROM leaders_list"""
                    ).fetchall()
                    nicks = list(map(ret_zero, nicks))
                    print(nicks)
                    if nick not in nicks and len(nick) > 0:
                        cursor.execute(
                            """INSERT INTO leaders_list (nick) VALUES (?)""", (nick,)
                        )
                        conn.commit()
                    player_nick = nick
                    nick = ""  # Очищаем поле после отправки
                    time_start = datetime.now()
                    game_started = True
                if keys[pygame.K_BACKSPACE]:
                    nick = nick[:-1]
                else:
                    if event.unicode.isalpha() or event.unicode.isdigit():
                        nick += event.unicode

        if not game_started:
            window.fill((255, 255, 255))
            top_players = get_top_players()
            draw_table(top_players)
            pygame.draw.rect(window, (0, 0, 0), input_box, 2)
            txt_surface = font_nick.render(nick, True, (0, 0, 0))
            window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            input_box.w = max(200, txt_surface.get_width() + 10)
            font = pygame.font.Font(None, 37)
            start_text = font.render(
                "Введите имя и нажмите Enter, чтобы начать", True, (0, 0, 0)
            )
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 5))
            window.blit(start_text, text_rect)
            control_text = font.render(
                "Для движения персонажа используйте клавиши A и D", True, (0, 255, 0)
            )
            ctrl_txt = control_text.get_rect(center=(WIDTH // 2, HEIGHT // 8))
            window.blit(control_text, ctrl_txt)
            rules_text = font.render("Собирайте только фрукты", True, (255, 0, 0))
            rul_txt = rules_text.get_rect(center=(WIDTH // 2, HEIGHT // 18))
            window.blit(rules_text, rul_txt)
            all_sprites.draw(window)
            all_sprites.update()

        else:
            if not game_over and not player_win and level_g < 4:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:  # Движение влево
                    player.move(-player.speed)
                if keys[pygame.K_d]:  # Движение вправо
                    player.move(player.speed)

                # Добавляем новый объект только если их меньше максимального количества
                if len(falling_objects) < max_objects and random.randint(1, 30) == 1:
                    obj_type = random.randint(
                        0, 2
                    )  # 0 - большой, 1 - средний, 2 - маленький
                    falling_objects.append(FallingObject(obj_type))

                # Обновляем позиции объектов и проверяем на столкновение с игроком
                for obj in falling_objects:
                    obj.fall(level_g)

                    # Проверяем на столкновение
                    if player.get_rect().colliderect(
                        pygame.Rect(obj.x, obj.y, obj.size[0], obj.size[1])
                    ):
                        if obj.obj_type == 0:  # Большой объект
                            score -= 2  # Уменьшаем на 2 очка
                        elif obj.obj_type == 1:  # Средний объект
                            score += 2
                        elif obj.obj_type == 2:  # Маленький объект
                            score += 1

                        # Удаляем объект после столкновения
                        falling_objects.remove(obj)

                # Проверяем, не достиг ли счет отрицательных значений
                if score < 0 or level_g == 4:
                    game_over = True  # Устанавливаем флаг окончания игры

                # Проверяем достижение счета 30 для победы
                if score >= 30:
                    raznica = current_time - time_start
                    vr = str(raznica.seconds) + "." + str(raznica.microseconds)[:2]
                    print(f"{raznica.seconds}:{raznica.microseconds}", level_g)
                    cursor.execute(
                        f"""UPDATE leaders_list 
                            SET level_{level_g} = CASE
                                    WHEN level_{level_g} > {vr} THEN {vr} 
                                    WHEN level_{level_g} = 0 THEN {vr}
                                    WHEN level_{level_g} <= {vr} THEN level_{level_g}
                                    END 
                            WHERE nick = ?""",
                        (player_nick,),
                    )
                    conn.commit()
                    player_win = True  # Устанавливаем флаг победы
                    level_g += 1

                # Удаляем объекты, которые вышли за границы экрана
                falling_objects = [obj for obj in falling_objects if obj.y < HEIGHT]

                # Очистка экрана
                window.fill((255, 255, 255))  # Устанавливаем белый фон

                # Рисуем все падающие объекты
                for obj in falling_objects:
                    obj.draw(window)

                # Рисуем управляемый объект
                player.draw(window)

                # Отображаем счет
                font_1 = pygame.font.Font(None, 36)
                score_text = font_1.render(f"Счет: {score}", True, (0, 0, 0))
                window.blit(
                    score_text, (10, 10)
                )  # Размещение счета в верхнем левом углу

                current_time = datetime.now()
                sec = current_time - time_start
                fon = pygame.font.Font(None, 36)
                secundomer = fon.render(
                    f"{sec.seconds}.{str(sec.microseconds)[:2]}", True, (0, 0, 0)
                )
                window.blit(secundomer, (150, 10))
            else:
                # Проверяем, проиграл игрок или победил
                if game_over and level_g < 4:
                    # Отображение текста "Game Over!" с первоначальным размером шрифта

                    font_2 = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    game_over_text = font_2.render("Game Over!", True, (255, 0, 0))
                    text_rect = game_over_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 3)
                    )
                    window.blit(game_over_text, text_rect)
                    # Отображение текста "Нажмите пробел чтобы начать заново" с уменьшенным размером шрифта
                    smaller_font = pygame.font.Font(
                        None, 36
                    )  # Уменьшаем размер шрифта для второго текста
                    restart_text = smaller_font.render(
                        "Нажмите пробел чтобы начать заново", True, (0, 0, 0)
                    )
                    restart_rect = restart_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    window.blit(restart_text, restart_rect)
                    level_g = 1

                elif player_win or level_g == 4:
                    # Отображение текста "Поздравляем, игра пройдена!"
                    font_3 = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    text_2 = ""
                    rst_text = ""
                    if level_g == 2:
                        text_2 = "Вы прошли первый уровень!"
                        rst_text = "Нажмите пробел чтобы запустить следующий уровень"
                    elif level_g == 3:
                        text_2 = "Вы прошли второй уровень!"
                        rst_text = "Нажмите пробел чтобы запустить следующий уровень"
                    elif level_g == 4:
                        text_2 = "Поздравляем, игра пройдена!"
                        nick = ""
                        pygame.draw.rect(window, (0, 0, 255), button_rect)
                        window.blit(
                            button_text, (button_rect.x + 20, button_rect.y + 30)
                        )
                    win_text = font_3.render(text_2, True, (0, 255, 0))
                    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                    window.blit(win_text, text_rect)

                    # Отображение текста "Нажмите пробел чтобы начать заново"
                    smaller_font = pygame.font.Font(
                        None, 36
                    )  # Уменьшаем размер шрифта для второго текста
                    restart_text = smaller_font.render(rst_text, True, (0, 0, 0))
                    restart_rect = restart_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    window.blit(restart_text, restart_rect)
                    # Проверяем нажатие пробела для перезапуска игры
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and level_g < 4:
                    time_start = datetime.now()
                    (
                        falling_objects,
                        player,
                        score,
                        game_over,
                        player_win,
                        level_g,
                    ) = next_level(level_g)
                # Обновляем экран
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
