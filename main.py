import pygame as pg
import random
import sys
import time
import colors as Col
"""I'm gonna try code a blackjack game with only functions, without using pygame sprites, """

# Initalize the pygame and prepare screen
pg.init()
WIDTH, HEIGHT = SCSIZE = (960, 540)
screen = pg.display.set_mode(SCSIZE)
pg.display.set_caption("BlankJack")
BG_COLOR = Col.indigo
screen.fill(BG_COLOR)
pg.display.flip()
CARD_WIDTH, CARD_HEIGHT = (120,200)
CARD_SPACING = 20
FONT_NAME = ''
FONT_SIZE = 60
SCORE_FONT_SIZE = 30
SCORE_FONT_NAME = FONT_NAME
PLAYER_NAME = 'player'
OPPONENT_NAME = 'opponent'


def splash():
    pass
def calc(l):
    # return sum(l)
    isblackjack = False
    if len(l) == 2 and 1 in l and 20 in l:
        isblackjack = True
    var = [0]
    for i in l:
        if i != 1:
            var = [i+j for j in var]
        elif i==1:
            var = [1+j for j in var] + [21+j for j in var]
    for ver in sorted(var,reverse=True):
        if ver <= 21:
            return ver, isblackjack
    return sum(l), isblackjack # is this needed?

def draw_rect(screen,*coords):
    """ Draw a card rectangle onto screen """
    x, y = coords
    width, height = CARD_WIDTH+2, CARD_HEIGHT+2 # Why even use w and h may change
    draw_rect = pg.Rect((x,y), (width, height))
    pg.draw.rect(screen, Col.neon_red_light, draw_rect, width=3)
    pg.draw.rect(screen, Col.neon_red_dark, draw_rect, width=1)
    return draw_rect
def draw_card(screen, card_type: str, *coords) -> pg.Rect:
    """ Draw a card a number in it """
    font = pg.font.SysFont(FONT_NAME, FONT_SIZE)
    rendered = font.render(str(card_type),True,Col.red)
    my_rect = rendered.get_rect()
    rect = draw_rect(screen, *coords)
    my_rect.center = rect.center
    screen.blit(rendered, my_rect)
    return my_rect

def draw_n_card(screen, cards: iter, y=20) -> pg.Rect:
    """ Draw n cards to screen for player and opponent[?] with spacing
        cards --> list that contains
    """
    n = len(cards)
    width = n * CARD_WIDTH+ (n-1) * CARD_SPACING
    rect_list = list()

    startx = (WIDTH-width)//2
    sp = CARD_SPACING + CARD_WIDTH
    for i,card in enumerate(cards):
        rect_of = draw_card(screen, str(card), sp*i+startx, y)
        rect_list.append(rect_of)
    return rect_list
def draw_card_player(screen, cards: iter):
    """ Draws the players card list """
    y = HEIGHT - CARD_HEIGHT - 20
    rect_list = draw_n_card(screen, cards, y)
    return rect_list
def draw_card_opponent(screen, cards: iter):
    """ Draws the opponents card list """
    rect_list = draw_n_card(screen, cards)
    return rect_list

def play_opponent(loc, lis):
    """ Opponent ai
            loc: list --> list of cards op have
            lis: list --> list can be used to add new character
    """
    print('Hi i\'m a opponent play ')
    sco, isblackjack = calc(loc)
    if sco < 17:
        print('And it is less than 17')
        return loc + [lis.pop()],True
    else:
        return loc, False

def who_wins(l1, l2, i=False):
    """
        l1: list of cards player have
        l2: list of cards opponent have
        i: bool?
    """
    s1, is_p = calc(l1)
    s2, is_o = calc(l2)

    player = 'Player'
    opponent = 'Opponent'
    draw = 'Draw'
    if is_p or is_o: # Blackjack probabilities
        if is_p == is_o:
            return draw
        if is_p:
            return player
        if is_o:
            return opponent
    if s1 == 21:
        if s1 == s2:
            return draw
        return player
    elif s2 == 21:
        if s2 == s1:
            return draw
        return opponent
    elif s2 > 21 and s1 < 21:
        return player
    elif s1 > 21 and s2 < 21:
        return opponent
    if i:
        if s1 > s2:
            return player
        elif s1 == s2:
            return draw
        else:
            return opponent
    return False
