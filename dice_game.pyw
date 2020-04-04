import subprocess
import sys
import pathlib
import random


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pygame")

import pygame

F_P = str(pathlib.Path(__file__).parent.absolute())

# Initialize the pygame
pygame.init()
WIDTH = 1200
HEIGHT = 800
FELT_GREEN = (10, 118, 30)

# Set Screen Dimensions and Colour
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.draw.rect(SCREEN, FELT_GREEN, (0, 0, WIDTH, HEIGHT))
pygame.display.set_caption('The Dice Game')

GAME_OVER = False

class Score():
    def __init__(self):
        self.init_score = 0
        self.current_score = 0

    def modify_score(self, player_score):
        self.current_score += player_score

    def get_score(self):
        return self.current_score

    def reset_score(self):
        self.current_score = 0

class DiceDisplay():
    def __init__(self):
        self.offset_x = 100
        self.offset_y = 200

    def x_offset_adjust(self, increment):
        self.offset_x += increment

    def y_offset_adjust(self, increment):
        self.offset_y += increment

    def return_y_offset(self):
        return self.offset_y

    def return_x_offset(self):
        return self.offset_x

    def y_offset_reset(self):
        self.offset_y = 200

    def x_offset_reset(self):
        self.offset_x = 100


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.text = text
        self.deleted = False

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x_pos-2, self.y_pos -
                                            2, self.width+4, self.height+4), 0)

        pygame.draw.rect(win, self.color, (self.x_pos, self.y_pos,
                                           self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('timesnewroman', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x_pos + (self.width/2 - text.get_width()/2),
                            self.y_pos + (self.height/2 - text.get_height()/2)))
    def delete_button(self):
        self.deleted = True

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] >= self.x_pos and pos[0] < self.x_pos + self.width and not self.deleted:
            if pos[1] >= self.y_pos and pos[1] < self.y_pos + self.height:
                return True

        return False

#initialize buttons
KEEP_ROLLING_BUTTON = Button((0, 255, 0), 10000, 50000, 375, 100, 'Click to roll again')
KEEP_SCORE = Button((0, 255, 0), 600, 50, 350, 100, 'Click to keep score')
#initialize scores
PLAYER_ONE_SCORE = Score()
CURRENT_PLAYER_ONE_SCORE = Score()
#Initialize Dice Position Manager
DICE_POS = DiceDisplay()


def total_points(dice_list):
    print_image(dice_list)
    total = 0
    # Calculates the points in any given integer array

    counter = 0
    while counter <= len(dice_list):
        if dice_list.count(counter+1) >= 3:
            if counter == 0:
                counter_2 = 0
                while counter_2 < 3:
                    counter_2 += 1
                    dice_list.remove(1)
                total = total + 1000

            elif counter == 4:
                counter_2 = 0
                while counter_2 < 3:
                    counter_2 += 1
                    dice_list.remove(5)
                total = total + 500

            else:
                total = total + 100 * (counter+1)
                counter_2 = 0
                while counter_2 < 3:
                    counter_2 += 1
                    dice_list.remove(counter+1)
        counter += 1

    while 1 in dice_list:
        total = total + 100
        dice_list.remove(1)

    while 5 in dice_list:
        total = total + 50
        dice_list.remove(5)

    return total


def print_image(dice):
    # Function to print images of dice onto SCREEN
    c_p = 0
    while c_p < len(dice):
        current_dice = pygame.image.load(F_P + "/Images/dice" + str(dice[c_p]) + ".png")
        dice_image = pygame.transform.scale(
            current_dice,
            (int(current_dice.get_width() / 2), int(current_dice.get_height() / 2)))

        SCREEN.blit(dice_image, (DICE_POS.return_x_offset(), DICE_POS.return_y_offset()))
        DICE_POS.x_offset_adjust(75)
        c_p += 1
    DICE_POS.x_offset_reset()
    DICE_POS.y_offset_adjust(75)


def to_screen(display_msg, rect_dim):
    rect_dim_list = list(rect_dim)
    rect_center = (rect_dim_list[0] + (rect_dim_list[2]/ 2), rect_dim_list[1])
    score_font = pygame.font.SysFont('timesnewroman', 40)
    score_text = score_font.render(display_msg,
                                   True, (0, 0, 0), (199, 138, 239))
    text_rect = score_text.get_rect()
    text_rect.center = rect_center
    SCREEN.blit(score_text, text_rect)


def roll_again(dice):
    r_c1 = 0
    while r_c1 < len(dice):
        dice[r_c1] = (random.randint(1, 6))
        r_c1 += 1
    print(dice)
    return total_points(dice)



