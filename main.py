from configparser import DuplicateSectionError
import pygame
import random
import math
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

    FONT = pygame.font.SysFont('Times New Roman', 20)
    LARGE_FONT = pygame.font.SysFont('Times New Roman', 30)

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
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))

        #start drawing blocks from x coord considering side pad space
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info, algorithm_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND)

    title = draw_info.FONT.render(f"{algorithm_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 ,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 ,35))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 ,65))

    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions = {}, clear_background = False):
    lst = draw_info.lst

    if clear_background:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        #draw rectangle
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND, clear_rect)
    for i, val in enumerate(lst): #enumerate gives index and value of every element in list
        #x, y from top left hand corner
        x = draw_info.start_x + i * draw_info.block_width
        #height is taken by taking the screen height and subtracting block height
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GREYS[i % 3] 

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_background:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    """Randomly generates list to be sorted"""
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True):
    """Implements Bubble Sort algorithm"""
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 -i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst [j + 1], lst[j] #swap
                draw_list(draw_info, {j: draw_info.BLACK, j + 1: draw_info.BLACK}, True)
                yield True #yield makes function a generator
    return lst

def insertion_sort(draw_info, ascending = True):
    """Implements Insertion Sort algorithm"""
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            #swaps
            lst[i] = lst[i - 1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i: draw_info.BLACK, i - 1: draw_info.BLACK}, True)
            yield True

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

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60) #max number of times this loop can run per second
        #to speed up sorting speed increase clock tick

        if sorting: #if currently sorting
            try: #try to call next method
                next(sorting_algorithm_generator)
            except StopIteration: #generator is done
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name, ascending)

        #draw(draw_info)
        #pygame.display.update() #render display

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
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"


    pygame.quit()
        
if __name__ == "__main__":
    main()
        