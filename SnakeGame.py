import pygame
from pygame.locals import *
import time
import random

r=random

SIZE=40

if __name__ == '__main__':
    pygame.init()

    w=pygame.display.set_mode((1000, 800))
    w.fill((110,110,5))
    block_x,block_y= 100,100

    pygame.display.flip()

    running=True

    class Snake:
        def __init__(self,w, length):
            self.parentscreen=w
            self.block=pygame.image.load("resources/block.jpg")
            self.length=length
            self.x=[40]*length
            self.y=[40]*length
            self.direction='down'

        def move_left(self):
            self.direction='left'
            self.draw()

        def move_right(self):
            self.direction='right'
            self.draw()

        def move_up(self):
            self.direction='up'
            self.draw()

        def move_down(self):
            self.direction='down'
            self.draw()

        def walk(self):

            for i in range(self.length-1, 0, -1):
                self.x[i]=self.x[i-1]
                self.y[i]=self.y[i-1]

            if self.direction=='left':
                self.x[0]-=SIZE

            if self.direction=='right':
                self.x[0]+=SIZE

            if self.direction=='up':
                self.y[0] -= SIZE

            if self.direction=='down':
                self.y[0] += SIZE

            self.draw()

        def expand(self):
            self.length+=1
            self.x.append(1)
            self.y.append(1)

        def draw(self):
                self.parentscreen.fill((110, 110, 5))
                for i in range(self.length):
                    self.parentscreen.blit(self.block, (self.x[i], self.y[i]))
                pygame.display.flip()

class Apple:
    def __init__(self,w):
        self.parentscreen=w
        self.image=pygame.Surface((40,40))
        self.image = pygame.image.load("resources/apple-removebg-preview.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.x=120
        self.y=120

    def draw(self):
        self.parentscreen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = r.randint(1, 25)*SIZE
        self.y = r.randint(1, 20) * SIZE

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.playbackgroundmusic()
        self.surface=pygame.display.set_mode((1000, 800))
        self.snake=Snake(self.surface, 2)
        self.apple=Apple(self.surface)
        self.apple.draw()
        self.snake= Snake(self.surface, 5)
        self.snake.draw()

    def playbackgroundmusic(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1,0)

    def playsound(self, sound_name):
        if sound_name=='crash':
            sound=pygame.mixer.Sound("resource/crash.mp3")
        elif sound_name=='ding':
            sound=pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface, 5)
        self.apple = Apple(self.surface)

    def collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
            return False

    def RenderBackground(self):
        bg=pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def gameover(self):
        self.RenderBackground()
        font=pygame.font.SysFont('arial', 30)
        line1=font.render((f"You lost! Your score was {self.snake.length}"), True, (255,255,255))
        self.surface.blit(line1, (200,350))
        line2=font.render(("Press ENTER to play again or ESCAPE to exit"), True, (255,255,255))
        self.surface.blit(line2, (200, 250))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def play(self):
        self.RenderBackground()
        self.snake.walk()
        self.apple.draw()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.expand()
            self.playsound('ding')
            self.apple.move()

        for i in range(2, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.playsound('crash')
                raise "Collided"

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.playsound('crash')
            raise "Hit the edge"

    def run(self):
        running=True
        pause=False

        while running:

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key==K_RETURN:
                        pause=False
                        pygame.mixer.music.unpause()

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_UP:
                            self.snake.move_up()

                elif event.type == QUIT:
                        running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.gameover()
                pause=True
                self.reset()

            time.sleep(.25)

if __name__=='__main__':
    game=Game()
    game.run()