import pygame
from datetime import datetime
from tools import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    base_layer = pygame.Surface((800, 600))
    clock = pygame.time.Clock()

    radius = 5
    color = (255, 255, 255)
    mode = 'brush'

    LMBpressed = False
    prev_pos = None
    startX, startY = 0, 0

    font = pygame.font.SysFont(None, 36)
    text_input = ""
    text_pos = None

    shape_modes = ['rect', 'circle', 'square', 'right_triangle', 'eq_triangle', 'rhombus', 'line']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if mode == 'text' and text_pos:
                    if event.key == pygame.K_RETURN:
                        base_layer.blit(font.render(text_input, True, color), text_pos)
                        text_input = ""; text_pos = None
                    elif event.key == pygame.K_ESCAPE:
                        text_input = ""; text_pos = None
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                else:
                    if event.key == pygame.K_r: color = (255, 0, 0)
                    if event.key == pygame.K_g: color = (0, 255, 0)
                    if event.key == pygame.K_b: color = (0, 0, 255)
                    if event.key == pygame.K_1: mode = 'brush'
                    if event.key == pygame.K_2: mode = 'rect'
                    if event.key == pygame.K_3: mode = 'circle'
                    if event.key == pygame.K_4: mode = 'eraser'
                    if event.key == pygame.K_5: mode = 'square'
                    if event.key == pygame.K_6: mode = 'right_triangle'
                    if event.key == pygame.K_7: mode = 'eq_triangle'
                    if event.key == pygame.K_8: mode = 'rhombus'
                    if event.key == pygame.K_q: mode = 'pencil'
                    if event.key == pygame.K_w: mode = 'line'
                    if event.key == pygame.K_f: mode = 'fill'
                    if event.key == pygame.K_t: mode = 'text'
                    if event.key == pygame.K_z: radius = 2
                    if event.key == pygame.K_x: radius = 5
                    if event.key == pygame.K_c: radius = 10
                    if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        filename = "canvas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                        pygame.image.save(base_layer, filename)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LMBpressed = True
                    startX, startY = event.pos
                    prev_pos = event.pos
                    if mode == 'fill': flood_fill(base_layer, *event.pos, color)
                    if mode == 'text': text_pos = event.pos; text_input = ""

            if event.type == pygame.MOUSEMOTION:
                if LMBpressed:
                    curr_pos = event.pos
                    if mode == 'brush':
                        draw_line(base_layer, color, prev_pos, curr_pos, radius); prev_pos = curr_pos
                    elif mode == 'eraser':
                        draw_line(base_layer, (0, 0, 0), prev_pos, curr_pos, radius * 2); prev_pos = curr_pos
                    elif mode == 'pencil':
                        pygame.draw.line(base_layer, color, prev_pos, curr_pos, radius); prev_pos = curr_pos
                    elif mode in shape_modes:
                        screen.blit(base_layer, (0, 0))
                        if mode == 'rect': pygame.draw.rect(screen, color, calculate_rect(startX, startY, *curr_pos), 2)
                        elif mode == 'circle':
                            dist = int(((startX-curr_pos[0])**2+(startY-curr_pos[1])**2)**0.5)
                            pygame.draw.circle(screen, color, (startX, startY), dist, 2)
                        elif mode == 'square': draw_polygon(screen, color, get_square_points(startX, startY, *curr_pos))
                        elif mode == 'right_triangle': draw_polygon(screen, color, get_right_triangle_points(startX, startY, *curr_pos))
                        elif mode == 'eq_triangle': draw_polygon(screen, color, get_equilateral_triangle_points(startX, startY, *curr_pos))
                        elif mode == 'rhombus': draw_polygon(screen, color, get_rhombus_points(startX, startY, *curr_pos))
                        elif mode == 'line': pygame.draw.line(screen, color, (startX, startY), curr_pos, radius)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LMBpressed = False
                    if mode == 'rect': pygame.draw.rect(base_layer, color, calculate_rect(startX, startY, *event.pos), 2)
                    elif mode == 'circle':
                        dist = int(((startX-event.pos[0])**2+(startY-event.pos[1])**2)**0.5)
                        pygame.draw.circle(base_layer, color, (startX, startY), dist, 2)
                    elif mode == 'square': draw_polygon(base_layer, color, get_square_points(startX, startY, *event.pos))
                    elif mode == 'right_triangle': draw_polygon(base_layer, color, get_right_triangle_points(startX, startY, *event.pos))
                    elif mode == 'eq_triangle': draw_polygon(base_layer, color, get_equilateral_triangle_points(startX, startY, *event.pos))
                    elif mode == 'rhombus': draw_polygon(base_layer, color, get_rhombus_points(startX, startY, *event.pos))
                    elif mode == 'line': pygame.draw.line(base_layer, color, (startX, startY), event.pos, radius)
                    prev_pos = None

        if not (LMBpressed and mode in shape_modes):
            screen.blit(base_layer, (0, 0))
        if text_pos:
            screen.blit(font.render(text_input + "|", True, color), text_pos)

        pygame.display.flip()
        clock.tick(60)

main()