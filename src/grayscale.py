import random
import pygame
import os
import numpy as np
import matplotlib.pyplot as plt
from pygame.locals import *

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Image_list = [
    os.path.join(base_dir, "assets", "house1.jpg"),
    os.path.join(base_dir, "assets", "house2.jpg"),
    os.path.join(base_dir, "assets", "house3.jpg"),
    os.path.join(base_dir, "assets", "house4.jpg"),
    # os.path.join(base_dir, "assets", "win1984.png"),
    # os.path.join(base_dir, "assets", "win2077.jpg"),
]


# Запасные изображения для тестирования
def create_test_image(color, size=(250, 250)):
    """
    Создает тестовое изображение заданного цвета
    """
    surface = pygame.Surface(size)
    surface.fill(color)
    return surface


class App:
    def __init__(self, width=920, height=610, caption="GloriousRoboticEelYodeler"):
        """
        Sample App
        Args:
            width: очевидно
            height: нетрудно догадаться
            caption: оставим читателю, как упражнение

        :return: 😂😂😂
        """
        pygame.init()
        self.width, self.height = width, height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(caption)

        # Цвета
        self.colors = {
            'background': (40, 44, 52),
            'panel': (30, 34, 42),
            'text': (220, 220, 220),
            'border': (80, 85, 95),
            'highlight': (97, 175, 239),
            'button': (150,150,250)
        }

        # Шрифты
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)

        # Изображения и данные
        self.images = []
        self.processed_images = []
        self.image_size = (200, 200)
        self.image_surfaces = []
        self.histogram_surfaces = []
        self.selected_image_index = 0
        self.current_image_path = None

        # Позиции и размеры
        self.margin = 20
        self.buttons_panel_width = 70
        self.buttons_panel_height = 30
        self.panel_width = self.width - 2 * self.margin
        self.panel_height = self.height - self.buttons_panel_height - 3 * self.margin

        self.button_prev = pygame.Rect(
            self.margin,
            self.margin,
            self.buttons_panel_width * 0.5 - 5,
            self.buttons_panel_height
            )
        self.button_next = pygame.Rect(
            self.margin + self.buttons_panel_width * 0.5 + 5,
            self.margin,
            self.buttons_panel_width * 0.5 - 5,
            self.buttons_panel_height
            )

        self.images_area = pygame.Rect(
            self.margin,
            self.margin * 2 + self.buttons_panel_height,
            self.panel_width,
            self.panel_height * 0.5 - self.margin * 0.5
        )


        # Область для гистограммы
        self.histogram_area = pygame.Rect(
            self.margin,
            self.margin * 3 + self.buttons_panel_height + self.panel_height  * 0.5,
            self.panel_width,
            self.panel_height  * 0.5 - self.margin * 0.5
        )

        # Размеры миниатюр изображений
        self.thumb_width = 200
        self.thumb_height = 200

        # Флаги состояния
        self.running = False

    def load_images(self):
        """
        Загружает все доступные изображения
        """
        self.image_surfaces = []
        self.images = []

        # Пробуем загрузить изображения из списка
        loaded_count = 0
        for path in Image_list:
            if self.load_single_image(path):
                loaded_count += 1

        # Если не удалось загрузить изображения, создаем тестовые
        if loaded_count == 0:
            print("Не найдены файлы изображений, создаем тестовые изображения")
            test_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
            for i, color in enumerate(test_colors):
                test_surface = create_test_image(color, (self.thumb_width, self.thumb_height))
                self.image_surfaces.append(test_surface)
                # Создаем fake array для тестового изображения
                fake_array = np.random.randint(0, 256, (self.thumb_height, self.thumb_width, 3), dtype=np.uint8)
                self.images.append(fake_array)
                print(f"Создано тестовое изображение {i + 1}")

    def load_single_image(self, path):
        """
        Загружает одно изображение
        """
        try:
            if os.path.exists(path):
                img_surf = pygame.image.load(path).convert()
                scaled_img_surf = pygame.transform.scale(
                    img_surf,
                    (self.thumb_width, self.thumb_height)
                )
                self.image_surfaces.append(scaled_img_surf)

                # Загружаем как numpy array для гистограммы
                try:
                    img_array = plt.imread(path)
                    self.images.append(img_array)
                except:
                    # Если plt.imread не работает, создаем массив из pygame surface
                    img_array = pygame.surfarray.array3d(scaled_img_surf)
                    img_array = np.transpose(img_array, (1, 0, 2))  # Поворачиваем массив
                    self.images.append(img_array)

                print(f"Загружено изображение: {os.path.basename(path)}")
                return True
            else:
                print(f"Файл не найден: {path}")
                return False
        except Exception as e:
            print(f"Ошибка загрузки {path}: {e}")
            return False

    def to_grayscale_1(self, img):
        temp_img = img.copy()
        new_img = img.copy()
        temp_array = temp_img[:,:,0]*0.299 + temp_img[:,:,1]*0.587 + temp_img[:,:,2]*0.114
        new_img[:,:,0] = temp_array
        new_img[:,:,1] = temp_array
        new_img[:,:,2] = temp_array
        return new_img

    def to_grayscale_2(self, img):
        # temp_img = img.copy()
        # new_img = temp_img[:,:,0]#*0.2126 + temp_img[:,:,1]*0.7152 + temp_img[:,:,2]*0.0722
        temp_img = img.copy()
        new_img = img.copy()
        temp_array = temp_img[:,:,0]*0.2126 + temp_img[:,:,1]*0.7152 + temp_img[:,:,2]*0.0722
        new_img[:,:,0] = temp_array
        new_img[:,:,1] = temp_array
        new_img[:,:,2] = temp_array
        return new_img

    def grayscale_sub(self, img1, img2):
        new_img = abs(img1 - img2)
        return new_img

    def create_histograms(self):
        """
        Создает 4 гистограммы для текущего изображения:
        - 3 отдельные гистограммы для каждого цветового канала
        - 1 совмещенная гистограмма со всеми тремя каналами
        """
        if not self.images or self.selected_image_index >= len(self.images):
            return []

        try:
            img = self.images[self.selected_image_index]

            # Нормализуем значения, если они в диапазоне [0, 1]
            if abs(int(img[:, :, 0][0][0]) - img[:, :, 0][0][0]) > 0.0001:
                img = img.copy()
                img *= 255

            histogram_surfaces = []

            if len(img.shape) == 3:  # Цветное изображение
                colors = ['lightgray', 'darkgray']
                methods_names = ['Полутоновое 1', 'Полутоновое 2']

                # Создаем 2 гистограммы для каждого метода
                for i, (color, name) in enumerate(zip(colors, methods_names)):
                    fig, ax = plt.subplots(figsize=(2, 2))
                    ax.hist(self.processed_images[i][:, :, 0].flatten(), bins=16, alpha=0.8, color=color, density=True)
                    # ax.set_xlabel('Значение пикселя', fontsize=8)
                    # ax.set_ylabel('Плотность', fontsize=8)
                    ax.set_title(name, fontsize=9)
                    ax.tick_params(axis='both', which='major', labelsize=7)
                    plt.tight_layout()
                    
                    # Конвертируем в pygame surface
                    fig.canvas.draw()
                    buf = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
                    width, height = fig.canvas.get_width_height()
                    buf = buf.reshape(height, width, 4)  # RGBA формат

                    # Конвертируем в RGB для pygame (убираем альфа-канал)
                    rgb_buf = buf[:, :, :3]
                    histogram_surf = pygame.surfarray.make_surface(rgb_buf.swapaxes(0, 1))
                    
                    # Масштабируем под размер области
                    scaled_surf = pygame.transform.scale(
                        histogram_surf,
                        (int(self.thumb_width), int(self.thumb_height))
                    )
                    histogram_surfaces.append(scaled_surf)
                    plt.close(fig)

            return histogram_surfaces

        except Exception as e:
            print(f"Ошибка создания гистограмм: {e}")
            # Создаем заглушки
            histogram_surfaces = []
            for i in range(4):
                fallback_surf = pygame.Surface((int(self.histogram_area.width // 2 - 15),
                                                int(self.histogram_area.height // 2 - 40)))
                fallback_surf.fill((60, 60, 60))
                histogram_surfaces.append(fallback_surf)
            return histogram_surfaces

    def process_image(self, img_array, process_type="original"):
        """
        Обрабатывает изображение в зависимости от типа обработки
        Args:
            img_array: numpy array изображения
            process_type: тип обработки ("original", "halftone1", "halftone2", "substraction")
        Returns:
            обработанный numpy array
        """

        if process_type == "original":
            return img_array.copy()
        # red -> 0, green -> 1, blue -> 2
        elif process_type == "halftone1":
            processed = self.to_grayscale_1(img_array)
            # plt.imsave(arr=processed, fname=os.path.join(base_dir, "assets", 'red.jpg'))
            return processed
        elif process_type == "halftone2":
            processed = self.to_grayscale_2(img_array)
            return processed
        elif process_type == "substraction":
            processed = self.grayscale_sub(self.to_grayscale_1(img_array), self.to_grayscale_2(img_array))
            return processed
        return img_array.copy()

    def create_processed_surfaces(self):
        """Создает 4 обработанные версии текущего изображения"""
        if not self.images or self.selected_image_index >= len(self.images):
            return []

        processed_surfaces = []

        for processed_img in self.processed_images:


            try:
                # Создаем pygame surface через разные подходы
                if processed_img.shape[2] == 3:  # RGB
                    surf = pygame.surfarray.make_surface(processed_img.swapaxes(0, 1))
                else:  # RGBA
                    surf = pygame.surfarray.make_surface(processed_img[:, :, :3].swapaxes(0, 1))

                scaled_surf = pygame.transform.scale(surf, (self.thumb_width, self.thumb_height))
                processed_surfaces.append(scaled_surf)

            except Exception as e:
                print(f"Ошибка создания surface для {process_type}: {e}")
                print(f"Форма массива: {processed_img.shape}, тип: {processed_img.dtype}")

                # Создаем заглушку
                fallback_surf = pygame.Surface((self.thumb_width, self.thumb_height))
                fallback_surf.fill((100, 100, 100))  # Серый цвет
                processed_surfaces.append(fallback_surf)

        return processed_surfaces

    def create_processed_images(self):
        """Создает 4 обработанные версии текущего изображения"""
        if not self.images or self.selected_image_index >= len(self.images):
            return []

        base_img = self.images[self.selected_image_index].copy()
        process_types = ["original", "halftone1", "halftone2", "substraction"]
        processed_images = []

        for process_type in process_types:
            processed_img = self.process_image(base_img, process_type)

            try:
                processed_images.append(processed_img)

            except Exception as e:
                print(f"Ошибка обработки изображения для {process_type}: {e}")
                print(f"Форма массива: {processed_img.shape}, тип: {processed_img.dtype}")

                # Возвращаем то же изображение
                processed_images.append(base_img)

        return processed_images

    def draw_interface(self):
        """
        Отрисовка интерфейса
        """
        # Очищаем экран
        self.screen.fill(self.colors['background'])

        # Рисуем кнопки:
        pygame.draw.rect(self.screen, self.colors['button'], self.button_prev, border_radius=8)
        text = "<"
        text_surf = self.font_large.render(text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.button_prev.x + 8, self.button_prev.y + 2))  

        pygame.draw.rect(self.screen, self.colors['button'], self.button_next, border_radius=8)
        text = ">"
        text_surf = self.font_large.render(text, True, self.colors['text'])
        self.screen.blit(text_surf, (self.button_next.x + 10, self.button_next.y + 2))
        # Рисуем рамки областей
        pygame.draw.rect(self.screen, self.colors['border'], self.images_area, 2)
        pygame.draw.rect(self.screen, self.colors['border'], self.histogram_area, 2)

        # Отрисовка текущего изображения
        if self.image_surfaces and self.selected_image_index < len(self.image_surfaces):
            processed_surfaces = self.create_processed_surfaces()

            if processed_surfaces:
                # Заголовки для каждой версии
                titles = ["Оригинал", "Полутоновое 1", "Полутоновое 2", "Разность"]

                # Располагаем изображения в ряд
                y = self.images_area.y + 40
                for i, (surf, title) in enumerate(zip(processed_surfaces, titles)):

                    x = self.images_area.x + 10 + i * (self.thumb_width + 20)

                    # Рисуем изображение
                    self.screen.blit(surf, (x, y))

                    # Рисуем заголовок
                    title_surf = self.font_small.render(title, True, self.colors['text'])
                    self.screen.blit(title_surf, (x, y - 20))

            # Информация об изображении
            info_text = f"Изображение {self.selected_image_index + 1}/{len(self.image_surfaces)}"
            text_surf = self.font_medium.render(info_text, True, self.colors['text'])
            self.screen.blit(text_surf, (self.images_area.x + 10, self.images_area.y + 5))

            # Отрисовка двух гистограмм
            if self.histogram_surfaces:
                histogram_titles = ["Полутоновое 1", "Полутоновое 2"]

                y = self.histogram_area.y + 35
                for i, (hist_surf, title) in enumerate(zip(self.histogram_surfaces, histogram_titles)):
                    x = self.histogram_area.x + 10 + (i + 1) * (self.thumb_width + 20)

                    # Рисуем гистограмму
                    self.screen.blit(hist_surf, (x, y))

                    # Рисуем заголовок
                    title_surf = self.font_small.render(title, True, self.colors['text'])
                    self.screen.blit(title_surf, (x, y - 15))

            # Заголовок области гистограммы
            hist_title = self.font_medium.render("Гистограммы полутоновых изображений (Тон / Вероятность)", True, self.colors['text'])
            self.screen.blit(hist_title, (self.histogram_area.x + 10, self.histogram_area.y + 5))
    
    def change_image_ind(self, changer):
        new_index = (len(self.image_surfaces) + self.selected_image_index + changer) % len(self.image_surfaces)
        if new_index < len(self.image_surfaces):
            self.selected_image_index = new_index
            self.processed_images = self.create_processed_images() # Пересоздаём изображения
            self.histogram_surfaces = self.create_histograms()  # Пересоздаем гистограммы

    def collide(self, point, collision_box):
        x_col = (collision_box.x <= point[0]) and (collision_box.x + collision_box.width >= point[0])
        y_col = (collision_box.y <= point[1]) and (collision_box.y + collision_box.height >= point[1])
        return x_col and y_col

    def handle_events(self):
        """
        Обработка событий
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == MOUSEBUTTONDOWN:
                if self.collide(event.pos,self.button_prev):
                    self.change_image_ind(-1)
                elif self.collide(event.pos,self.button_next):
                    self.change_image_ind(1)

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_LEFT:
                    self.change_image_ind(-1)
                elif event.key == K_RIGHT:
                    self.change_image_ind(1)

    def main_loop(self):
        """
        Главный цикл приложения
        """
        # Загружаем изображения
        self.load_images()

        # Создаем начальные гистограммы
        if self.images:
            self.processed_images = self.create_processed_images()
            self.histogram_surfaces = self.create_histograms()

        self.running = True
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()
            self.draw_interface()  # Добавили отрисовку!
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    app = App()
    app.main_loop()