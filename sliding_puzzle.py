import sys, pygame as pg, glob, os, random, button as b, grid as g
pg.init()

clock = pg.time.Clock()
FPS = 60
FRAMES_PER_SOLVE_ANIM = 15
current_solve_frame = 0

DISPLAY_DEBUG_TEXT = False
BG_COL = pg.Color("chocolate4")
IMG_DIR = "pics"

img_size = img_w, img_h = 720, 480
GRID_W = 6
GRID_H = 6
GRIDLINE_W = 2
TILE_W = img_w//GRID_W
TILE_H = img_h//GRID_H

img_area_size = img_area_w, img_area_h = img_w, img_h
status_bar_h = 50
screen_size = screen_w, screen_h = img_area_w, img_area_h + status_bar_h

# TL tile is 0, 0. TR tile is (GRID_X-1, 0). etc.
def get_picture_tile_at_position(x, y):
    return (x * TILE_W, y * TILE_H, TILE_W, TILE_H)

def get_random_image():
    image_list = glob.glob(os.path.join(IMG_DIR, "*"))
    random_img = random.choice(image_list)
    print (f"selected {random_img}")
    image = pg.image.load(random_img)
    image = pg.transform.scale(image, img_size)
    
    return image

def update_random_image():
    global display_image
    display_image = get_random_image()
    grid.shuffle_tiles()

def toggle_debug_text():
    global DISPLAY_DEBUG_TEXT
    DISPLAY_DEBUG_TEXT = not DISPLAY_DEBUG_TEXT

def play_solve():
    global playing_solve, solve_moves_to_play

    solved_moves = grid.solve()
    if solved_moves is not None:
        print("Playing solve")
        solve_moves_to_play = solved_moves
        playing_solve = True
    
grid = g.Grid(GRID_W, GRID_H)

num_buttons = 4
solve_button =          b.Button("Solve", pg.Rect(0 * screen_w/num_buttons, img_area_h, screen_w/num_buttons, status_bar_h), pg.Color("blueviolet"))
shuffle_button =        b.Button("Shuffle", pg.Rect(1 * screen_w/num_buttons, img_area_h, screen_w/num_buttons, status_bar_h), pg.Color("burlywood3"))
new_image_button =    b.Button("New image", pg.Rect(2 * screen_w/num_buttons, img_area_h, screen_w/num_buttons, status_bar_h), pg.Color("goldenrod3"))
debug_text_button =    b.Button("Debug", pg.Rect(3 * screen_w/num_buttons, img_area_h, screen_w/num_buttons, status_bar_h), pg.Color("seashell3"))
#solve_button.onclick = grid.initiate_tiles
solve_button.onclick = play_solve
new_image_button.onclick = update_random_image
shuffle_button.onclick = grid.shuffle_tiles
debug_text_button.onclick = toggle_debug_text
#debug_text_button.onclick = grid.check_valid_moves

buttons = [solve_button, shuffle_button, new_image_button, debug_text_button]

screen = pg.display.set_mode(screen_size)
pg.mouse.set_cursor(*pg.cursors.arrow)
display_image = get_random_image()
playing_solve = False
solve_moves_to_play = []

def handle_events():
    for event in pg.event.get():
        if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]: 
            pg.quit()
            sys.exit
        elif event.type == pg.MOUSEBUTTONDOWN:
            if playing_solve: continue # Disable mouse input when playing solve

            if pg.Rect(0, 0, img_area_w, img_area_h).collidepoint(event.pos):
                
                x_idx = event.pos[0] // TILE_W # to test on larger tiles
                y_idx = event.pos[1] // TILE_H
                #print(f"Collided with tile x={x_idx},y={y_idx}")
                if (grid.click_on_tile(x_idx, y_idx)):
                    was_solved = grid.check_solve()
                    if was_solved:
                        print(f"SOLVED! in {grid.iterdepth} moves.")
            else:
                for button in buttons: 
                    button.check_press(event.pos)

def render():
    screen.fill(BG_COL)
     
    mpos = pg.mouse.get_pos()
    for button in buttons: button.draw(screen, mpos)
    
    for i in range(GRID_H):
        for j in range(GRID_W):
            # the index of all_positions is incrememnted one at a time from left to right as we loop through the nested list
            tile = grid.get_tile_position(j, i)

            draw_pos_x = j * TILE_W
            draw_pos_y = i * TILE_H
                
            # None signifies the blank tile, don't draw it.
            # Unless the game is solved
            draw_tile = tile is not None or grid.solved

            if draw_tile:
                tile_x, tile_y = tile

                # get the actual the tile image and draw it on the correct position
                picture_tile_rect = get_picture_tile_at_position(tile_x, tile_y)
                screen.blit(display_image, (draw_pos_x, draw_pos_y), picture_tile_rect)
            else:
                # Draw black tile
                pg.draw.rect(screen, pg.Color("black"), (draw_pos_x, draw_pos_y, TILE_W, TILE_H))

            if DISPLAY_DEBUG_TEXT and not grid.solved:
                debug_text = "BLANK" if tile is None else f"x={tile_x},y={tile_y},n={tile_y * GRID_W + tile_x}"
                textsurface = pg.font.SysFont('Corbel', 35).render(debug_text, True, pg.Color("deeppink"))
                screen.blit(textsurface, (draw_pos_x, draw_pos_y))

    # Draw gridlines
    border_col = pg.Color("sienna")
    if not grid.solved or True:
        # Draw inner gridlines, such that it overlaps a tile on either sides by one pixel
        for i in range(GRID_W - 1):
            pg.draw.line(screen, border_col, ((i+1)*TILE_W-1, 0), ((i+1)*TILE_W-1, img_area_h), GRIDLINE_W)
        for i in range(GRID_H - 1):
            pg.draw.line(screen, border_col, (0, (i+1)*TILE_H-1), (img_area_w, (i+1)*TILE_H-1), GRIDLINE_W)
        # Draw border
        pg.draw.rect(screen, border_col, (0, 0, img_area_w, img_area_h), 2)

    if playing_solve:
        textsurface = pg.font.SysFont('Corbel', 50).render(f"Solving... {len(solve_moves_to_play)}" , True, pg.Color("white"))
        screen.blit(textsurface, (img_area_w/2 - textsurface.get_width()/2, img_area_h/2-textsurface.get_height()/2))

    pg.display.update()

def update(step_size):
    # Runs every frame
    global playing_solve, solve_moves_to_play, current_solve_frame

    if not playing_solve: return

    current_solve_frame += 1
    if (current_solve_frame >= FRAMES_PER_SOLVE_ANIM):
        current_solve_frame = 0
        if len(solve_moves_to_play) > 0:            
            move_to_play = solve_moves_to_play.pop(0) # pop the first one
            grid.click_on_tile(*move_to_play)
        else:
            print("Stopped playing solve")
            playing_solve = False

#fixed simulation step duration (ms)
step_size = 1/FPS
acc = 0.0 #accumulated time in s
current_time = pg.time.get_ticks()
while True:
    handle_events()
    
    new_time = pg.time.get_ticks()
    acc += (new_time - current_time)/1000
    current_time = new_time

    #consumes accumulated frame time in even increments of step_size
    while(acc >= step_size):
        acc -= step_size
        update(step_size)
    
    render()

    clock.tick(60)
    