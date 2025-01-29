import random

import pygame

# Инициализация Pygame
pygame.init()

level = 1

# Устанавливаем размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови фрукты")

# Определяем путь к изображениям
zucchini_path = "data/zucchini.png"  # Путь к изображению для кабачка
pear_path = "data/pear.png"  # Путь к изображению для груши
apple_path = "data/apple.png"  # Путь к изображению для яблока
player_path = "data/snake.png"  # Путь к изображению для игрока

# Загружаем изображения
zucchini_image = pygame.image.load(zucchini_path).convert_alpha()
pear_image = pygame.image.load(pear_path).convert_alpha()
apple_image = pygame.image.load(apple_path).convert_alpha()
player_image = pygame.image.load(player_path).convert_alpha()

# Размеры объектов
zucchini_size = 90  # Размер кабачка
pear_size = 80  # Размер груши
apple_size = 60  # Размер яблока
player_size = 80  # Размер игрока

# Уменьшаем изображения до нужных размеров
zucchini_image = pygame.transform.scale(zucchini_image, (zucchini_size, zucchini_size))
pear_image = pygame.transform.scale(pear_image, (pear_size, pear_size))
apple_image = pygame.transform.scale(apple_image, (apple_size, apple_size))
player_image = pygame.transform.scale(player_image, (player_size, player_size))

MAX_OBJECTS = 10  # Определяем максимальное количество падающих объектов на экране

button_rect = pygame.Rect(300, 300, 200, 100)  # x, y, ширина, высота
fon = pygame.font.Font(None, 36)
button_text = fon.render("Главное меню", True, (255, 255, 255))


# Класс падающих объектов
class FallingObject:
    def __init__(self, obj_type):
        images = [zucchini_image, pear_image, apple_image]  # Изображения объектов
        self.image = images[obj_type]
        self.size = self.image.get_size()  # Используем размеры изображения

        self.x = random.randint(0, WIDTH - self.size[0])  # Ширина изображения
        self.y = -self.size[1]  # Начало выше экрана

        # Скорость падения
        self.speed = [3, 2.5, 2][obj_type]  # Скорость падения
        self.obj_type = obj_type  # Сохраняем тип объекта

    def fall(self, lvl):
        if lvl == 1:
            self.y += self.speed
        elif lvl == 2:
            self.y += self.speed * 1.5
        elif lvl == 3:
            self.y += self.speed * 2

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))  # Рисуем изображение


# Класс для управления игроком
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


# Функция для перезапуска игры
def reset_game():
    return [], Player(), 0, False, False, level  # Возвращаем начальные значения


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    global level
    falling_objects, player, score, game_over, player_won, level = reset_game()

    running = True
    game_started = False  # Состояние начала игры

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
                            player_won,
                            level,
                        ) = reset_game()

        if not game_started:
            screen.fill((255, 255, 255))  # Устанавливаем белый фон
            font = pygame.font.Font(None, 74)
            start_text = font.render("Нажмите Enter, чтобы начать", True, (0, 0, 0))
            text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            screen.blit(start_text, text_rect)
            # Проверка нажатия Enter для начала игры
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                game_started = True

        else:
            if not game_over and not player_won and level < 4:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:  # Движение влево
                    player.move(-player.speed)
                if keys[pygame.K_d]:  # Движение вправо
                    player.move(player.speed)

                # Добавляем новый объект только если их меньше максимального количества
                if len(falling_objects) < MAX_OBJECTS and random.randint(1, 30) == 1:
                    obj_type = random.randint(0, 2)  # 0 - большой, 1 - средний, 2 - маленький
                    falling_objects.append(FallingObject(obj_type))

                # Обновляем позиции объектов и проверяем на столкновение с игроком
                for obj in falling_objects:
                    obj.fall(level)

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
                if score < 0 or level == 4:
                    game_over = True  # Устанавливаем флаг окончания игры

                # Проверяем достижение счета 30 для победы
                if score >= 30:
                    player_won = True  # Устанавливаем флаг победы
                    level += 1

                # Удаляем объекты, которые вышли за границы экрана
                falling_objects = [obj for obj in falling_objects if obj.y < HEIGHT]

                # Очистка экрана
                screen.fill((255, 255, 255))  # Устанавливаем белый фон

                # Рисуем все падающие объекты
                for obj in falling_objects:
                    obj.draw(screen)

                # Рисуем управляемый объект
                player.draw(screen)

                # Отображаем счет
                font = pygame.font.Font(None, 36)
                score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
                screen.blit(
                    score_text, (10, 10)
                )  # Размещение счета в верхнем левом углу

            else:
                # Проверяем, проиграл игрок или победил
                if game_over and level < 4:
                    # Отображение текста "Game Over!" с первоначальным размером шрифта

                    font = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    game_over_text = font.render("Game Over!", True, (255, 0, 0))
                    text_rect = game_over_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 3)
                    )
                    screen.blit(game_over_text, text_rect)
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
                    screen.blit(restart_text, restart_rect)
                    level = 1

                elif player_won or level == 4:
                    # Отображение текста "Вы победили!" с первоначальным размером шрифта
                    font = pygame.font.Font(None, 74)  # Оставляем размер шрифта 74
                    text = ""
                    rst_text = ""
                    if level == 2:
                        text = "Вы прошли первый уровень!"
                        rst_text = "Нажмите пробел чтобы запустить следующий уровень"
                    elif level == 3:
                        text = "Вы прошли второй уровень!"
                        rst_text = "Нажмите пробел чтобы запустить следующий уровень"
                    elif level == 4:
                        text = "Вы победили!"
                        level = 1
                        pygame.draw.rect(screen, (0, 0, 255), button_rect)
                        screen.blit(
                            button_text, (button_rect.x + 20, button_rect.y + 30)
                        )
                    win_text = font.render(text, True, (0, 255, 0))
                    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
                    screen.blit(win_text, text_rect)

                    # Отображение текста "Нажмите пробел чтобы начать заново"
                    smaller_font = pygame.font.Font(
                        None, 36
                    )  # Уменьшаем размер шрифта для второго текста
                    restart_text = smaller_font.render(rst_text, True, (0, 0, 0))
                    restart_rect = restart_text.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    screen.blit(restart_text, restart_rect)
                    # Проверяем нажатие пробела для перезапуска игры
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    (
                        falling_objects,
                        player,
                        score,
                        game_over,
                        player_won,
                        level,
                    ) = reset_game()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()
