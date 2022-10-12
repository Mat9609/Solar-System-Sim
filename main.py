from ast import Mod
import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 1000

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Solar System Sim")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (210,105,30)
LIGHT_BROWN = (226,191,125)
LIGHT_BLUE = (187, 225, 228)
DARK_BLUE = (62, 84, 232)
FONT_COLOR = (169,169,169)

class Planet:
    #Astronomical Unit, distance from Earth to Sun in meters
    AU = 149.6e6 * 1000
    # Grativational Constant
    G = 6.67428e-11
    #Scaling meter to pixels - 1AU = 100 pixels
    SCALE = 100/AU
    SIZE_SCALE = 100/AU
    # 1 day Timestep
    TIMESTEP = 3600*24
    FONT = pygame.font.SysFont("arial", 20, True)

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

    def draw(self, win, offset_x, offset_y, scale_change):
        x = self.x * self.SCALE * scale_change + WIDTH / 2 + offset_x
        y = self.y * self.SCALE * scale_change + HEIGHT / 2 + offset_y

        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = x_orbit * self.SCALE * scale_change + WIDTH / 2 + offset_x
                y_orbit = y_orbit * self.SCALE * scale_change + HEIGHT / 2 + offset_y
                scaled_points.append((x_orbit, y_orbit))
            pygame.draw.lines(win, self.color, False, scaled_points, 2)
        
        
        
        name_text = self.FONT.render(self.name, True, FONT_COLOR)
        pygame.draw.circle(win, self.color, (x, y), self.radius * self.AU * self.SIZE_SCALE * scale_change)
        win.blit(name_text, (x - name_text.get_width()/2, y))
        if not self.sun:
            distance_text = self.FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", True, FONT_COLOR)
            win.blit(distance_text, (x - distance_text.get_width()/2, y + 20))

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


