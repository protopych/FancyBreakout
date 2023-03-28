import consts

class Rocket:
    moveStep = consts.ROCKET_SPEED
    def __init__(self):
        pass
    
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.lives = 3
        self.score = 0
    
    def left(self):
        if self.x - Rocket.moveStep >= 0:
            self.x -= Rocket.moveStep
    
    def right(self):
        if self.x + self.width + Rocket.moveStep <= consts.W:
            self.x += Rocket.moveStep
            
class Ball:
    def __init__(self):
        pass
    
    def __init__(self, x: int, y: int, color: tuple, rocket: Rocket):
        self.x = x
        self.y = y
        self.speed = 0
        self.vecX = 1
        self.vecY = -1
        self.color = color
        self.size = consts.BALL_SIZE
        self.rocket = rocket
        
    def launch(self):
        self.speed = consts.BALL_SPEED
        if self.rocket.lives < 3:
            if self.rocket.lives == 0:
                self.rocket.score = 0
                self.rocket.lives = 3
            
            self.vecX = 1
            self.vecY = -1
            self.rocket.x = consts.W/2 - consts.ROCKET_WIDTH/2
            self.rocket.y = consts.H - 2*consts.ROCKET_HEIGHT
            self.x = consts.W/2
            self.y = consts.H - 2*consts.ROCKET_HEIGHT - consts.BALL_SIZE - 2
            

    def tick(self):
        if self.speed:
            self.collision()
            self.x += self.speed * self.vecX
            self.y += self.speed * self.vecY
        
    def collision(self):
        #rocket collision
        if (self.x >= self.rocket.x and self.x <= self.rocket.x + self.rocket.width) and (self.y >= self.rocket.y - self.size and self.y < self.rocket.y):
            
            if (self.x <= self.rocket.x + self.rocket.width // 4 and self.vecX == 1) or (self.x >= self.rocket.x + self.rocket.width - self.rocket.width // 4 and self.vecX == -1):
                self.vecX *= -1
                self.vecY *= -1
            else:
                self.vecY *= -1
      
        
        #wall collision
        elif self.x <= self.size or self.x >= consts.W - self.size:
            self.vecX *= -1
        
        elif self.y <= self.speed + self.size and self.vecY == -1:
            self.vecY *= -1
            
        elif self.y >= consts.H - self.speed - self.size and self.vecY == 1:
            self.rocket.lives -= 1
            self.speed = 0

class Brick:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
    def collision(self, ball: Ball):
        if (ball.x >= self.x and ball.x <= self.x + self.width) and ball.y <= self.y - ball.size:
            ball.vecY *= -1
            return True
        
        return False
