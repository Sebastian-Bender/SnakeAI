import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [(0, 0)]
        self.direction = down
        self.color = (10, 10, 10)

        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)

        if (new[0] == 0 and self.direction == right) or (new[1] == 0 and self.direction == down) or (new[0] == 460 and self.direction == left) or (new[1] == 460 and self.direction == up):
            self.reset()
        elif len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(0, 0)]
        self.direction = down
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
            c = self.color
            if p == self.get_head_position():
                c = (75, 100, 100)
            pygame.draw.rect(surface, c, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def controls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)
    
    def hamiltonian_cycle(self):
        if self.get_head_position()[1] == 0 and self.get_head_position()[0] == 460:
            self.turn(left)
        elif (self.get_head_position()[1] == 20 and self.direction != up) or (self.get_head_position() == (0, 0)):
            self.turn(down)
        elif self.get_head_position()[1] == 460 and self.direction != down:
            self.turn(up)
        elif (self.get_head_position()[1] == 460 or self.get_head_position()[1] == 20) and self.get_head_position()[0] != 460:
            self.turn(right)

class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_position()

    def randomize_position(self, snakePositions = []):
        pos = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)
        if pos in snakePositions:
            self.randomize_position(snakePositions)
        else:
            self.position = pos

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",16)
    limit = 10
    while (True):
        # check if snake length == grid_width * grid_height
        if snake.length == grid_width * grid_height:
            print('Game won')
            return

        clock.tick(limit)
        if len(sys.argv) == 2 and sys.argv[1] == 'hamiltonian':
            snake.hamiltonian_cycle()
            limit = 0
        
        snake.controls()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position(snake.positions)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text = myfont.render(f"Score {snake.score}", 1, (255,255,255))
        screen.blit(text, (5,10))
        pygame.display.update()

main()