START_BUTTON = Button((245, 194, 194), 450, 200, 300, 200, 'Start The Game!')
START_BUTTON.draw(SCREEN, (0, 0, 0))
TOTAL_SCORE_PLACE = (150, 700, 100, 100)
TOTAL_SCORE_POINTS = (375, 700, 100, 100)
CURRENT_SCORE_PLACE = (665, 227, 100, 100)
CURRENT_SCORE_POINTS = (860, 227, 100, 100)

while not GAME_OVER:

    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()

        if PLAYER_ONE_SCORE.get_score() >= 5000:
            pygame.draw.rect(SCREEN, FELT_GREEN, (0, 0, 1200, 800))
            pygame.draw.rect(SCREEN, (199, 138, 239), (0, 0, 1200, 800))
            to_screen("Congratulations! You Won!", (350, 200, 500, 800))

        if event.type == pygame.QUIT:
            sys.exit()
            GAME_OVER = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if START_BUTTON.is_over(mouse_pos):
                #Recreate Scene
                START_BUTTON.delete_button()
                pygame.draw.rect(SCREEN, FELT_GREEN, (0, 0, 1200, 800))
                ROLL_BUTTON = Button((0, 255, 0), 150, 50, 250, 100, 'Click To Roll')
                ROLL_BUTTON.draw(SCREEN, (0, 0, 0))

            elif KEEP_ROLLING_BUTTON.is_over(mouse_pos):
                CURR_SCORE = roll_again(dice_array)
                CURRENT_PLAYER_ONE_SCORE.modify_score(CURR_SCORE)
                to_screen(str(CURRENT_PLAYER_ONE_SCORE.get_score()), CURRENT_SCORE_POINTS)
                to_screen("Current Score:", CURRENT_SCORE_PLACE)

                if CURR_SCORE == 0:
                    #print("RAN")
                    #Delete old buttons
                    KEEP_ROLLING_BUTTON.delete_button()
                    KEEP_SCORE.delete_button()

                    #Recreate Scene
                    pygame.draw.rect(SCREEN, FELT_GREEN, (0, 0, 1200, 800))
                    CURRENT_PLAYER_ONE_SCORE.reset_score()
                    to_screen(str(PLAYER_ONE_SCORE.get_score()), TOTAL_SCORE_POINTS)
                    to_screen("Total Score:", TOTAL_SCORE_PLACE)
                    ROLL_BUTTON = Button((0, 255, 0), 150, 50, 250, 100, 'Click To Roll')
                    ROLL_BUTTON.draw(SCREEN, (0, 0, 0))

            elif KEEP_SCORE.is_over(mouse_pos):
                #print("Keep Score!!")
                #Delete old buttons
                KEEP_ROLLING_BUTTON.delete_button()
                KEEP_SCORE.delete_button()
                pygame.draw.rect(SCREEN, FELT_GREEN, (0, 0, 1200, 800))
                PLAYER_ONE_SCORE.modify_score(CURRENT_PLAYER_ONE_SCORE.get_score())
                CURRENT_PLAYER_ONE_SCORE.reset_score()
                to_screen(str(PLAYER_ONE_SCORE.get_score()), TOTAL_SCORE_POINTS)
                to_screen("Total Score:", TOTAL_SCORE_PLACE)
                ROLL_BUTTON = Button((0, 255, 0), 150, 50, 250, 100, 'Click To Roll')
                ROLL_BUTTON.draw(SCREEN, (0, 0, 0))
                dice_array = []

            elif ROLL_BUTTON.is_over(mouse_pos):
                dice_array = []
                i = 0
                # Add dice to array
                DICE_POS.y_offset_reset()
                while i < 5:
                    dice_array.append((random.randint(1, 6)))
                    i += 1
                CURRENT_PLAYER_ONE_SCORE.modify_score(total_points(dice_array))
                if CURRENT_PLAYER_ONE_SCORE.get_score() < 150:
                    CURRENT_PLAYER_ONE_SCORE.reset_score()

                if CURRENT_PLAYER_ONE_SCORE.get_score() >= 150:
                    pygame.draw.rect(SCREEN, FELT_GREEN, (140, 45, 270, 110))
                    ROLL_BUTTON.delete_button()
                    to_screen(str(PLAYER_ONE_SCORE.get_score()), TOTAL_SCORE_POINTS)
                    to_screen("Total Score:", TOTAL_SCORE_PLACE)
                    to_screen(str(CURRENT_PLAYER_ONE_SCORE.get_score()), CURRENT_SCORE_POINTS)
                    to_screen("Current Score:", CURRENT_SCORE_PLACE)
                    KEEP_ROLLING_BUTTON = Button((0, 255, 0), 100, 50, 375, 100,
                                                 'Click to keep rolling')
                    KEEP_ROLLING_BUTTON.draw(SCREEN, (0, 0, 0))
                    KEEP_SCORE = Button((0, 255, 0), 600, 50, 350, 100, 'Click to keep score')
                    KEEP_SCORE.draw(SCREEN, (0, 0, 0))

    pygame.display.update()
