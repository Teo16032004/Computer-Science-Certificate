import pygame
import random
pygame.init()

class DrawInformation:
    BLACK= 0,0,0
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    RED = (255,0,0)
    BACKGROUND_COLOR= WHITE

    GRADIENTS= [
        (128,128,128), (160,160,160),(192,192,192)
    ]


    FONT = pygame.font.SysFont('comicsans', 23)
    LARGE_FONT = pygame.font.SysFont('comicsans', 33)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width= width
        self.height= height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)
    
    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = (self.height - self.TOP_PAD) // (self.max_val - self.min_val + 1)
        self.start_x = self.SIDE_PAD // 2
    
def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.GREEN)
    draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2 ,5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2 ,48))
    sorting = draw_info.FONT.render("I - Insersion Sort | B - Bubble Sort | M - Merge Sort | Q - Quick Sort",1,draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2 ,78))
    draw_list(draw_info)
    pygame.display.update()


def draw_list(draw_info, color_positions={},clear_bg= False):
    lst=draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD,draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)
    for i,val in enumerate(lst):
        x= draw_info.start_x + i* draw_info.block_width
        y= draw_info.height-(val- draw_info.min_val)*draw_info.block_height
        
        color = draw_info.GRADIENTS[i%3]

        if i in color_positions:
            color = color_positions[i]


        pygame.draw.rect(draw_info.window, color, (x,y,draw_info.block_width,draw_info.height))

    if clear_bg:
        pygame.display.update()

def generate_starting_list(n,min_val,max_val):
    lst =[]

    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range (len(lst) -1 -i):
            num1= lst[j]
            num2= lst[j+1]

            if (num1>num2 and ascending) or (num1<num2 and not ascending): 
                lst[j], lst[j+1] = lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN, j+1:draw_info.RED},True)
                yield True
    return lst

def insertion_sort(draw_info, ascending = True):
    lst=draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort=i >0 and lst[i-1]>current and ascending
            descending_sort=i >0 and lst[i-1]<current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i]=lst[i-1]
            i=i-1
            lst[i]=current
            draw_list(draw_info,{i-1:draw_info.GREEN,i:draw_info.RED},True)
            yield True

    return lst


def merge_sort(draw_info, ascending=True, start=0, end=None):
    lst = draw_info.lst

    if end is None:
        end = len(lst)

    if end - start > 1:
        mid = (start + end) // 2

        yield from merge_sort(draw_info, ascending, start, mid)
        yield from merge_sort(draw_info, ascending, mid, end)

        left_half = lst[start:mid]
        right_half = lst[mid:end]

        i = j = 0
        k = start

        while i < len(left_half) and j < len(right_half):
            if (left_half[i] < right_half[j] and ascending) or (left_half[i] > right_half[j] and not ascending):
                lst[k] = left_half[i]
                i += 1
            else:
                lst[k] = right_half[j]
                j += 1
            k += 1

            draw_list(draw_info, {start+i: draw_info.GREEN,mid+j:draw_info.RED}, True)
            yield True

        while i < len(left_half):
            lst[k] = left_half[i]
            i += 1
            k += 1
            draw_list(draw_info, {start+i-1: draw_info.GREEN}, True)
            yield True

        while j < len(right_half):
            lst[k] = right_half[j]
            j += 1
            k += 1
            draw_list(draw_info, {mid+j-1:draw_info.RED}, True)
            yield True

    draw_list(draw_info, {i: draw_info.GREEN for i in range(start, end)})
    return lst

def quick_sort(draw_info, ascending=True, start=0, end=None):
    lst = draw_info.lst

    if end is None:
        end = len(lst)

    if end - start > 1:
        pivot = lst[end-1]
        i = start - 1
        for j in range(start, end-1):
            if (lst[j] < pivot and ascending) or (lst[j] > pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True
        lst[i+1], lst[end-1] = lst[end-1], lst[i+1]
        draw_list(draw_info, {i+1: draw_info.GREEN, end-1: draw_info.RED}, True)
        yield True

        yield from quick_sort(draw_info, ascending, start, i+1)
        yield from quick_sort(draw_info, ascending, i+2, end)

    return lst



def main():
    run= True
    clock = pygame.time.Clock()

    n= 50
    min_val=0
    max_val=100
    lst=generate_starting_list(n,min_val,max_val)
    draw_info= DrawInformation(800,650,lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None


    while run:
        clock.tick(30)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting= False
        else: 
            draw(draw_info,sorting_algo_name,ascending)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst=generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info,ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm=insertion_sort
                sorting_algo_name="Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm=bubble_sort
                sorting_algo_name="Bubble Sort"
            elif event.key == pygame.K_m and not sorting:
                sorting_algorithm=merge_sort
                sorting_algo_name="Merge Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm=quick_sort
                sorting_algo_name="Quick Sort"
    pygame.quit()

if __name__ == "__main__":
    main()
