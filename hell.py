import pygame
from random import randint
import sys

pygame.init()

if getattr(sys, 'frozen', False):       # Эти строчки нужны, для нормальной архивации в exe
    os.chdir(sys._MEIPASS)              # Создает временную папку в которой хранятся данные во время архивации
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

font=pygame.font.Font("FreeSansBold.ttf", 20)   #Устанавливаем другой шрифт так как станданртый шрифт при запуске в пайгем выдает ошикку

"""Устанавливаем переенные"""
score=0
W=800
H=600
black    = (   0,   0,   0)
white    =(     255,  255, 255)
size=[W,H]
"""Загружаем изображения"""
background=pygame.image.load("wp.jpg")
win_background = pygame.image.load("Winner.jpg")
souls_img =("s.png", 's.png')
souls_surfase=[]                    # Список для хранения изображений душ
angels_img =("angel.png", 'angel.png')
angels_surfase=[]                    # Список для ангелов
devil=pygame.image.load("devil.png")
"""Переменый используемые в циклах"""
iteration=0
win=False
done=True
make=False


pygame.time.set_timer(pygame.USEREVENT, 2000) # устанавливает определенный промежуток времени.
screen=pygame.display.set_mode(size)           #Установка размеров окна
pygame.display.set_caption("Welcome to hell")
clock=pygame.time.Clock()                      #Переменная для установки числа кадров
"""Загрузка музыки и звуков"""
pygame.mixer.music.load('T.mp3')
pygame.mixer.music.play(-1)
sound1 = pygame.mixer.Sound('apple.aiff')
sound2 = pygame.mixer.Sound('scream.wav')
sound3 = pygame.mixer.Sound('fanfare.wav')

"""Добавление изображение в список"""
for i in range(len(souls_img)):
    souls_surfase.append(pygame.image.load(souls_img[i]).convert())
for i in range(len(angels_img)):
    angels_surfase.append(pygame.image.load(angels_img[i]).convert())

class avatar(pygame.sprite.Sprite):
    def __init__(self, surf, x, y, step):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf                       #Возвращает изображение
        self.rect = self.image.get_rect(center=(x, y)) #rect управляет прямоугольными поверхностями, get_rect возврашает положения rect
        self.x = x
        self.y = y
        self.step = step
    def _move(self, event):
        if self.rect.x  > 800:
            self.rect.x=0
        elif self.rect.x <0:
            self.rect.x=800
        elif self.rect.y > 600:
            self.rect.y=0
        elif self.rect.y <0:
            self.rect.y=600
        """Настройка управления """
        keys = pygame.key.get_pressed()# Создает картеж если клавиша нажата возврашает 1 если нет то ноль.
        if keys[pygame.K_w]:
            self.rect = self.rect.move(0, -self.step)
        elif keys[pygame.K_s]:
            self.rect = self.rect.move(0, self.step)
        elif keys[pygame.K_a]:
            self.rect = self.rect.move(-self.step, 0)
        elif keys[pygame.K_d]:
            self.rect = self.rect.move(self.step, 0)


