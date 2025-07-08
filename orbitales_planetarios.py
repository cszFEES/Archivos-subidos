import pygame
import math

pygame.init()
ancho, alto = 1200, 900
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Orbitales planetarios")
reloj = pygame.time.Clock()

gravedad = 6.67430e-11
vista_fijada = 6e-11
vista_entera = 1e-9
dt = 86400  # valor típico de un día en segundos

zoom = False

class Planeta:
    def __init__(self, x, y, vx, vy, masa, radio, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.masa = masa
        self.radio = radio
        self.color = color
        self.trayecto = []

    def actualizar_posicion(self, cuerpos):
        fx = fy = 0

        for cuerpo in cuerpos:
            if cuerpo != self:
                dx = cuerpo.x - self.x
                dy = cuerpo.y - self.y
                r = math.sqrt(dx**2 + dy**2)
                if r > 0:
                    # Fuerza gravitatoria correcta: F = G * m1 * m2 / r^2
                    fuerza = gravedad * self.masa * cuerpo.masa / (r**2)
                    fx += fuerza * dx / r
                    fy += fuerza * dy / r

        ax = fx / self.masa
        ay = fy / self.masa
        self.vx += ax * dt
        self.vy += ay * dt
        self.x += self.vx * dt 
        self.y += self.vy * dt  
        
        talla_actual = vista_fijada if zoom else vista_entera

        self.trayecto.append((int(self.x * talla_actual + ancho // 2), int(self.y * talla_actual + alto // 2)))

        if len(self.trayecto) > 200:  
            self.trayecto.pop(0)

    def draw(self, pantalla):
        if len(self.trayecto) > 1: 
            pygame.draw.lines(pantalla, (60, 60, 60), False, self.trayecto, 1)

        talla_actual = vista_fijada if zoom else vista_entera

        pantallaX = int(self.x * talla_actual + ancho // 2)
        pantallaY = int(self.y * talla_actual + alto // 2)  

        pygame.draw.circle(pantalla, self.color, (pantallaX, pantallaY), self.radio)


cuerpos = [ # x, y, vx, vy, masa, radio, color
    Planeta(0, 0, 0, 0, 1.989e30, 8, (255, 255, 0)),  # Sol
    Planeta(5.79e10, 0, 0, 47360, 3.301e23, 2, (169, 169, 169)),  # Mercurio
    Planeta(1.082e11, 0, 0, 35020, 4.867e24, 3, (255, 165, 0)),  # Venus
    Planeta(1.496e11, 0, 0, 29780, 5.972e24, 4, (0, 100, 255)),  # Tierra
    Planeta(2.79e11, 0, 0, 24077, 6.39e23, 3, (255, 100, 0)),  # Marte
    Planeta(7.786e11, 0, 0, 13070, 1.898e27, 6, (200, 150, 100)),  # Júpiter
    Planeta(1.432e12, 0, 0, 9680, 5.683e26, 5, (250, 200, 100)),  # Saturno
    Planeta(2.867e12, 0, 0, 6810, 8.681e25, 4, (100, 200, 255)),  # Urano
    Planeta(4.515e12, 0, 0, 5430, 1.024e26, 4, (0, 0, 255)),  # Neptuno
    Planeta(5.906e12, 0, 0, 4670, 1.309e22, 2, (150, 100, 50)),  # Plutón
]

activado = True
while activado:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            activado = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_z:
                zoom = not zoom
                for cuerpo in cuerpos:
                    cuerpo.trayecto = []

    pantalla.fill((0, 0, 0))

    for cuerpo in cuerpos:
        cuerpo.actualizar_posicion(cuerpos)
        cuerpo.draw(pantalla)

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
