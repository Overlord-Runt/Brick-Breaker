import pygame, random, sys, asyncio
from pygame.locals import *

pygame.init()

async def main():
    FPS = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)


    white = (255, 255, 200)
    black = (0, 0, 0)
    green = (0, 255, 0)
    darkgray = (90, 90, 90)
    darkbrown = (91, 64, 51)

    run = True


    background = pygame.display.set_mode((1000, 700))
    background.fill(white)
    pygame.display.set_caption("Brick Breaker")

    class You(pygame.sprite.Sprite):
        def __init__(self):
            self.height = 20
            self.width = 100
            self.x = 500
            self.y = 600

        def draw(self):
            pygame.draw.rect(background, darkgray, (self.x, self.y, self.width, self.height))

        def moveRight(self, pixels):
            self.x += pixels

        def moveLeft(self, pixels):
            self.x -= pixels
        

    class Bullet(pygame.sprite.Sprite):
        def __init__(self):
            self.radius = 10
            self.x = 500
            self.y = 400

        def draw(self):
            pygame.draw.circle(background, green, (self.x, self.y), self.radius)
        
        def move1(self, pixels):
            self.x += pixels
            self.y += pixels
        def move2(self, pixels):
            self.x -= pixels
            self.y += pixels
        def move3(self, pixels):
            self.x -= pixels
            self.y -= pixels
        def move4(self, pixels):
            self.x += pixels
            self.y -= pixels

    
    class Brick(pygame.sprite.Sprite):
        def __init__(self, x, y):
            self.width = 70
            self.height = 30
            self.colour = darkbrown
            self.x = x
            self.y = y
        
        def draw(self):
            pygame.draw.rect(background, self.colour, (self.x, self.y, self.width, self.height))
    
    brick_array = []
    rows = 5
    cols = 11

    for row in range(rows):
        for col in range(cols):
            x = col * (90) + 15
            y = row * (50) + 15
            brick_array.append(Brick(x, y))


    P1 = You()
    bul = Bullet()


    speed = 5
    dir = random.randint(3,4)
    bulspeed = 5
    score = 0
    r = False
    while run == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    run = False
        
        background.fill(white)
        # player movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            P1.moveLeft(speed)
        
        if keys[pygame.K_RIGHT]:
            P1.moveRight(speed)
        
        if keys[pygame.K_a]:
            P1.moveLeft(speed)

        if keys[pygame.K_d]:
            P1.moveRight(speed)

        if keys[pygame.K_SPACE]:
            speed = 30
        else:
            speed = 5
        

        # bullet movement
        if dir == 1:
            if bul.y > 690:
                run = False
            if bul.x > 990:
                dir = 2
            if 640 > bul.y > 600:
                if -10 < (bul.x - P1.x) < 110:
                    dir = 4

        elif dir == 2:
            if bul.y > 690:
                run = False
            if bul.x < 10:
                dir = 1
            if 640 > bul.y > 600:
                if -10 < (bul.x - P1.x) < 110:
                    dir = 3

        elif dir == 3:
            if bul.x < 10:
                dir = 4
            if bul.y < 10:
                dir = 2
        elif dir == 4:
            if bul.x > 990:
                dir = 3
            if bul.y < 10:
                dir = 1
        else:
            run = False

        if dir == 1:
            bul.move1(bulspeed)
        elif dir == 2:
            bul.move2(bulspeed)
        elif dir == 3:
            bul.move3(bulspeed)
        elif dir == 4:
            bul.move4(bulspeed)
        else:
            run = False
        

        #bricks
        brick_to_remove = []
        for brick in brick_array:
            if dir == 4:    
                if 25 > brick.y - bul.y > -10:
                    if 0 > brick.x - bul.x > -70:
                        brick_to_remove.append(brick)
                        dir = 1
                    elif 10 > brick.x - bul.x > -80:
                        brick_to_remove.append(brick)
                        dir = 3
            elif dir == 3:    
                if 25 > brick.y - bul.y > -10:
                    if 0 > brick.x - bul.x > -70:
                        brick_to_remove.append(brick)
                        dir = 2
                    elif 10 > brick.x - bul.x > -80:
                        brick_to_remove.append(brick)
                        dir = 4
            elif dir == 1:    
                if 25 > brick.y - bul.y > -10:
                    if 0 > brick.x - bul.x > -70:
                        brick_to_remove.append(brick)
                        dir = 4
                    elif 10 > brick.x - bul.x > -80:
                        brick_to_remove.append(brick)
                        dir = 2
            elif dir == 2:    
                if 25 > brick.y - bul.y > -10:
                    if 0 > brick.x - bul.x > -70:
                        brick_to_remove.append(brick)
                        dir = 3
                    elif 10 > brick.x - bul.x > -80:
                        brick_to_remove.append(brick)
                        dir = 1
                    
        for brick in brick_to_remove:
            if brick in brick_array:
                brick_array.remove(brick)
                score += 1
        
        for brick in brick_array:
            brick.draw()


        score_text = font.render(f"Score: {score}", True, black)
        background.blit(score_text, (10, 660))


        if score == 55:
            r = True
            run = False
        else:
            r = False
        bul.draw()
        P1.draw()
        pygame.display.update()
        FPS.tick(60)
        await asyncio.sleep(0)
    if r == True:
        over_text = font.render(f"You Win!!!", True, black)
        background.blit(over_text, (420, 300))
    else:
        over_text = font.render(f"Game Over!!!", True, black)
        background.blit(over_text, (400, 300))
    pygame.display.update()
    pygame.time.delay(2000)

asyncio.run(main())
        



