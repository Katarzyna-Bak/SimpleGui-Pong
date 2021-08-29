# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
#canvas size
WIDTH = 600
HEIGHT = 400       

#initial direction
LEFT = False
RIGHT = True

#ball parameters
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 1]
BALL_RADIUS = 20

#scores
score1 = 0
score2 = 0

#paddles
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    x = random.randrange(120, 240) / 100
    y = (-1) * random.randrange(60, 180) / 100
    
    if direction == RIGHT:
        ball_vel = [x, y]
    elif direction == LEFT:
        ball_vel = [-x, y]
    
    return ball_pos, ball_vel

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos  # these are numbers
    global score1, score2  # these are ints
    
    #check direction
    if LEFT:
        spawn_ball(LEFT)
    elif RIGHT:
        spawn_ball(RIGHT)
    
    #reset results
    paddle1_pos_center = HEIGHT / 2
    paddle2_pos_center = HEIGHT / 2
    score1 = 0
    score2 = 0
    
    return paddle1_pos_center, paddle2_pos_center, score1, score2

def reset():
    new_game()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 10, 'Orange', 'Orange')
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos <= HEIGHT - PAD_HEIGHT and paddle1_vel > 0) or (paddle1_pos >= 0 and paddle1_vel < 0):
        paddle1_pos += paddle1_vel 
    elif (paddle2_pos <= HEIGHT - PAD_HEIGHT and paddle2_vel > 0) or (paddle2_pos >= 0 and paddle2_vel < 0):
        paddle2_pos += paddle2_vel 
        
    #keep ball on the screen - vertical borders
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    # check if the ball touched horizontal borders, trigger score change and spawn_ball
    # and determine whether paddle and ball collide, if yes, increase ball_vel by 10%
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH) or ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):                
        if (ball_pos[0] > WIDTH / 2):             
            if (ball_pos[1] < paddle2_pos) or (ball_pos[1] > paddle2_pos + PAD_HEIGHT):
                score1 += 1 
                spawn_ball(LEFT) 
            else:
                ball_vel[0] = -1.1 * ball_vel[0]
            
        if (ball_pos[0] < WIDTH / 2):
            if (ball_pos[1] < paddle1_pos) or (ball_pos[1] > paddle1_pos + PAD_HEIGHT):
                score2 += 1
                spawn_ball(RIGHT)
            else:
                ball_vel[0] = -1.1 * ball_vel[0]

    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos], [HALF_PAD_WIDTH, paddle1_pos+PAD_HEIGHT], PAD_WIDTH, 'green')
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos], [WIDTH-HALF_PAD_WIDTH, paddle2_pos+PAD_HEIGHT], PAD_WIDTH, 'blue')

    # draw scores
    canvas.draw_text(str(score1), [260, 50], 40, "green")
    canvas.draw_text(str(score2), [320, 50], 40, "blue")
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    vel = 4
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -vel
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -vel
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel
    
    return paddle1_vel, paddle2_vel
    
def keydown(key):
    pass

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keyup_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Reset the game', reset, 200)

# start frame
new_game()
frame.start()
