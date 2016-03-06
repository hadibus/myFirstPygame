import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((640,480))
pygame.display.set_caption('Run and Avoid')

pygame.display.update()

while not gameExit:
    for event in pygame.event.get():



pygame.quit() #uninitialize pygame
quit() #quit program
