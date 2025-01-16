import pygame
import random

# Инициализация Pygame
pygame.init()

# Устанавливаем размеры окна
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Падающие объекты")

# Определяем цвета для каждого типа объекта
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0)]  # Красный, Синий, Зеленый
max_objects = 5  # Максимальное количество падающих объектов на экране


# Класс для падающих объектов
class FallingObject:
    def __init__(self, obj_type):
        sizes = [80, 50, 30]  # Большой, Средний, Маленький
        self.size = sizes[obj_type]
        self.color = colors[obj_type]
        self.x = random.randint(0, WIDTH - self.size)
        self.y = -self.size
        self.speed = [2, 1.5, 1][obj_type]  # Скорость падения

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


# Основной игровой цикл
def main():
    clock = pygame.time.Clock()
    falling_objects = []
    player = Player()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Движение влево
            player.move(-player.speed)
        if keys[pygame.K_d]:  # Движение вправо
            player.move(player.speed)

        # Добавляем новый объект только если их меньше максимального количества
        if len(falling_objects) < max_objects and random.randint(1, 30) == 1:
            obj_type = random.randint(0, 2)  # 0 - большой, 1 - средний, 2 - маленький
            falling_objects.append(FallingObject(obj_type))

        # Обновляем позиции объектов
        for obj in falling_objects:
            obj.fall()

        # Удаляем объекты, которые вышли за границы экрана
        falling_objects = [obj for obj in falling_objects if obj.y < HEIGHT]

        # Очистка экрана
        window.fill((255, 255, 255))  # Устанавливаем белый фон

        # Рисуем все падающие объекты
        for obj in falling_objects:
            obj.draw(window)

        # Рисуем управляемый объект
        player.draw(window)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
