# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400 # height
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80 # height for the paddles
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT_SCORE = 0
RIGHT_SCORE = 0
diff = WIDTH - PAD_WIDTH
down = True
const = 0

init_pos = [WIDTH / 2, HEIGHT / 2]
# ball_pos = [0, 0]
ball_vel = [0, 3]  # pixels per tick
time = 1


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = init_pos

    if direction == 'Right':
        ball_vel[0] = 2 #random.randrange(120, 240)
        ball_vel[1] = -2 #random.randrange(60, 180)

    elif direction == 'Left':
        ball_vel[0] = -2 #random.randrange(120, 240)
        ball_vel[1] = -2 #random.randrange(60, 180)


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 0
    paddle2_pos = 0
    paddle1_vel = 0
    paddle2_vel = 0

    spawn_ball('Right')

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, diff, paddle1_vel, paddle2_vel

    if ball_pos[1] == BALL_RADIUS or ball_pos[1] == (HEIGHT - BALL_RADIUS): # up/down bounce
        ball_vel[1] = -ball_vel[1]

    if ball_pos[0] == BALL_RADIUS or ball_pos[0] == (WIDTH - BALL_RADIUS): # up/down bounce
        ball_vel[0] = -ball_vel[0]


    if ball_pos[0] == PAD_WIDTH:
        spawn_ball('Right')

    if ball_pos[0] == (WIDTH - PAD_WIDTH):
        spawn_ball('Left')


    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] = init_pos[0] + ball_vel[0]
    ball_pos[1] = init_pos[1] + ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'White', 'White')
    # print ball_pos[0]

    # update paddle's vertical position, keep paddle on the screen
    a = paddle1_pos + paddle1_vel
    b = paddle2_pos + paddle2_vel

    if a >= 0 and a <= (HEIGHT - PAD_HEIGHT):
        paddle1_pos += paddle1_vel # vertical
        # print 'hi'

    if b >= 0 and b <= (HEIGHT - PAD_HEIGHT):
        paddle2_pos += paddle2_vel # vertical
        # print 'hi there'


    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos], [PAD_WIDTH, paddle1_pos], [PAD_WIDTH, PAD_HEIGHT + paddle1_pos], [0, PAD_HEIGHT + paddle1_pos]], 1, 'Red', 'Red')
    canvas.draw_polygon([[diff, paddle2_pos], [PAD_WIDTH + diff, paddle2_pos], [PAD_WIDTH + diff, PAD_HEIGHT + paddle2_pos], [diff, PAD_HEIGHT + paddle2_pos]], 1, 'Red', 'Red')

    global LEFT_SCORE, RIGHT_SCORE
    # determine whether paddle and ball collide
    if (ball_pos[0] == BALL_RADIUS) and (ball_pos[1] not in range(paddle1_pos, paddle1_pos + 81)):
        # ball crossed left line
        RIGHT_SCORE += 1
        print(LEFT_SCORE, RIGHT_SCORE)

    if (ball_pos[0] == WIDTH - BALL_RADIUS) and (ball_pos[1] not in range(paddle2_pos, paddle1_pos + 81)):
        # ball crossed right line
        LEFT_SCORE += 1
        print(LEFT_SCORE, RIGHT_SCORE)

    # draw scores
    canvas.draw_text(str(LEFT_SCORE) + '/' + str(RIGHT_SCORE), (300, 50), 20, 'White')


def keydown(key):
    global const, paddle1_vel, paddle2_vel
    const = 4

    # for up motion
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -const

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -const


    # for down motion
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = const

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = const

    # down = False

def keyup(key):
    global paddle1_vel, paddle2_vel, const
    const = 0

    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -const

    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -const


    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = const

    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = const

    # down = True


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
