import pygame
import math
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode(([800, 450]), RESIZABLE)
screen_width, screen_height = [800, 450]

color2 = (255, 255, 255)
color1 = (0, 0, 0)

def draw_O(screen, x, y, radius, thickness, color=color2):
    pygame.draw.circle(screen, color, (int(round(x)), int(round(y))), int(round(radius)))
    pygame.draw.circle(screen, color1, (int(round(x)), int(round(y))), int(round(radius - thickness)))

def draw_X(screen, x, y, size, thickness, color=color2):
    pygame.draw.polygon(screen, color, [(int(round(x - size)), int(round(y - size + 2*thickness/2/math.sqrt(2)))), (int(round(x - size + 2*thickness/2/math.sqrt(2))), int(round(y - size))), (int(round(x)), int(round(y - thickness/math.sqrt(2)))), \
                                        (int(round(x + size - 2*thickness/2/math.sqrt(2))), int(round(y - size))), (int(round(x + size)), int(round(y - size + 2*thickness/2/math.sqrt(2)))), (int(round(x + thickness/math.sqrt(2))), int(round(y))), \
                                        (int(round(x + size)), int(round(y + size - 2*thickness/2/math.sqrt(2)))), (int(round(x + size - 2*thickness/2/math.sqrt(2))), int(round(y + size))), (int(round(x)), int(round(y + thickness/math.sqrt(2)))), \
                                        (int(round(x - size + 2*thickness/2/math.sqrt(2))), int(round(y + size))), (int(round(x - size)), int(round(y + size - 2*thickness/2/math.sqrt(2)))), (int(round(x - thickness/math.sqrt(2))), int(round(y)))])

def draw_grid(screen, thickness, x_min, y_min, x_max, y_max):
    #Thickness must be int

    for i in range(4):
        pygame.draw.line(screen, color2, (int(round(x_min + i*min(x_max, y_max)/3)), int(round(y_min))), (int(round(x_min + i*min(x_max, y_max)/3)), int(round(y_max))), int(round(thickness)))
    for i in range(4):
        pygame.draw.line(screen, color2, (int(round(x_min)), int(round(y_min + i*min(x_max, y_max)/3))), (int(round(x_max)), int(round(y_min + i*min(x_max, y_max)/3))), int(round(thickness)))

def get_dimensions(screen):
    x_min, y_min = [0, 0]
    x_max, y_max = [screen.get_size()[0], screen.get_size()[1]];
    grid_width = min(x_max, y_max)/3

    if (x_max < y_max):
        y_min = (y_max - x_max)/2
        y_max = x_max + (y_max - x_max)/2
    else:
        x_min = (x_max - y_max)/2
        x_max = y_max + (x_max - y_max)/2

    return [x_min, y_min, x_max, y_max, grid_width]

def update_game(screen, game):

    x_min, y_min, x_max, y_max, grid_width = get_dimensions(screen)

    draw_grid(screen, round(min(screen.get_size()[0], screen.get_size()[1])/50), x_min, y_min, x_max, y_max)

    for i, row in enumerate(game):
        for j, spot in enumerate(row):
            if spot == 0:
                draw_O(screen, x_min + (j + 0.5)*grid_width, y_min + (i + 0.5)*grid_width, grid_width*7/16, round(min(screen.get_size()[0], screen.get_size()[1])/50), (100, 100, 255))
            elif spot == 1:
                draw_X(screen, x_min + (j + 0.5)*grid_width, y_min + (i + 0.5)*grid_width, grid_width*7/16, round(min(screen.get_size()[0], screen.get_size()[1])/50), (255, 100, 100))

def click_location(x, y):

    x_min, y_min, x_max, y_max, grid_width = get_dimensions(screen)

    for i in range(3):
        for j in range(3):
            if x >= x_min + i*grid_width and x < x_min + (i + 1)*grid_width and \
               y >= y_min + j*grid_width and y < y_min + (j + 1)*grid_width:
               return [i, j]



def win(game):

    for col in game:
        if col[0] == -1:
            continue
        temp = col[0]
        iswin = True
        for spot in col:
            if spot != temp:
                iswin = False
                break
        if iswin:
            return temp

    for row in range(3):
        if game[0][row] == -1:
            continue
        temp = game[0][row]
        iswin = True
        for col in range(3):
            if game[col][row] != temp:
                iswin = False
                break
        if iswin:
            return temp

    if (game [0][0] != -1 and game[0][0] == game[1][1] and game[0][0] == game[2][2]):
        return game[0][0]

    if (game[0][2] != -1 and game[0][2] == game[1][1] and game[0][2] == game[2][0]):
        return game[0][2]

    tie = True
    for col in game:
        for spot in col:
            if spot == -1:
                tie = False
                break
        if not tie:
            break
    if tie:
        return 2

    return -1

