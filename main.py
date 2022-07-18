import pygame
from random import randint
from sys import exit
from time import sleep

WIDTH = 500
HEIGHT = 500
FPS = 60
NAMEPROJECT = 'SQUARE'
BACKGROUND = 'background/menu-background.png'

class Color:
    def __init__(self):
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)

class Background:
    def __init__(self, path, size):
        self.path = path
        self.size = size.split('x')

    def transform(self):
        img = pygame.image.load(self.path)
        background = pygame.transform.scale(img, [int(self.size[0]), int(self.size[1])])
        return background

class MusicSound:
    def __init__(self, path):
        self.path = path
        pygame.mixer.init()
        pygame.mixer.music.load('{}'.format(path))


    def play(self, volume):
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    @staticmethod
    def pause():
        pygame.mixer.music.pause()
    
    @staticmethod
    def unpause():
        pygame.mixer.music.unpause()
        pygame.mixer.music.stop()

class Menu:
    def __init__(self, TITULO, MUSICPATH):
        self.img = Background(BACKGROUND, '{}x{}'.format(WIDTH, HEIGHT))
        self.bg = self.img.transform()
        self.color = Color()
        self.menu = pygame.display.set_mode((WIDTH, HEIGHT))
        self.TITULO = TITULO
        self.MUSICPATH = MUSICPATH
        self.VOLUME = 0.2
        self.sound = MusicSound(self.MUSICPATH)
        pygame.display.set_caption(NAMEPROJECT)

    def show_text(self, text, bgcolor):
        font = pygame.font.SysFont(None, 24)
        text = font.render(text, True, self.color.WHITE, bgcolor)
        return text

    def start(self, pos_text):
        while True:
            self.menu.fill(self.color.BLACK)
            self.menu.blit(self.bg, (0, 0))
            self.menu.blit(self.show_text(self.TITULO, self.color.RED), pos_text)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.sound.play(self.VOLUME)
                sleep(0.6)
                break
            pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        self.img = Background(BACKGROUND, '{}x{}'.format(WIDTH, HEIGHT))
        self.bg = self.img.transform()
        self.color = Color()
        self.menu = Menu('PRESS SPACE FOR START', 'media/sound.ogg')
        self.menu.start((140, 240))
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.MUSICPATH = 'media/sound.ogg'
        self.VOLUME = 0.2
        self.sound = MusicSound(self.MUSICPATH)
        pygame.display.set_caption(NAMEPROJECT)

    def start(self):
        block_white_x, block_white_y = 30, 40
        vel = 40
        block_red_x, block_red_y = 190, 190
        block_green_x, block_green_y = 390, 40
        block_white_cont = 0
        while True:
            self.screen.fill(self.color.BLACK)
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.menu.show_text('SCORE: {}'.format(block_white_cont), self.color.RED), (195, 5))

            block_white = pygame.draw.rect(self.screen, self.color.WHITE, [block_white_x, block_white_y, 40, 40], 0)
            block_red = pygame.draw.rect(self.screen, self.color.RED, [block_red_x, block_red_y, 40, 40], 0)
            block_green = pygame.draw.rect(self.screen, self.color.GREEN, [block_green_x, block_green_y, 40, 40], 0)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.sound.unpause()
                    pygame.quit()
                    exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] and block_white_x > 15:
                    block_white_x -= vel

                if keys[pygame.K_RIGHT] and block_white_x < 500:
                    block_white_x += vel

                if keys[pygame.K_UP] and block_white_y > 15:
                    block_white_y -= vel

                if keys[pygame.K_DOWN] and block_white_y < 500:
                    block_white_y += vel

            if block_white.colliderect(block_red): 
                self.sound.play(self.VOLUME)
                block_white_cont += 1
                while True:
                    print(f'DEBUG: Calculating block position: block_red_x: {block_red_x}, block_red_y: {block_red_y}, block_green_x: {block_green_x}, block_green_y: {block_green_y}')
                    block_red_x = randint(15, 400); block_red_y = randint(15, 400)
                    block_green_x = randint(15, 400); block_green_y = randint(15, 400)
                    
                    if block_red_x != block_white_x and block_red_y != block_white_y:
                        if block_green_x != block_red_x and block_green_y != block_red_y:
                            if block_green_x != block_white_x and block_green_y != block_white_y:
                                    print('DEBUG: No collision position between blocks')
                                    break      

            if block_white.colliderect(block_green):
                game = Game()
                game.start()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.start()
