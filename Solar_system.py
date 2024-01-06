import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

button_width, button_height = 150, 50
button_x, button_y = WIDTH/2.2, HEIGHT/20

clock = pygame.time.Clock()
COLOR_BLACK = (0,0,0)
COLOR_WHITE = (255, 255, 255)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (201,144,57)
COLOR_SATURN = (234,214,184)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
COLOR_BUTTON = (255,255,255)

FONT = pygame.font.SysFont("comicsans", 16)
AU = 149.6e6 * 1000
G = 6.67428e-11
deltatime = 3600*24
distance = 10
DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)

controls = ["Mousewheel Up/Down to zoom in/out",
            "Up arrow to speed up",
            "Down arrow to slow down",
            "'T' to pause",
            "'Y' to unpause",
            "'WASD' to move",
            "C to center"]

controls_description = list(map(lambda x: FONT.render(x, 1, COLOR_WHITE), controls))

DEFAULT_IMAGE_SIZE = (WIDTH, HEIGHT)
background = pygame.image.load('space_background.jpg')
image = pygame.transform.scale(background, DEFAULT_IMAGE_SIZE)
DEFAULT_IMAGE_POSITION = (500, 400)

time = 0.0

def calculating_time(deltatime):
    global time
    elapsed_time = deltatime * clock.tick(60) / 1000.0 
    time += elapsed_time
    return time


class Planet:
    scale = 70 / AU

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, move_x, move_y):
        x = self.x * Planet.scale + WIDTH / 2
        y = self.y * Planet.scale + HEIGHT / 2

        updated_points = []
        if len(self.orbit) > 2:

            for point in self.orbit:
                x, y = point
                x = x * Planet.scale + WIDTH / 2
                y = y * Planet.scale + HEIGHT / 2
                updated_points.append((x + move_x, y + move_y))

            pygame.draw.lines(WIN, self.color, False, updated_points, 2)


        pygame.draw.circle(WIN, self.color, (x + move_x, y + move_y), self.radius)

        scale = FONT.render(
            (f"Scale:{1/(1e6*(Planet.scale)):.3f} thousand km/px"), 1, COLOR_WHITE)
        WIN.blit(scale, (10, 50))

        if not self.sun:
            distance_text = FONT.render(
                f"{self.distance_to_sun/1.5e11:.4f}AU", 1, COLOR_WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width() / 2 + move_x,
                                            y - distance_text.get_height() / 2 - 20 + move_y))
            
                
        return updated_points

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * deltatime
        self.y_vel += total_fy / self.mass * deltatime

        self.x += self.x_vel * deltatime
        self.y += self.y_vel * deltatime

        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        self.radius *= scale

def initialization():
    sun = Planet(0, 0, 15, COLOR_SUN, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * AU, 0, 8, COLOR_EARTH, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * AU, 0, 6, COLOR_MARS, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * AU, 0, 4, COLOR_MERCURY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * AU, 0, 7, COLOR_VENUS, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * AU, 0, 13, COLOR_JUPITER, 1.8982 * 10**27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(9.582 * AU, 0, 12, COLOR_SATURN, 5.68 * 10**26)
    saturn.y_vel = 9.69 * 1000

    uranus = Planet(19.22 * AU, 0, 11, COLOR_URANUS, 8.68 * 10**25)
    uranus.y_vel = 6.81 * 1000

    neptune = Planet(30.07 * AU, 0, 10, COLOR_NEPTUNE, 1.024 * 10**26)
    neptune.y_vel = 5.43 * 1000

    pluto = Planet(39.48 * AU, 0, 4, COLOR_MERCURY, 1.3 * 10**22)
    planets = [sun, earth, mars, mercury, venus,
               jupiter, saturn, uranus, neptune, pluto]
    return planets

def update_planets(planets, move_x, move_y, deltatime):
    for planet in planets:
        planet.update_position(planets)
        planet.draw(WIN, move_x, move_y)

        if len(planet.orbit) >= 600:
            planet.orbit.pop(0)

def handle_keyboard_events(event, keys, deltatime, move_x, move_y, planets):

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            deltatime /= 1.5
        if event.key == pygame.K_DOWN:
            deltatime *= 1.5
        if event.key == pygame.K_t:
            deltatime = 0
        if event.key == pygame.K_y:
            deltatime = 86400
    if keys[pygame.K_c]:
        move_x, move_y = planets[0].x * planets[0].scale, planets[0].y * planets[0].scale

    return deltatime, move_x, move_y

def handle_mouse_wheel_event(event, planets):
    if event.type == pygame.MOUSEWHEEL:
        zoom_factor = 1.3**event.y
        Planet.scale = Planet.scale * zoom_factor
        for planet in planets:
            planet.update_scale(zoom_factor)

def handle_key_state(keys, move_x, move_y, distance):

    if keys[pygame.K_a]:
        move_x += distance
    if keys[pygame.K_d]:
        move_x -= distance
    if keys[pygame.K_w]:
        move_y += distance
    if keys[pygame.K_s]:
        move_y -= distance
    if keys[pygame.K_x]:
        for i, value in enumerate(controls_description):
            WIN.blit(value, (10, 650 + i * 20))
    return move_x, move_y

def handle_screen_control(event, move_x, move_y, moving):
    if event.type == pygame.MOUSEBUTTONUP:
        moving = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
        moving = True
    elif event.type == pygame.MOUSEMOTION and moving:
        move_x += event.rel[0] // 2
        move_y += event.rel[1] // 2
    return move_x, move_y, moving

def display_information(deltatime):
    time_text = FONT.render(
        f"Time from start:{calculating_time((deltatime)/525600):.3f} years", 1, COLOR_WHITE)
    WIN.blit(time_text, (10, 10))

    deltatime_text = FONT.render(f"Time:{round((deltatime/1440),3)} days/s", 1, COLOR_WHITE)
    WIN.blit(deltatime_text, (10, 30))

    controls = FONT.render(("Hold X to see the controls"), 1, COLOR_WHITE)
    WIN.blit(controls, (1000, 10))

    pygame.draw.rect(WIN, COLOR_BUTTON, (button_x, button_y, button_width, button_height))
    text = FONT.render("Create new object", True, COLOR_BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    WIN.blit(text, text_rect)

    pygame.display.set_caption(str(clock.get_fps()))
    pygame.display.update()

def main():
    global deltatime
    move_x = 0
    move_y = 0
    run = True
    planets = initialization()
    moving = False
    while run:
        clock.tick(60)
        WIN.blit(image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (
                    button_x <= mouse_x <= button_x + button_width
                    and button_y <= mouse_y <= button_y + button_height
                ):
                    print("Button Clicked!")

            handle_mouse_wheel_event(event, planets)
            move_x, move_y, moving = handle_screen_control(event, move_x, move_y, moving)

            
        
        keys = pygame.key.get_pressed()
        deltatime, move_x, move_y = handle_keyboard_events(event, keys, deltatime, move_x, move_y, planets)

        move_x, move_y = handle_key_state(keys, move_x, move_y, 10)

        update_planets(planets, move_x, move_y, deltatime)
        display_information(deltatime)

        pygame.display.flip()

    pygame.quit()
main()