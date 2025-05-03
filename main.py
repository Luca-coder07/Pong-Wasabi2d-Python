import wasabi2d as w2d
import random


scene = w2d.Scene()
scene.background = 'black'

# Balle 
ball = scene.layers[0].add_circle(
        radius=10, 
        color='white', 
        pos=(400, 300)
)
ball.vx = 3
ball.vy = 3

paddle_width = 10
paddle_height = 100
paddle_speed = 5

# Raquette Gauche (Joueur 1)
left_paddle = scene.layers[0].add_rect(
        width=paddle_width,
        height=paddle_height,
        pos=(30, scene.height / 2),
        color='white'
)

# Raquette Droite (Joueur 2)
right_paddle = scene.layers[0].add_rect(
        width=paddle_width,
        height=paddle_height,
        pos=(scene.width - 30, scene.height / 2),
        color='white'
)

# Scores
score_left = 0
score_right = 0
score_display_left = scene.layers[0].add_label(
        str(score_left),
        font='anonymous_pro_bold.ttf',
        fontsize=40,
        pos=(300, 550),
        color='white'
)
score_display_right = scene.layers[0].add_label(
        str(score_right),
        font='anonymous_pro_bold.ttf',
        fontsize=40,
        pos=(500, 550),
        color='white'
)

def check_collision(paddle):
    """
        Renvoie True si la balle touche la raquette
    """
    
    # Bord de la balle
    ball_left = ball.x - ball.radius
    ball_right = ball.x + ball.radius
    ball_top = ball.y + ball.radius
    ball_bottom = ball.y - ball.radius

    # Bord de la raquette
    paddle_left = paddle.x - paddle.width / 2
    paddle_right = paddle.x + paddle.width / 2
    paddle_top = paddle.y + paddle.height / 2
    paddle_bottom = paddle.y - paddle.height / 2

    return (
        ball_right > paddle_left and
        ball_left < paddle_right and
        ball_top > paddle_bottom and
        ball_bottom < paddle_top 
    )

def reset_ball():
    """
        Reinitialisation de la balle tant qu'il sort de l'école
    """
    ball.x = scene.width / 2
    ball.y = scene.height / 2
    ball.vx = random.choice([-4, 4])
    ball.vy = random.choice([-4, 4])

@w2d.event
def update(dt, keyboard):
    global score_left, score_right

    ball.x += ball.vx
    ball.y += ball.vy

    # rebond sur les murs
    if ball.y + 10 > scene.height or ball.y - 10 < 0:
        ball.vy *= -1
    #if ball.x - 10 < 0 or ball.x + 10 > scene.width:
    #    ball.vx *= -1

    # Deplacer la raquette gauche
    if keyboard.z and left_paddle.y - 50 > 0:
        left_paddle.y -= paddle_speed
        print("z touché")
    if keyboard.s and left_paddle.y + 50 < scene.height:
        left_paddle.y += paddle_speed
        print("s touché")

    # Deplacer la raquette droite
    if keyboard.up and right_paddle.y - 50 > 0:
        right_paddle.y -= paddle_speed
        print("up touché")
    if keyboard.down and right_paddle.y + 50 < scene.height:
        right_paddle.y += paddle_speed
        print("down touché")
    
    # Collision avec les raquettes 
    if check_collision(left_paddle) and ball.vx < 0:
        ball.vx *= -1
        print("Rebond vers la droite")
    if check_collision(right_paddle) and ball.vx > 0:
        ball.vx *= -1
        print("Rebond vers la gauche")

    if ball.x + ball.radius < 0:
        score_right += 1
        score_display_right.text = str(score_right)
        reset_ball()
        print("Augmentation du score de droite.\n")
        print("Reinitialisation de la balle")

    elif ball.x - ball.radius > scene.width:
        score_left += 1
        score_display_left.text = str(score_left)
        reset_ball()
        print("Augmentation du score de droite.\n")
        print("Reinitialisation de la balle")

w2d.run()


