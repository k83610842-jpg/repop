import pygame

# Считаем рамки для прямоугольника, чтоб рисовался в любую сторону
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

# Магия плавной линии: соединяем кружочки, чтоб не было дырок
def draw_line(surface, color, start, end, radius):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(surface, color, (x, y), radius)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    # Это наш холст, на нем остается всё рисоволово
    base_layer = pygame.Surface((800, 600))
    clock = pygame.time.Clock()
    
    radius = 5
    color = (255, 255, 255) # Белый по умолчанию, классика
    mode = 'brush' # Стартуем с кисточки
    
    LMBpressed = False
    prev_pos = None # Сюда сохраняем, где мышка была только что
    startX, startY = 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                # Меняем цвета на кнопки: R, G, B
                if event.key == pygame.K_r: color = (255, 0, 0)
                if event.key == pygame.K_g: color = (0, 255, 0)
                if event.key == pygame.K_b: color = (0, 0, 255)
                
                #1-кисть, 2-квадрат, 3-круг, 4-стерка
                if event.key == pygame.K_1: mode = 'brush'
                if event.key == pygame.K_2: mode = 'rect'
                if event.key == pygame.K_3: mode = 'circle'
                if event.key == pygame.K_4: mode = 'eraser'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LMBpressed = True
                    startX, startY = event.pos # Засекаем, где нажали
                    prev_pos = event.pos 

            if event.type == pygame.MOUSEMOTION:
                if LMBpressed:
                    curr_pos = event.pos
                    
                    if mode == 'brush':
                        # Рисуем ровную линию без пробелов
                        draw_line(base_layer, color, prev_pos, curr_pos, radius)
                        prev_pos = curr_pos # Запоминаем текущую позицию как старую
                    
                    elif mode == 'eraser':
                        # Стираем.Та же линия, только черная и потолще
                        draw_line(base_layer, (0, 0, 0), prev_pos, curr_pos, radius * 2)
                        prev_pos = curr_pos
                    
                    elif mode in ['rect', 'circle']:
                        # Рисуем «призрачную» фигуру, пока тащим мышку
                        screen.blit(base_layer, (0, 0)) # Сначала чистим экран слоем базы
                        if mode == 'rect':
                            pygame.draw.rect(screen, color, calculate_rect(startX, startY, *curr_pos), 2)
                        else:
                            # Считаем радиус круга от точки нажатия до мышки
                            dist = int(((startX - curr_pos[0])**2 + (startY - curr_pos[1])**2)**0.5)
                            pygame.draw.circle(screen, color, (startX, startY), dist, 2)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    LMBpressed = False
                    # Кнопку отпускаем и фигура на холсте намертво
                    if mode == 'rect':
                        pygame.draw.rect(base_layer, color, calculate_rect(startX, startY, *event.pos), 2)
                    elif mode == 'circle':
                        dist = int(((startX - event.pos[0])**2 + (startY - event.pos[1])**2)**0.5)
                        pygame.draw.circle(base_layer, color, (startX, startY), dist, 2)
                    prev_pos = None

        # Если не рисуем фигуры, просто показываем наш главный холст
        if not (LMBpressed and mode in ['rect', 'circle']):
            screen.blit(base_layer, (0, 0))

        pygame.display.flip()
        clock.tick(60) # Держим стабильный ФПС

main()
