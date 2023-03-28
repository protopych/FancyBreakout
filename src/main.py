import pygame
from entities import Rocket, Ball, Brick
import consts

bricks = []
paused = False

def screen_setup():
    consts.W, consts.H = pygame.display.Info().current_w, pygame.display.Info().current_h
    consts.SCORE_GAP = round(consts.H * 0.1)    
    consts.ROCKET_WIDTH = consts.W // 15
    consts.ROCKET_HEIGHT = consts.W // 180
    consts.BRICK_WIDTH = consts.W // 32
    consts.BRICK_HEIGHT = consts.BRICK_WIDTH // 4
    consts.BRICK_EXTRA_GAP = consts.BRICK_WIDTH // 3

def bricks_setup():
    bricks.clear()
    for i in range(8):
        for j in range(consts.BRICK_EXTRA_GAP,consts.W - consts.BRICK_EXTRA_GAP, consts.BRICK_WIDTH + consts.BALL_SIZE):
            bricks.append(Brick(j, i * consts.BRICK_WIDTH/2 + consts.SCORE_GAP, consts.BRICK_WIDTH, consts.BRICK_HEIGHT,consts.colors[i]))
            
pygame.init()
screen_setup()
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #using an invisible cursor

display_surface = pygame.display.set_mode((consts.W,consts.H))
pygame.display.set_caption('Fancy Breakout')
clock = pygame.time.Clock()

rocket = Rocket(consts.W/2 - consts.ROCKET_WIDTH/2, consts.H - 2*consts.ROCKET_HEIGHT, consts.ROCKET_WIDTH, consts.ROCKET_HEIGHT, consts.MEDIUM_BLUE)
ball = Ball(consts.W/2, consts.H - 2*consts.ROCKET_HEIGHT - consts.BALL_SIZE - 1, (255,255,255), rocket)

font = pygame.font.SysFont('arial', consts.SCORE_GAP // 2)
bricks_setup()
bricks_max_size = len(bricks)

while True:
    clock.tick(75)
    display_surface.fill((0,0,0))
    pygame.draw.rect(display_surface, rocket.color, (rocket.x, rocket.y, rocket.width, rocket.height))
    pygame.draw.rect(display_surface, ball.color, (ball.x, ball.y, ball.size, ball.size))
    #pygame.draw.line(display_surface, consts.WHITE,  (ball.x, ball.y), (ball.x + ball.vecX * ball.speed * 80, ball.y  + ball.vecY * ball.speed * 80))
    
    if not bricks or (rocket.score == 0 and len(bricks) != bricks_max_size):
        bricks_setup()
        
    for brick in bricks:
        if brick.collision(ball):
            rocket.score += 1
            bricks.remove(brick)
        else:
            pygame.draw.rect(display_surface, brick.color, (brick.x, brick.y, brick.width, brick.height))
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT] and ball.speed > 0 and not paused:
        rocket.left()
    if keys_pressed[pygame.K_RIGHT] and ball.speed > 0 and not paused:
        rocket.right()
    if keys_pressed[pygame.K_SPACE] and not paused and ball.speed == 0:
        ball.launch()
    if keys_pressed[pygame.K_ESCAPE]:
          pygame.quit()
          quit()

    if not paused:
        ball.tick()

    t1 = font.render(str(rocket.score), True,consts.S_VIOLET)
    t2 = font.render(str(rocket.lives), True,consts.S_VIOLET)
    display_surface.blit(t1,(consts.W//4, 10))
    display_surface.blit(t2,(consts.W - consts.W//4, 10))
    pygame.display.update()
    pygame.display.flip()