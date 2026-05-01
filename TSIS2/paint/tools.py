import pygame
import math

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def draw_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surface, color, (x, y), radius)

def get_square_points(x1, y1, x2, y2):
    side = min(abs(x2 - x1), abs(y2 - y1))
    sx = x1 + (side if x2 > x1 else -side)
    sy = y1 + (side if y2 > y1 else -side)
    return [(x1, y1), (sx, y1), (sx, sy), (x1, sy)]

def get_right_triangle_points(x1, y1, x2, y2):
    return [(x1, y1), (x2, y1), (x1, y2)]

def get_equilateral_triangle_points(x1, y1, x2, y2):
    base = x2 - x1
    height = int(abs(base) * math.sqrt(3) / 2) * (1 if y2 >= y1 else -1)
    mid_x = (x1 + x2) // 2
    return [(x1, y1), (x2, y1), (mid_x, y1 + height)]

def get_rhombus_points(x1, y1, x2, y2):
    cx, cy = x1, y1
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    return [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]

def draw_polygon(surface, color, points):
    if len(points) >= 2:
        pygame.draw.polygon(surface, color, points, 2)

def flood_fill(surface, x, y, fill_color):
    target_color = surface.get_at((x, y))
    if target_color == fill_color:
        return
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if cx < 0 or cx >= surface.get_width() or cy < 0 or cy >= surface.get_height():
            continue
        if surface.get_at((cx, cy)) != target_color:
            continue
        surface.set_at((cx, cy), fill_color)
        stack.append((cx + 1, cy))
        stack.append((cx - 1, cy))
        stack.append((cx, cy + 1))
        stack.append((cx, cy - 1))