class soul(pygame.sprite.Sprite):
    def __init__(self,x, y, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.add(group)
        self.speed=(randint(1,10))              #Устанавливаю случайную скорость от 1 до 10
        self.image.set_colorkey(black)          #Делает прозрачным определенный цвет, в данном случае черный
    def update(self):
        if self.rect.x  < 800:
            self.rect.x += self.speed
        else:
            self.kill()

class angel(pygame.sprite.Sprite):
    def __init__(self,x, y, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y
        self.add(group)
        self.speed=(randint(5,10))
        self.image.set_colorkey(black)
    def update(self):
        if self.rect.x  < 795:
            self.rect.x += self.speed
        else:
            self.kill()
"""Задаю, начальные положения для гг, трех душ и одного ангела, а так же создаю две группы """
avt=avatar(devil,400,300,10)
souls = pygame.sprite.Group()
angels = pygame.sprite.Group()
soul(40,100, souls_surfase[0],souls)
soul(40,200, souls_surfase[0],souls)
soul(40,400, souls_surfase[0],souls)
angel(40,500, angels_surfase[0],angels)

while 1:
    while not(make):
        if win==True:
            screen.blit(win_background , (0, 0))            #Устанавливаю фон в случае победы
            text = font.render("Поздравляю вы победили!!!",True,white)
            screen.blit(text, [250,10])
            text = font.render("Если хотите сыграть еще раз нажмите пробел.",True,white)
            screen.blit(text, [250,550])
        elif iteration == 0 and win==False:
            screen.fill(white)
            text = font.render("Добро пожаловать в мою игру!",True,black)
            screen.blit(text, [50,100])
            text = font.render("Цель игры - набрать сто душ и не столкнутся с ангелочком.",True,black)
            screen.blit(text, [50,200])
            text = font.render("Для управления используются клавиши W,S,A,D ",True,black)
            screen.blit(text, [50,300])
            text = font.render("Для запуска игры нажмите пробел.",True,black)
            screen.blit(text, [50,400])
        elif iteration >= 1 and win==False:
            screen.fill(black)
            text = font.render("Вы проиграли",True,white)
            screen.blit(text, [50,100])
            text = font.render("Вы смогли набрать только "+str(score)+" душ.",True,white)
            screen.blit(text, [50,200])
            text = font.render("Не отчаивайтесь, в следущий раз вы сможете набрать 100 душ.  ",True,white)
            screen.blit(text, [50,300])
            text = font.render("Для того чтобы сделать еще одну попытку, нажмите пробел.",True,white)
            screen.blit(text, [50,400])
        for i in pygame.event.get():    #Проверка произошедшего события, не важно какое
            if i.type==pygame.QUIT:
                    pygame.quit()       #Вырубает пайгем
                    sys.exit()          #Вырубает цикл
            if i.type==pygame.KEYDOWN:
                """Если нажимаем пробел то происходит запуск самой игры путем выключения этого цикла и включения игрового цикла"""
                if i.key==pygame.K_SPACE:
                    done=False
                    make=True
                    score=0
        """Обновление экрана, отчиска уровня от ангелов и душ, возврат гг в исходную точку"""
        pygame.display.update()
        pygame.sprite.Group.empty(angels)
        pygame.sprite.Group.empty(souls)
        avt=avatar(devil,400,300,10)
    while not(done):
        win=False
        for i in pygame.event.get():
            if i.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        avt._move(i)                    #Осуществляет движение
        screen.blit(background, (0, 0))
        screen.blit(avt.image, avt.rect) #Отрисовывает самое изображени в определенных координатах
        if i.type== pygame.USEREVENT:    #Если проходит две секунды то спаунятся души и ангелы
            soul(randint(25,W-25),randint(25,W-25),
            souls_surfase[0],souls)
            angel(20,randint(25,W-25),
            angels_surfase[0],angels)
        souls.draw(screen)              #Отрисовка группы душ
        angels.draw(screen)             #Отрисовка группы Ангелов
        souls.update()                  #Обновления душ
        angels.update()                 #Обновления Ангелов
        if pygame.sprite.spritecollide(avt, souls, True):  #Проверка столкнований
            score+=1
            sound1.play()
            if score >=100:
                text = font.render("ВЫ ПОБЕДИЛИ "+ str(score),True,white)
                screen.blit(text, [400,400])
                done=True
                make=False
                win=True
                sound3.play()
        if pygame.sprite.spritecollide(avt, angels, True):
            sound2.play()
            text = font.render("Вы проиграли",True,black)
            screen.blit(text, [400,400])
            done=True
            make=False
            iteration+=1
        text = font.render("Ваш счет = "+ str(score)+" душ",True,white)
        screen.blit(text, [10,10])
        pygame.display.update()         #Обновления экрана
        clock.tick(60)                  #Фпс