def minimax (game, depth, player, move):
    #print("working")
    if (win(game) == move):
        return 100 - depth
    elif (win(game) == abs(move-1)):
        return -100 + depth
    elif (win(game) == 2):
        return 0



    if player == "human":
        best = 1000000000
        for i in range(3):
            for j in range(3):
                if game[i][j] == -1:
                    game[i][j] = abs(move-1)
                    best = min(minimax(game, depth + 1, "cpu", move), best)
                    game[i][j] = -1
        return best

    else:
        best = -1000000000
        for i in range(3):
            for j in range(3):
                if game[i][j] == -1:
                    game[i][j] = move
                    best = max(minimax(game, depth + 1, "human", move), best)
                    game[i][j] = -1
        return best

def cpu_move(game, move):

    #first move takes forever, so it is hard-coded
    empty = True
    for i in range(3):
        for j in range(3):
            if game[i][j] != -1:
                empty = False
                break
        if not empty:
            break

    if empty:
        return [0, 0]
    
    best = [-1000000000, [-1, -1]]

    for i in range(3):
        for j in range(3):
            if (game[i][j] == -1):
                game[i][j] = move
                temp = minimax(game, 0, "human", move)
                game[i][j] = -1
                if best[0] < temp:
                    best[0] = temp
                    best[1] = [i, j]

    return best[1]



playing = False
menu = True
running = True
winner = -1
game = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
player = 1
cpu = 0

screen.fill(color1)
draw_X(screen, screen_width/4, screen_height/2, min(screen_width/2, screen_height)/3, min(screen_width, screen_height)/25, (255, 100, 100))
draw_O(screen, screen_width*3/4, screen_height/2, min(screen_width/2, screen_height)/3, min(screen_width, screen_height)/25, (100, 100, 255))
pygame.display.update()

while running:
    update = False

    for event in pygame.event.get():

        if event.type == pygame.VIDEORESIZE:
            surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            screen_width, screen_height = [event.w, event.h]
            update = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            update = True
            click_x, click_y = event.pos

            if (not playing) and menu:
                if click_x < screen_width/2:
                    cpu = 0
                else:
                    cpu = 1
                playing = True

            elif (not playing) and (not menu):
                menu = True
                game = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
            
            elif playing and player == abs(cpu - 1):
                y, x = click_location(click_x, click_y)

                if game[x][y] == -1:
                    game[x][y] = player
                    player = abs(player - 1)

                #print(game)


        elif event.type == pygame.QUIT:
            running = False

    screen.fill(color1)
    if playing and win(game) >= 0:
        playing = False
        menu = False
        winner = win(game)
    
    if playing and player == cpu:
        move = cpu_move(game, player)
        game[move[0]][move[1]] = player
        player = abs(cpu - 1)
        update = True
        if playing and win(game) >= 0:
            playing = False
            menu = False
            winner = win(game)

    if not update:
        continue

    if not playing:
        if menu:
            draw_X(screen, screen_width/4, screen_height/2, min(screen_width/2, screen_height)/3, min(screen_width, screen_height)/25, (255, 100, 100))
            draw_O(screen, screen_width*3/4, screen_height/2, min(screen_width/2, screen_height)/3, min(screen_width, screen_height)/25, (100, 100, 255))
        else:
            update_game(screen, game)
            
            text = ""
            if winner == cpu:
                text = "You Lose"
            elif winner == 2:
                text = "Tie"
            else:
                text = "You Win"

                
            #built-in fonts look bad
            text1 = pygame.font.Font("font.ttf", round(min(screen_height, screen_width)/5)).render(text, True, (abs(color2[0]-100), abs(color2[1]-100), abs(color2[2]-100)))
            screen.blit(text1, (int(round((screen_width - text1.get_width())/2)), int(round(screen_height*2/5 - text1.get_height()/2))))

            text2 = pygame.font.Font("font.ttf", round(min(screen_height, screen_width)/10)).render("Click anywhere to continue", True, (abs(color2[0]-100), abs(color2[1]-100), abs(color2[2]-100)))
            screen.blit(text2, (int(round((screen_width - text2.get_width())/2)), int(round(screen_height*3/5 - text2.get_height()/2))))
            
    else:
        update_game(screen, game)

    pygame.display.update()

pygame.quit()
