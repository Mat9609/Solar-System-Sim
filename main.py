import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1500, 1500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Solar System Sim")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (210,105,30)
FONT_COLOR = (169,169,169)

class Planet:
    #Astronomical Unit, distance from Earth to Sun in meters
    AU = 149.6e6 * 1000
    # Grativational Constant
    G = 6.67428e-11
    #Scaling meter to pixels - 1AU = 100 pixels
    SCALE = 90/AU
    # 1 day Timestep
    TIMESTEP = 3600*24


    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
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

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        bigfont = pygame.font.SysFont("arial", 20, True)
        text = bigfont.render(self.name, True, FONT_COLOR)
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        win.blit(text, (x,y))


    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():
    # Run variable
    run = True

    #Clock definition to refresh window
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 109, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    mercury = Planet ("Mercury", 0.387 * Planet.AU, 0, 0.383, DARK_GREY, 3.30* 10**23)
    mercury.y_vel = 47.4 *1000
    venus = Planet ("Venus",0.723 * Planet.AU, 0, 0.949, WHITE, 4.8685* 10**24)
    venus.y_vel = -35.02 *1000
    earth = Planet ("Earth", -1 * Planet.AU, 0, 1, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 *1000
    mars = Planet ("Mars", -1.524 * Planet.AU, 0, 0.532, RED, 6.39 * 10**23) 
    mars.y_vel = 24.077 *1000
    jupiter = Planet ("Jupiter", 5.2 * Planet.AU, 0, 11.209, BROWN, 4.8685* 10**24)
    jupiter.y_vel = 13.06 *1000
    planets = [sun, mercury, venus, earth, mars, jupiter]

    while run:
        #60 frames per second max
        clock.tick(60)
        WIN.fill((0,0,0))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()


    pygame.quit()


main()