def shuffle_cards():
    return [1,2,3,4,4,4,20,20,1,1,1,1,1,1,1,13,2,2,3,5,4,12,4,5,3,6,12,15]
def draw_scores(screen, player, opponent):
    """ Draws player and opponent scores onto screen
            screen: pygame Surface
            player: integer score of player
            opponent: integer score of opponent
    """
    col = Col.neon_red_light
    midx = WIDTH // 2
    midy = HEIGHT // 2
    font = pg.font.SysFont(SCORE_FONT_NAME, SCORE_FONT_SIZE)
    p_name = font.render(PLAYER_NAME, True, col)
    o_name = font.render(OPPONENT_NAME, True, col)
    p_x = midx - CARD_SPACING
    o_x = midx + CARD_SPACING

    p_rect = p_name.get_rect()
    o_rect = o_name.get_rect()
    p_rect.right = p_x
    p_rect.centery = midy
    o_rect.left = o_x
    o_rect.centery = midy

    ps_name = font.render(str(player), True, col)
    os_name = font.render(str(opponent), True, col)

    ps_rect = ps_name.get_rect()
    os_rect = os_name.get_rect()

    ps_rect.right = p_rect.left - CARD_SPACING
    os_rect.left = o_rect.right + CARD_SPACING
    ps_rect.centery = midy
    os_rect.centery = midy

    screen.blit(p_name, p_rect)
    screen.blit(o_name, o_rect)
    screen.blit(ps_name, ps_rect)
    screen.blit(os_name, os_rect)
    return [o_rect, p_rect, ps_rect, os_rect]
def print_winner(screen, winner):
    print(winner)
def game():
    # Variables
    list_of_cards = shuffle_cards()
    list_of_cards_pl = list()
    list_of_cards_op = list()
    player_ended = False
    wins = False

    list_of_cards_pl = [list_of_cards.pop(), list_of_cards.pop()]
    list_of_cards_op = [list_of_cards.pop(), list_of_cards.pop()]
    # Main Game Loop
    while True:
        rect_list = list()
        # Handle keys(input)
        for event in pg.event.get():
            if event.type == pg.QUIT: # Exit if pressed x
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    # Exit if pressed esc
                    sys.exit()
                if event.key == pg.K_SPACE and not player_ended:
                    list_of_cards_pl.append(list_of_cards.pop())
                if event.key == pg.K_e:
                    player_ended = True
                    if calc(list_of_cards_pl)[0] > 21:
                        wins = OPPONENT_NAME
                    if wins:
                        player_ended = False
        # Update
        if player_ended:
            list_of_cards_op, player_ended = play_opponent(list_of_cards_pl,list_of_cards)
            time.sleep(1) # Wait a little bit
            if calc(list_of_cards_op)[0] > 21:
                wins = PLAYER_NAME
        if not wins and not player_ended:
            wins = who_wins(list_of_cards_pl, list_of_cards_op)
        elif wins:
            print_winner(screen, wins)
            list_of_cards_pl = [list_of_cards.pop() for _ in range(2)]
            list_of_cards_op = [list_of_cards.pop() for _ in range(2)]
            player_ended = False
            wins = False
            # Reset everything
        # Check if anyone wins
        player_score = calc(list_of_cards_pl)[0]
        opponent_score = calc(list_of_cards_op)[0]

            # reset everything
        # Remove the screen
        screen.fill(BG_COLOR)
        # Blit the screen
        draw_card_player(screen, list_of_cards_pl)
        draw_card_opponent(screen, list_of_cards_op)
        pg.draw.line(screen,Col.red, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        draw_scores(screen, player_score, opponent_score)

        # Paint the screen(!!!use dirty rect)
        rect_list.append(None)
        pg.display.update()#rect_list)
def end():
    return False


if __name__ == "__main__":
    isplaying = True
    while isplaying:
        splash()
        game()
        isplaying = end()
