import pygame
import random
import socket
import pickle
import select
import time
from moviepy.editor import *


pygame.init()
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (60, 15, 236)

massege_close = b''
massege_close = pickle.dumps(massege_close)



screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('snake')
clock = pygame.time.Clock()
speed = 15  # int(input("speed?")) ####  REFRESH_RATE  #####
#font_style = pygame.font.SysFont('Comic Sans MS', 30)
font_style = pygame.font.SysFont(None, 30)



def you_die(my_socket):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data = pickle.dumps([[-10, 0]])
                my_socket.send(data)
                time.sleep(0.02)
                my_socket.send(massege_close)
                pygame.quit()
            else:
                rlist, wlist, xlist = select.select([my_socket], [], [], 0.01)
                for sock in rlist:
                    screen = pygame.display.set_mode((800, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
                    before_decode = my_socket.recv(2048)
                    print(f"before decode: {before_decode}")
                    data = pickle.loads(before_decode)
                    screen.fill(white)
                    draw_snake(data)
                data = pickle.dumps([[-10, 0]])
                my_socket.send(data)
                cool_message("you Disqualified  ", 0, 0, red)
                pygame.display.update()
                clock.tick(speed)


def movie():
    pygame.display.set_caption('loading...')
    # pygame.display.set_mode((0,0), 0, 32)
    clip = VideoFileClip('loading_screen.mp4')
    clip.preview()


def cool_message(msg, x, y, color):
    text_surface = font_style.render(msg, False, color)
    screen.blit(text_surface, (x, y))

def message(points):
    text_surface = font_style.render("score: " + str(points), False, black)
    screen.blit(text_surface, (0, 0))

def play_music():
    pygame.mixer.music.load("coin.mp3")
    pygame.mixer.music.play()

def cheak_if_hit_other(all, x_head, y_head, Length_of_snake):
    if Length_of_snake <= 2:
        return False
    tmp = []
    tmp.append(x_head)
    tmp.append(y_head)
    #print(tmp)
    if tmp in all:
        return True
    return False


def cheak_himself_gvulot(x_snake, y_snake):  ##    בדיקה אם אנחנו בגבולות
    if x_snake >= 800 or x_snake < 0 or y_snake >= 600 or y_snake < 0:
        return True
    else:
        return False


def choose_server_ip():
    first_answer = input("Do you want to play with Local server? Y - yes, N - no\r\n")
    if first_answer.lower() == "n":
        second_ans = input("please enter IP to play with: ")
        return second_ans
    return "127.0.0.1"

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, black, [x[0], x[1], 10, 10])


def THE_game():
    movie()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('snake')
    clock = pygame.time.Clock()
    my_socket = socket.socket()
    my_socket.connect((choose_server_ip(), 5555))  # change if servers run over another PC
    # my_socket.connect(("127.0.0.1", 5555))  # change if servers run over another PC
    Gamefinish = False
    x_snake = random.randrange(0, 800, 10)
    y_snake = random.randrange(0, 600, 10)
    x_food = random.randrange(20, 760, 10)
    y_food = random.randrange(20, 560, 10)

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    while not Gamefinish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data = pickle.dumps([[-10, 0]])
                my_socket.send(data)
                time.sleep(0.02)
                my_socket.send(massege_close)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 10
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -10
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 10
                    x1_change = 0

        x_snake += x1_change
        y_snake += y1_change
        if cheak_himself_gvulot(x_snake, y_snake) == True:
            you_die(my_socket)
        screen.fill(white)
        message(Length_of_snake)
        pygame.draw.rect(screen, red, [x_food, y_food, 10, 10])  ##ציור של אוכל
        snake_Head = []
        snake_Head.append(x_snake)
        snake_Head.append(y_snake)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:    #בדיקה אם אנחנו נכנסים בעצמנו
            if x == snake_Head:
                Gamefinish = True
                you_die(my_socket)

        if x_snake == x_food and y_snake == y_food:  ##בדיקה אם אנחנו במיקום של אוכל
            x_food = random.randrange(20, 760, 10)
            y_food = random.randrange(20, 560, 10)
            Length_of_snake = Length_of_snake + 1
            play_music()

        data = pickle.dumps(snake_List)
        my_socket.send(data)

        rlist, wlist, xlist = select.select([my_socket], [], [], 0.01)
        for sock in rlist:
            before_decode = my_socket.recv(2048)
            print(f"before decode: {before_decode}")
            data = pickle.loads(before_decode)
            draw_snake(data)
        tmp_X = x_snake
        tmp_Y = y_snake
        if cheak_if_hit_other(data, tmp_X, tmp_Y, Length_of_snake) == True:
            you_die(my_socket)
        if Length_of_snake < 3:
            cool_message("You -->", x_snake-70, y_snake+2, blue)
        pygame.display.update()
        clock.tick(speed)
    you_die(my_socket)


THE_game()
