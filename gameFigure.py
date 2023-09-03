import pygame
import time

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
ROSAFOSFO = (255, 0, 255)

WIDHT = 800
HEIGHT = 600

pygame.init()

screen = pygame.display.set_mode([WIDHT, HEIGHT])
pygame.display.set_caption("Las Torres Gemelas")

class Disk:
    def __init__(self, size, color):
        self.size = size
        self.color = color

class Pole:
    def __init__(self, x, color):
        self.disks = []
        self.x = x
        self.color = color

    def agregar(self, disk):
        self.disks.append(disk)

    def eliminar(self):
        if len(self.disks) > 0:
            return self.disks.pop()

    def primero(self):
        if len(self.disks) > 0:
            return self.disks[-1]

    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x - 5, 400, 10, 500])
        for i, disk in enumerate(self.disks):
            pygame.draw.rect(screen, disk.color, [
                self.x - disk.size * 10, HEIGHT - (i + 1) * 20, disk.size * 20, 20])

class Game:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.poles = [Pole(WIDHT / 4, AZUL), Pole(WIDHT /
                                                         2, ROJO), Pole(WIDHT * 3 / 4, VERDE)]
        self.moves = 0
        self.resuelto = False
        
        for i in range(num_disks):
            self.poles[0].agregar(Disk(num_disks - i, ROSAFOSFO))

    def move_disk(self, from_pole, to_pole):
        disk = from_pole.eliminar()
        if disk:
            to_pole.agregar(disk)
            self.moves += 1
            self.check_resuelto()
            return True
        else:
            return False

    def solve(self, num_disks, from_pole, to_pole, aux_pole):
        if num_disks == 1:
            self.move_disk(from_pole, to_pole)
            self.draw()
            time.sleep(0.5)
        else:
            self.solve(num_disks - 1, from_pole, aux_pole, to_pole)
            self.move_disk(from_pole, to_pole)
            self.draw()
            time.sleep(0.5)
            self.solve(num_disks - 1, aux_pole, to_pole, from_pole)

    def check_resuelto(self):

        if len(self.poles[0].disks) == 0 and len(self.poles[1].disks) == 0 and len(self.poles[2].disks) == self.num_disks:
            self.resuelto = True
        

    def draw(self):
        screen.fill(BLANCO)
        for pole in self.poles:
            pole.draw()

        font = pygame.font.SysFont(None, 50)
        text = font.render("Movimientos: {}".format(self.moves), True, NEGRO)
        text_rect = text.get_rect()
        text_rect.topright = (WIDHT - 20, 20)
        screen.blit(text, text_rect)

        if self.resuelto:
            text = font.render("RESUELTOOO", True, NEGRO)
            screen.blit(text, (10, 10))

        pygame.display.flip()

game = Game(3)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game.resuelto:
        game.solve(game.num_disks, game.poles[0], game.poles[2], game.poles[1])

    game.draw()
    pygame.display.flip()

pygame.quit()