class Comet:
        #Astronomical Unit, distance from Earth to Sun in meters
    AU = 149.6e6 * 1000
    # Grativational Constant
    G = 6.67428e-11
    #Scaling meter to pixels - 1AU = 100 pixels
    SCALE = 100/AU
    SIZE_SCALE = 100/AU
    # 1 day Timestep
    TIMESTEP = 3600*24
    FONT = pygame.font.SysFont("arial", 20, True)

    def __init__(self, name, x, y, mass, offset_x, offset_y, scale_change):
        self.name = name
        self.x = (x - (WIDTH / 2 + offset_x))/(self.SCALE * scale_change) 
        self.y = (y - (HEIGHT / 2 + offset_y))/(self.SCALE * scale_change)
        self.radius = 1.33691742e-9 #200 meters
        self.color = WHITE
        self.mass = mass

        self.orbit = []
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, offset_x, offset_y, scale_change):
        x = self.x
        y = self.y

        if len(self.orbit) > 2:
            scaled_points = []
            for point in self.orbit:
                x_orbit, y_orbit = point
                x_orbit = x_orbit * self.SCALE * scale_change + WIDTH / 2 + offset_x
                y_orbit = y_orbit * self.SCALE * scale_change + HEIGHT / 2 + offset_y
                scaled_points.append((x_orbit, y_orbit))
            pygame.draw.lines(win, self.color, False, scaled_points, 2)
        
        name_text = self.FONT.render(self.name, True, FONT_COLOR)
        pygame.draw.circle(win, self.color, (x * self.SCALE * scale_change + WIDTH / 2 + offset_x, y * self.SCALE * scale_change + HEIGHT / 2 + offset_y), self.radius * self.AU * self.SIZE_SCALE * scale_change)
        
        distance_text = self.FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", True, FONT_COLOR)
        win.blit(name_text, (x * self.SCALE * scale_change + WIDTH / 2 + offset_x - distance_text.get_width()/2 - name_text.get_width()/2, y * self.SCALE * scale_change + HEIGHT / 2 + offset_y))

        win.blit(distance_text, (x * self.SCALE * scale_change + WIDTH / 2 + offset_x - distance_text.get_width()/2, y * self.SCALE * scale_change + HEIGHT / 2 + offset_y + 20))

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
    moving = False
    comet_setup = False
    offset_x = 0
    offset_y = 0
    scale_change = 1
    coor_right_click = [0, 0]
    coor_right_click_last = [0, 0]
    bg = pygame.image.load("bg.jpg")
    FONT = pygame.font.SysFont("arial", 20, True)
    #Clock definition to refresh window
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 0.00465047, YELLOW, 1.98892 * 10**30)
    sun.sun = True
    mercury = Planet ("Mercury", 0.387 * Planet.AU, 0, 0.00001630836515, DARK_GREY, 3.30* 10**23)
    mercury.y_vel = 47.4 *1000
    venus = Planet ("Venus", 0.723 * Planet.AU, 0, 0.00004045372964, WHITE, 4.8685* 10**24)
    venus.y_vel = -35.02 *1000
    earth = Planet ("Earth", -1 * Planet.AU, 0, 0.00004258744697, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 *1000
    mars = Planet ("Mars", -1.524 * Planet.AU, 0, 0.00002265737741, RED, 6.39 * 10**23) 
    mars.y_vel = 24.077 *1000
    jupiter = Planet ("Jupiter", 5.2 * Planet.AU, 0, 0.0004673255383, BROWN, 1.898 * 10**27)
    jupiter.y_vel = 13.06 *1000
    saturn = Planet ("Saturn", 9.5 * Planet.AU, 0, 0.0003892569, LIGHT_BROWN, 5.683* 10**26)
    saturn.y_vel = 9.69 *1000
    uranus = Planet ("Uranus",  19.8 * Planet.AU, 0, 0.0001695345, LIGHT_BLUE, 8.681* 10**25)
    uranus.y_vel = 6.81 *1000
    neptune = Planet ("Neptune", 30 * Planet.AU, 0, 0.0001645879, DARK_BLUE, 1.024* 10**26)
    neptune.y_vel = 5.43 *1000
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    comets = []
    comet_edited = Comet ("Comet", 0, 0, 3.36 * 10**10, offset_x, offset_y, scale_change)
    day = 0
    mercury_year = 0
    venus_year = 0
    earth_year = 0
    mars_year = 0
    jupiter_year = 0
    saturn_year = 0
    uranus_year = 0
    neptune_year = 0
    while run:
        #60 frames per second max
        clock.tick(60)
        WIN.fill((0,0,0))
        WIN.blit(bg, (0, 0))
        day += 1
        if day % 88 == 0:
            mercury_year += 1
        if day % 225 == 0:
            venus_year += 1   
        if day % 365 == 0:
            earth_year += 1
        if day % 687 == 0:
            mars_year += 1
        if day % 4333 == 0:
            jupiter_year += 1
        if day % 10759 == 0:
            saturn_year += 1
        if day % 30687 == 0:
            uranus_year += 1
        if day % 60190 == 0:
            neptune_year += 1
       
        day_text = FONT.render(f"Days: {day}", True, FONT_COLOR)
        WIN.blit(day_text, (10, 10))
        mercury_year_text = FONT.render(f"Mercury years: {mercury_year}", True, FONT_COLOR)
        WIN.blit(mercury_year_text, (10, 30))
        venus_year_text = FONT.render(f"Venus years: {venus_year}", True, FONT_COLOR)
        WIN.blit(venus_year_text, (10, 50))
        earth_year_text = FONT.render(f"Earth years: {earth_year}", True, FONT_COLOR)
        WIN.blit(earth_year_text, (10, 70))
        mars_year_text = FONT.render(f"Mars years: {mars_year}", True, FONT_COLOR)
        WIN.blit(mars_year_text, (10, 90))
        jupiter_year_text = FONT.render(f"Jupiter years: {jupiter_year}", True, FONT_COLOR)
        WIN.blit(jupiter_year_text, (10, 110))
        saturn_year_text = FONT.render(f"Saturn years: {saturn_year}", True, FONT_COLOR)
        WIN.blit(saturn_year_text, (10, 130))
        uranus_year_text = FONT.render(f"Uranus years: {uranus_year}", True, FONT_COLOR)
        WIN.blit(uranus_year_text, (10, 150))
        neptune_year_text = FONT.render(f"Neptune years: {neptune_year}", True, FONT_COLOR)
        WIN.blit(neptune_year_text, (10, 170))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moving = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving = True
                coor_start = event.pos
            if event.type == pygame.MOUSEMOTION and moving:
                coor_now = event.pos
                offset_x = offset_x + (coor_now[0] - coor_start[0])/15
                offset_y = offset_y + (coor_now[1] - coor_start[1])/15
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                offset_x = 0
                offset_y = 0
            if event.type == pygame.MOUSEWHEEL and event.y == 1:
                scale_change = scale_change + 0.2
            if event.type == pygame.MOUSEWHEEL and event.y == -1:
                scale_change = scale_change - 0.2
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                coor_right_click = event.pos
                comet_setup = True
                comet_edited = Comet ("Comet", 0, 0, 3.36 * 10**10, offset_x, offset_y, scale_change)
                comet_edited.x = (coor_right_click[0] - (WIDTH / 2 + offset_x))/(comet_edited.SCALE * scale_change)
                comet_edited.y = (coor_right_click[1] - (HEIGHT / 2 + offset_y))/(comet_edited.SCALE * scale_change)
                print(comet_edited.x)
                
            if event.type == pygame.MOUSEMOTION and comet_setup:
                coor_right_click_last = event.pos
                comet_edited.x_vel = (coor_right_click_last[0] - coor_right_click[0]) * 100
                comet_edited.y_vel = (coor_right_click_last[1] - coor_right_click[1]) * 100
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                comets.append(comet_edited)
                print(comet_edited)
                comet_setup = False
                
        if comet_setup:
            pygame.draw.lines(WIN, RED, False, (coor_right_click, coor_right_click_last), 2)
            x_velocity_text = FONT.render(f"X Velocity: {round(comet_edited.x_vel, 1)}m/s", True, FONT_COLOR)
            WIN.blit(x_velocity_text, (coor_right_click[0] - x_velocity_text.get_width()/2, coor_right_click[1]))
            y_velocity_text = FONT.render(f"Y Velocity: {round(comet_edited.y_vel, 1)}m/s", True, FONT_COLOR)
            WIN.blit(y_velocity_text, (coor_right_click[0] - y_velocity_text.get_width()/2, coor_right_click[1]+30))
        
       
        if scale_change < 0.2:
            scale_change = 0.2

        if scale_change > 10:
            scale_change = 10

        

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, offset_x, offset_y, scale_change)

        for comet in comets:
            comet.update_position(planets)
            comet.draw(WIN, offset_x, offset_y, scale_change)

        pygame.display.update()


    pygame.quit()


main()