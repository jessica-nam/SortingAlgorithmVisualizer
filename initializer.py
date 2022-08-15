import pygame
import random
pygame.init()

class DrawInformation: #global values, better to use a class instead of global variables - less flexibility from global scope
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND = WHITE
    SIDE_PAD = 100 #padding from left right side
    TOP_PAD = 150 #top pad is area for title, controls etc

    GREYS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    def __init__(self, width, height, lst): #lst is the starting list to sort
        self.width = width 
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visulaizer")
        self.set_list(lst)
    
    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        #width depends on number of values
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))

        #height depends on range of values
        self.block_height = round((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        #start drawing blocks from x coord considering side pad space
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND)

    controls = draw_info.FONT.render("R - Reset | SPACE - Start sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 ,5))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 ,35))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info):
    lst = draw_info.lst
    for i, val in enumerate(lst): #enumerate gives index and value of every element in list
        #x, y from top left hand corner
        x = draw_info.start_x + i * draw_info.block_width
        #height is taken by taking the screen height and subtracting block height
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GREYS[i % 3] 
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))


def generate_starting_list(n, min_val, max_val):
    """Randomly generates list to be sorted"""
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst


def main():
    """Main event loop"""
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False
    ascending = True

    while run:
        clock.tick(60) #max number of times this loop can run per second

        draw(draw_info)
        pygame.display.update() #render display

        for event in pygame.event.get(): #returns list of all the events that have occured since the last loop call
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False


    pygame.quit()
        
if __name__ == "__main__":
    main()
        