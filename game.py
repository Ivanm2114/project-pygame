import pygame
import sys
import os
from copy import deepcopy, copy

FPS = 50

# Функции
# //////////////////////////////////


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def save_result(result):
    global volume
    file = open('data\\saves.txt', 'r+', encoding='utf-8')

    d = {}
    for line in file.readlines():
        line = line.replace('\n', '')
        if line:
            name, score = line.split(';')
            d[name] = int(score)

    intro_text = ["Сохранение",
                  "",
                  "Введите  желаемый  номер",
                  '',
                  '']

    arrows = ['↑      ↑      ↑',
              '',
              '↓      ↓      ↓']

    menu = ['В главное меню',
            'Выйти']

    number = [0, 0, 0]

    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    font = pygame.font.SysFont('arial', 30)
    pixfont = pygame.font.Font('data\\font.otf', 20)
    pixfont2 = pygame.font.Font('data\\font.otf', 43)
    pixfont3 = pygame.font.Font('data\\font.otf', 25)
    count = 0
    text_coord = 50
    flag = False

    while True:
        x, y = pygame.mouse.get_pos()
        text_coord = 100
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        for line in intro_text:
            string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for line in arrows:
            string_rendered = font.render(line, 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont2.render(' '.join(map(str, number)), 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord - 100
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        for line in menu:
            string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 20
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont3.render('Сохранить', 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 350
        intro_rect.x = 175
        screen.blit(string_rendered, intro_rect)

        if flag:
            text = ['Этот номер уже используется',
                    'Хотите перерзаписать результат?',
                    'Да                    Нет']
            a = 400
            for line in text:
                string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = a
                a += 20
                intro_rect.x = 150
                screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 50 and 300 < y < 336:
                number[0] += 1
                number[0] %= 10
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 51 < x < 101 and 300 < y < 336:
                number[1] += 1
                number[1] %= 10
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 102 < x < 150 and 300 < y < 336:
                number[2] += 1
                number[2] %= 10
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 50 and 411 < y < 447:
                number[0] -= 1
                number[0] = abs(number[0] % 10)
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 51 < x < 101 and 411 < y < 447:
                number[1] -= 1
                number[1] = abs(number[1] % 10)
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 102 < x < 150 and 411 < y < 447:
                number[2] -= 1
                number[2] = abs(number[2] % 10)
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 150 < x < 185 and 440 < y < 466 and flag:
                d[''.join(map(str, number))] = result
                d = d.items()
                file.seek(0)
                file.truncate()
                for el in sorted(d, key=lambda x: x[1], reverse=True):
                    file.write(';'.join(map(str, el)) + '\n')
                file.close()
                main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and 381 < x < 426 and 440 < y < 466:
                flag = False
            elif event.type == pygame.MOUSEBUTTONDOWN and 175 < x < 333 and 350 < y < 388:
                flag = False
                if ''.join(map(str, number)) not in d:
                    d[''.join(map(str, number))] = result
                    d = d.items()
                    file.seek(0)
                    file.truncate()
                    for el in sorted(d, key=lambda x: x[1], reverse=True):
                        file.write(';'.join(map(str, el)) + '\n')
                    file.close()
                    main_menu()
                else:
                    flag = True
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 211 and 523 < y < 549:
                main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 89 and 569 < y < 595:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def show_results():
    global volume
    file = open('data\\saves.txt', 'r+', encoding='utf-8')

    d = {}
    count = 0
    for line in file.readlines():
        line = line.replace('\n', '')
        if line and count < 10:
            name, score = line.split(';')
            d[name] = int(score)
            count += 1
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    pixfont = pygame.font.Font('data\\font.otf', 20)
    count = 0
    text_coord = 50
    flag = False

    while True:
        x, y = pygame.mouse.get_pos()
        text_coord = 100
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        for el in d:
            string_rendered = pixfont.render(str(el), 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 10
            screen.blit(string_rendered, intro_rect)

            string_rendered = pixfont.render(str(d[el]), 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.top = text_coord
            intro_rect.x = 200
            screen.blit(string_rendered, intro_rect)

            text_coord += 25

        string_rendered = pixfont.render('Код игрока    Очки', 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont.render('Выйти в главное меню', 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 450
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 300 and 450 < y < 476:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def controls_screen():
    intro_text = ['Управление', '', '', '', '', '',
                  "Стрелочки", "управление персонажем", '',
                  '-/=', 'понижение/повышение уровня громкости']

    pixfont = pygame.font.Font('data\\font.otf', 20)
    pixfont2 = pygame.font.Font('data\\font.otf', 43)
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

    r1, g1 = 0, 0
    flag = True

    while True:
        if r1 < 255 and flag:
            r1 += 1
            g1 += 1
        elif r1 == 255 and flag:
            flag = False
        elif 0 < r1 <= 255 and not flag:
            r1 -= 1
            g1 -= 1
        elif r1 == 0:
            flag = True

        text_coord = -9
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        for line in intro_text:
            string_rendered = pixfont.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont.render('Нажмите любую кнопку чтобы продолжить', 1, pygame.Color(r1, g1, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 570
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.flip()
        clock.tick(300)


def main_menu():
    global volume
    intro_text = ["Играть",
                  "Управление",
                  "Таблица лидеров",
                  "Выйти"]

    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
    count = 0
    pixfont = pygame.font.Font('data\\font.otf', 20)
    pixfont2 = pygame.font.Font('data\\font.otf', 43)

    r, g, b = 0, 0, 0
    pygame.mixer.music.load('data\\menu.mp3')
    pygame.mixer.music.play()

    while True:
        x, y = pygame.mouse.get_pos()

        if r != rainbow[count][0]:
            if r > rainbow[count][0]:
                r -= 1
            elif r < rainbow[count][0]:
                r += 1
        if g != rainbow[count][1]:
            if g > rainbow[count][1]:
                g -= 1
            elif g < rainbow[count][1]:
                g += 1

        if b != rainbow[count][2]:
            if b > rainbow[count][2]:
                b -= 1
            elif b < rainbow[count][2]:
                b += 1
        if (r, g, b) == rainbow[count]:
            count += 1
            count = count % 7

        text_coord = 150
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        string_rendered = pixfont2.render("Меню", 1, pygame.Color(r, g, b))

        intro_rect = string_rendered.get_rect()
        intro_rect.top = 50
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        for line in intro_text:
            string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 95 and 160 < y < 186:
                gaming()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 156 and 196 < y < 222:
                controls_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 233 and 232 < y < 258:
                show_results()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 89 and 268 < y < 294:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def start_screen(screen, width, height, clock):
    intro_text = ["Здравствуйте", "",
                  "Добро пожаловать в"]

    pixfont = pygame.font.Font('data\\font.otf', 20)
    pixfont2 = pygame.font.Font('data\\font.otf', 43)
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
    text_coord = 50

    r1, g1 = 0, 0
    flag = True

    while True:
        if r1 < 255 and flag:
            r1 += 1
            g1 += 1
        elif r1 == 255 and flag:
            flag = False
        elif 0 < r1 <= 255 and not flag:
            r1 -= 1
            g1 -= 1
        elif r1 == 0:
            flag = True

        text_coord = 100
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        for line in intro_text:
            string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont2.render('PACMAN', 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 250
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont.render('Нажмите любую кнопку чтобы продолжить', 1, pygame.Color(r1, g1, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 450
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                info_screen(screen, width, height, clock)

        pygame.display.flip()
        clock.tick(300)


def info_screen(screen, width, height, clock):
    intro_text = ["Ваша цель", "набрать как можно больше очков", "", "",
                  "Остерегайтесь призраков", "они опасны"]

    pixfont = pygame.font.Font('data\\font.otf', 20)
    pixfont2 = pygame.font.Font('data\\font.otf', 43)
    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]

    r1, g1 = 0, 0
    flag = True

    while True:
        if r1 < 255 and flag:
            r1 += 1
            g1 += 1
        elif r1 == 255 and flag:
            flag = False
        elif 0 < r1 <= 255 and not flag:
            r1 -= 1
            g1 -= 1
        elif r1 == 0:
            flag = True

        text_coord = -9
        screen.fill(pygame.Color("black"))
        screen.blit(fon, (300, 0))
        for line in intro_text:
            string_rendered = pixfont.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        string_rendered = pixfont.render('Нажмите любую кнопку чтобы продолжить', 1, pygame.Color(r1, g1, 0))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = 570
        intro_rect.x = 10
        screen.blit(string_rendered, intro_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.flip()
        clock.tick(300)


def end_screen(screen, width, height, clock):
    global volume
    end_text = ["КОНЕЦ ИГРЫ", "",
                "Ваш результат:",
                str(player.get_score()),
                'Новая игра',
                'Сохранить результат',
                'В главное меню',
                'Выйти']

    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
    pixfont = pygame.font.Font('data\\font.otf', 20)
    count = 0
    text_coord = 50

    r, g, b = 0, 0, 0

    screen.fill(pygame.Color("black"))
    screen.blit(fon, (300, 0))
    for line in end_text:
        string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pygame.mixer.music.load('data\\game over.mp3')
    pygame.mixer.music.play()

    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 152 and 204 < y < 230:
                gaming()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 279 and 240 < y < 268:
                save_result(player.get_score())
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 89 and 312 < y < 338:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 211 and 276 < y < 302:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def win_screen(screen, width, height, clock):
    global volume
    end_text = ["ПОБЕДА", "",
                "Ваш результат:",
                str(player.get_score()),
                'Новая игра',
                'Сохранить результат',
                'В главное меню',
                'Выйти']

    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    rainbow = [(255, 0, 0), (255, 125, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
    pixfont = pygame.font.Font('data\\font.otf', 20)
    count = 0
    text_coord = 50

    r, g, b = 0, 0, 0

    pygame.mixer.music.load('data\\win.mp3')
    pygame.mixer.music.play()

    screen.fill(pygame.Color("black"))
    screen.blit(fon, (300, 0))
    for line in end_text:
        string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 152 and 204 < y < 230:
                gaming()
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 279 and 240 < y < 268:
                save_result(player.get_score())
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 89 and 312 < y < 338:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN and 10 < x < 211 and 276 < y < 302:
                main_menu()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def chose_level():
    global volume
    end_text = ["ВЫБОР УРОВНЯ"]

    fon = pygame.transform.scale(load_image('fon.png'), (500, 500))
    screen.blit(fon, (300, 0))
    pixfont = pygame.font.Font('data\\font.otf', 20)
    text_coord = 0

    r, g, b = 0, 0, 0

    screen.fill(pygame.Color("black"))
    screen.blit(fon, (300, 0))
    for line in end_text:
        string_rendered = pixfont.render(line, 1, pygame.Color(255, 255, 0))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pic1 = pygame.transform.scale(load_image('map1.png'), (200, 150))
    screen.blit(pic1, (0, 50))
    string_rendered = pixfont.render('level 1', 1, pygame.Color(255, 255, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 200
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    pic2 = pygame.transform.scale(load_image('map2.png'), (200, 150))
    screen.blit(pic2, (0, 230))
    string_rendered = pixfont.render('level 2', 1, pygame.Color(255, 255, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 380
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    pic3 = pygame.transform.scale(load_image('map3.png'), (200, 150))
    screen.blit(pic3, (0, 410))
    string_rendered = pixfont.render('level 3', 1, pygame.Color(255, 255, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 560
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    pic4 = pygame.transform.scale(load_image('map4.png'), (200, 150))
    screen.blit(pic4, (0, 600))
    string_rendered = pixfont.render('level 4', 1, pygame.Color(255, 255, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 750
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and 0 < x < 200 and 50 < y < 210:
                return 'map1.txt'
            elif event.type == pygame.MOUSEBUTTONDOWN and 0 < x < 200 and 230 < y < 390:
                return 'map2.txt'
            elif event.type == pygame.MOUSEBUTTONDOWN and 0 < x < 200 and 410 < y < 570:
                return 'map3.txt'
            elif event.type == pygame.MOUSEBUTTONDOWN and 0 < x < 200 and 600 < y < 760:
                return 'map4.txt'
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)

        pygame.display.flip()
        clock.tick(300)


def load_level(filename):
    if filename:
        filename = "data/" + filename
    else:
        print('Файл не найден')
        pygame.quit()
        sys.exit(0)
    # читаем уровень, убирая символы перевода строки
    try:
        with open(filename, 'r') as mapFile:
            if mapFile:
                level_map = [[sym for sym in line.strip()] for line in mapFile]
    except:
        print('Файл не найден')
        pygame.quit()
        sys.exit(0)

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    return level_map


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('point', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == 'p':
                Tile('empty', x, y)
            elif level[y][x].isdigit():
                Tile('point', x, y)
                enemies.append(Enemy(x, y, int(level[y][x])))

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y, level


# Классы
# //////////////////////////////////////////////////////////


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.data = ['pacman1.png', 'pacman2.png']
        self.count = 0
        self.score = 0
        self.image = load_image(self.data[self.count])
        self.x = pos_x
        self.y = pos_y
        self.dist = 'r'
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, event, level_x, level_y):

        if event.key == pygame.K_RIGHT:
            self.dist = 'r'
        elif event.key == pygame.K_LEFT:
            self.dist = 'l'
        elif event.key == pygame.K_UP:
            self.dist = 'u'
        elif event.key == pygame.K_DOWN:
            self.dist = 'd'

        if event.key == pygame.K_RIGHT and level[self.y % (level_y + 1)][(self.x + 1) % (level_x + 1)] != '#':
            self.x = (self.x + 1) % (level_x + 1)
        elif event.key == pygame.K_LEFT and level[self.y % (level_y + 1)][(self.x - 1) % (level_x + 1)] != '#':
            self.x = (self.x - 1) % (level_x + 1)
        elif event.key == pygame.K_UP and level[(self.y - 1) % (level_y + 1)][self.x % (level_x + 1)] != '#':
            self.y = (self.y - 1) % (level_y + 1)
        elif event.key == pygame.K_DOWN and level[(self.y + 1) % (level_y + 1)][self.x % (level_x + 1)] != '#':
            self.y = (self.y + 1) % (level_y + 1)

        self.rect.x = self.x * tile_width
        self.rect.y = self.y * tile_width

        if level[self.y][self.x] == '.' or level[self.y][self.x].isdigit():
                Tile('empty', self.x, self.y)
                level[self.y][self.x] = 'p'
                self.score += 10

    def get_score(self):
        return self.score

    def get_coords(self):
        return (self.x, self.y)

    def change_sprite(self):
        self.count += 1

        if self.count > 100:
            self.count = 0
        elif self.count > 0 and self.count < 50:
            if self.dist == 'l':
                self.image = pygame.transform.flip(load_image(self.data[0]), True, False)
            elif self.dist == 'u':
                self.image = pygame.transform.rotate(load_image(self.data[0]), 90)
            elif self.dist == 'd':
                self.image = pygame.transform.rotate(load_image(self.data[0]), -90)
            else:
                self.image = load_image(self.data[0])
        elif self.count > 50:
            if self.dist == 'l':
                self.image = pygame.transform.flip(load_image(self.data[1]), True, False)
            elif self.dist == 'u':
                self.image = pygame.transform.rotate(load_image(self.data[1]), 90)
            elif self.dist == 'd':
                self.image = pygame.transform.rotate(load_image(self.data[1]), -90)
            else:
                self.image = load_image(self.data[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, pic):
        super().__init__(enemy_group, all_sprites)
        self.data = [f'ghost{pic}.png', 'sick.png']
        self.pic = pic
        self.image = load_image(self.data[0])
        self.x = pos_x
        self.y = pos_y
        self.count = 0
        self.dist = 'r'
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        if self.count == 0:
            self.find_path(screen)
            self.rect.x = self.x * tile_width
            self.rect.y = self.y * tile_width
            self.count += 1
        else:
            self.count += 1
            self.count %= 50

    def get_coords(self):
        return (self.x, self.y)

    def find_path(self, screen):
            start_cell = (self.x, self.y)
            end_cell = player.get_coords()
            self.way(start_cell, end_cell, screen)

    def way(self, start_cell, end_cell, screen):

        def cell_in_board(i, j):
            return (i >= 0 and i < len(level) and j >= 0 and j < len(level[0]))

        field = []
        for row in range(len(level)):
            field.append([])
            for i in range(len(level[row])):
                if level[row][i] != '#':
                    field[row].append('')
                elif level[row][i] == '#':
                    field[row].append('b')
        d = 0
        field[self.y][self.x] = d
        prev_field = []

        arr = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        while field[end_cell[1]][end_cell[0]] == '' and prev_field != field:
            prev_field = deepcopy(field)
            for i in range(len(level)):
                for j in range(len(level[0])):
                    if cell_in_board(i, j):
                        if field[i][j] == d:
                            for el in arr:
                                dx, dy = list(el)
                                if cell_in_board(i + dy, j + dx):
                                    if field[i + dy][j + dx] == '' and (dy != 0 or dx != 0):
                                        field[i + dy][j + dx] = d + 1

            d += 1

        if field[end_cell[1]][end_cell[0]] != '':
            self.path = []
            current = (end_cell[0], end_cell[1])
            self.path.insert(0, (end_cell[0], end_cell[1]))
            while current != start_cell:
                for el in arr:
                    dx, dy = list(el)
                    if cell_in_board(current[1] + dy, current[0] + dx):
                        if field[current[1] + dy][current[0] + dx] == d - 1:
                            current = (current[0] + dx, current[1] + dy)
                            self.path.insert(0, current)
                            break
                d -= 1

            flag = True
            for el in enemy_group:
                coords = el.get_coords()
                if coords:
                    if el.get_coords() == (self.path[1][0], self.path[1][1]):
                        flag = False
            if flag:
                if self.path[1][0] < self.x:
                    self.dist = 'l'
                else:
                    self.dist = 'r'
                self.change_sprite()
                self.x = self.path[1][0]
                self.y = self.path[1][1]

    def change_sprite(self, mode=0):
        if not mode:
            if self.dist == 'r':
                self.image = load_image(self.data[0])
            else:
                self.image = pygame.transform.flip(load_image(self.data[0]), True, False)


def gaming():
    global player, all_sprites, tiles_group, player_group, enemy_group, level, screen, volume

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    pixfont = pygame.font.Font('data\\font.otf', 20)
    map_name = chose_level()
    player, level_x, level_y, level = generate_level(load_level(map_name))

    running = True

    pygame.mixer.music.load('data\\game.mp3')
    pygame.mixer.music.play()

    while running:
        if pygame.sprite.spritecollideany(player, enemy_group):
            end_screen(screen, width, height, clock)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                for player in player_group:
                    player.update(event, level_x, level_y)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_EQUALS:
                volume += 0.1
                if volume > 1:
                    volume = 1
                pygame.mixer.music.set_volume(volume)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_MINUS:
                volume -= 0.1
                if volume < 0.1:
                    volume = 0.1
                pygame.mixer.music.set_volume(volume)
        flag = True
        for i in range(len(level)):
            for j in range(len(level[0])):
                if level[i][j] == '.':
                    flag = False
        if flag:
            win_screen(screen, width, height, clock)
        player.change_sprite()
        enemy_group.update()
        screen.fill(pygame.Color("black"))
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        clock.tick(FPS)

        string_rendered = pixfont.render(f'Your score: {str(player.get_score())}', 1, pygame.Color('yellow'))
        rect = string_rendered.get_rect()
        text_coord = 700
        rect.top = text_coord
        rect.x = 10
        screen.blit(string_rendered, rect)

        pygame.display.flip()


# Программа
# ///////////////////////////////////////////////////////////
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

enemies = []

tile_images = {
    'wall': load_image('block.png'),
    'empty': load_image('path.png'),
    'point': load_image('point.png')

}


pygame.mixer.init(48000, -16, 2)
pygame.mixer.music.load('data\\intro.mp3')
pygame.mixer.music.play()
volume = 1

tile_width = tile_height = 30

size = width, height = 810, 810
pygame.font.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
start_screen(screen, width, height, clock)


pygame.quit()
