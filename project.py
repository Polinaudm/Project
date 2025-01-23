import pygame
import random
import os
import sys

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Падающие объекты")

# Определяем цвета для каждого типа объекта
COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]  # Красный, Синий, Зеленый
MAX_OBJECTS = 5  # Максимальное количество падающих объектов на экране


def load_image(name, colorkey=None):
    # функция для загрузки картинок из папки data
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# Класс для падающих объектов
class FallingObject:
    def __init__(self, obj_type):
        sizes = [80, 50, 30]  # Размеры объектов: Большой, Средний, Маленький
        self.size = sizes[obj_type]
        self.color = COLORS[obj_type]
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size

        # Увеличиваем скорость падения объектов
        self.speed = [3, 2.5, 2][obj_type]  # Скорость падения: увеличена
        self.obj_type = obj_type  # Сохраняем тип объекта

    def fall(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


# Класс для управляемого объекта
class Player:
    def __init__(self):
        self.size = 50
        self.color = (0, 0, 0)  # Черный цвет
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
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    falling_objects = []
    player = Player()
    score = 0  # Начальный счет

    running = True
    game_over = False  # Флаг, указывающий, окончена ли игра

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:  # Движение влево
                player.move(-player.speed)
            if keys[pygame.K_d]:  # Движение вправо
                player.move(player.speed)

            # Добавляем новый объект только если их меньше максимального количества
            if len(falling_objects) < MAX_OBJECTS and random.randint(1, 30) == 1:
                obj_type = random.randint(
                    0, 2
                )  # 0 - большой, 1 - средний, 2 - маленький
                falling_objects.append(FallingObject(obj_type))

            # Обновляем позиции объектов и проверяем на столкновение с игроком
            for obj in falling_objects:
                obj.fall()

                # Проверяем на столкновение
                if player.get_rect().colliderect(
                        pygame.Rect(obj.x, obj.y, obj.size, obj.size)
                ):
                    if obj.obj_type == 0:  # Большой объект
                        score -= 1
                    elif obj.obj_type == 1:  # Средний объект
                        score += 2
                    elif obj.obj_type == 2:  # Маленький объект
                        score += 1

                    # Удаляем объект после столкновения

                    falling_objects.remove(obj)

            # Проверяем, не достиг ли счет отрицательных значений
            if score < 0:
                game_over = True  # Устанавливаем флаг окончания игры

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
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
            window.blit(score_text, (10, 10))  # Размещение счета в верхнем левом углу

        else:
            # Отображение текста "Game Over!" с меньшим размером шрифта
            font = pygame.font.Font(None, 48)  # Уменьшен размер шрифта
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(game_over_text, text_rect)

            # Отображение текста "Нажмите пробел чтобы начать заново" с меньшим размером шрифта
            restart_text = font.render(
                "Нажмите SPACE чтобы начать заново", True, (0, 0, 0)
            )
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            window.blit(restart_text, restart_rect)

            # Проверяем нажатие пробела для перезапуска игры
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                main()  # Запуск новой игры

        # Обновляем экран
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
