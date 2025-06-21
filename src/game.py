from game_logic import Game # For the rules of the game
import pygame # For the window
import random # For dev commands, since I get bored easily

TOTAL_PIXEL_SIZE = 4
PIXEL_BORDER_SIZE = 1

BACKGROUND_COLOR = (80, 80, 80)
DEAD_COLOR = (40, 40, 40)
ALIVE_COLOR = (180, 180, 180)

SLIDER_BOX_COLOR = (40, 40, 120)
SLIDER_COLOR = (180, 180, 180)

def run_game(rule: str) -> None:
    global TOTAL_PIXEL_SIZE, PIXEL_BORDER_SIZE
    global BACKGROUND_COLOR, DEAD_COLOR, ALIVE_COLOR
    global SLIDER_BOX_COLOR, SLIDER_COLOR
    
    pygame.init()

    g = Game(rule)
    
    width = 600
    height = 400
    x = -width // 2 # The board is infinite, so x and y represent the coordinates, in pixels, of the top-left corner of the window
    y = -height // 2

    drawing = False # Adding/removing pixels
    dragging = False # Moving around inside the window
    painting = False # False for removing, True for adding
    dragging_slider = False # Changing speed


    fill = False # randomly fill 30% of visible pixels, to add some chaos


    speed = 40 # speed is how many 'ticks' until the board next updates; high speed means slow game


    step = 0 # how many frames have passed


    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(" Game of Life")


    running = True
    clock = pygame.time.Clock() # Manages FPS (60)
    mouse_x, mouse_y = pygame.mouse.get_pos()


    while running:
        # Getting inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                old_width, old_height = width, height
                width, height = event.size
                x += (old_width - width) // 2 # Keep it centered on the same spot when resizing
                y += (old_height - height) // 2
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE) # Resize the window
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_f:
                    fill = True
                if event.key == pygame.K_c:
                    g.points = set() # Delete all points
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_y < height * 7 // 8: # In the pixels vs. in speed slider
                    if event.button == 1: # Left click
                        dragging = True
                        drawing = False
                    if event.button == 3: # Right click
                        drawing = True
                        dragging = False
                        painting = ((mouse_x + x) // TOTAL_PIXEL_SIZE, (mouse_y + y) // TOTAL_PIXEL_SIZE) not in g.points # Opposite of whether the mouse is on a live or dead pixel
                if width // 3 < mouse_x < width * 2 // 3 and height * 29 // 32 < mouse_y < height * 31 // 32: # Mouse is in the speed slider box
                    dragging_slider = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    dragging_slider = False
                if event.button == 3:
                    drawing = False


        # Handle different mouse functions
        a = pygame.mouse.get_pos()
        if dragging:
            x += mouse_x - a[0] # Change in mouse position
            y += mouse_y - a[1]
        if drawing:
            if painting == 1:
                g.points.add(((x + a[0]) // TOTAL_PIXEL_SIZE, (y + a[1]) // TOTAL_PIXEL_SIZE)) # Adding pixels
            else:
                g.points.discard(((x + a[0]) // TOTAL_PIXEL_SIZE, (y + a[1]) // TOTAL_PIXEL_SIZE)) # Deleting pixels
        if dragging_slider:
            speed = max(1, min((width * 2 // 3 - a[0]) * 180 // width, 60)) # Flattened to between 1 and 60


        # Drawing
        screen.fill(BACKGROUND_COLOR)
        for i in range(x // TOTAL_PIXEL_SIZE, (width + x) // TOTAL_PIXEL_SIZE + 1):
            for j in range(y // TOTAL_PIXEL_SIZE, (height * 7 // 8 + y) // TOTAL_PIXEL_SIZE + 1): # Drawing every pixel; also includes fill command
                if fill:
                    if random.random() < .3:
                        g.points.add((i, j))
                    else:
                        g.points.discard((i, j))
                if (i, j) in g.points: # Alive pixels
                    pygame.draw.rect(screen, ALIVE_COLOR, (i * TOTAL_PIXEL_SIZE - x + PIXEL_BORDER_SIZE, j * TOTAL_PIXEL_SIZE - y + PIXEL_BORDER_SIZE, TOTAL_PIXEL_SIZE - PIXEL_BORDER_SIZE, TOTAL_PIXEL_SIZE - PIXEL_BORDER_SIZE))
                else: # Dead pixels
                    pygame.draw.rect(screen, DEAD_COLOR, (i * TOTAL_PIXEL_SIZE - x + PIXEL_BORDER_SIZE, j * TOTAL_PIXEL_SIZE - y + PIXEL_BORDER_SIZE, TOTAL_PIXEL_SIZE - PIXEL_BORDER_SIZE, TOTAL_PIXEL_SIZE - PIXEL_BORDER_SIZE))


        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, height * 7 // 8, width, height // 8)) # Cut off encroaching pixels on the speed button


        pygame.draw.rect(screen, SLIDER_BOX_COLOR, (width // 3, height * 29 // 32, width // 3, height // 16)) # Speed box
        pygame.draw.rect(screen, SLIDER_COLOR, (width * 2 // 3 - speed * width // 180 - width // 128, height * 29 // 32, width // 64, height // 16)) # Speed slider
        pygame.display.flip()

        step += 1
        if speed < 60 and not step % speed:
            g.step()

        clock.tick(60)
        mouse_x, mouse_y = a
        fill = False


    pygame.quit()
    
    return
