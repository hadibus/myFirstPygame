#!/usr/bin/env python

"""This is a much simpler version of the badGuys.py
example. It makes a good place for beginners to get
used to the way pygame works. Gameplay is pretty similar,
but there are a lot less object types to worry about,
and it makes no attempt at using the optional pygame
modules.
It does provide a good method for using the updaterects
to only update the changed parts of the screen, instead of
the entire screen surface. This has large speed benefits
and should be used whenever the fullscreen isn't being changed."""


#import
import random, os.path, sys
import pygame
from pygame.locals import *

if not pygame.image.get_extended():
    raise SystemExit("Requires the extended image loading from SDL_image")


#constants
FRAMES_PER_SEC = 40
PLAYER_SPEED   = 12
BADGUY_SPEED    = 12
SCREENRECT     = Rect(0, 0, 640, 480)


#some globals for friendly access
dirtyrects = [] # list of update_rects
next_tick = 0   # used for timing
class Img: pass # container for images
main_dir = os.path.split(os.path.abspath(__file__))[0]  # Program's diretory


#first, we define some utility functions

def load_image(file, transparent):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' %
                         (file, pygame.get_error()))
    if transparent:
        corner = surface.get_at((0, 0))
        surface.set_colorkey(corner, RLEACCEL)
    return surface.convert()



# The logic for all the different sprite types

class Actor:
    "An enhanced sort of sprite class"
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def update(self):
        "update the sprite state for this frame"
        pass

    def draw(self, screen):
        "draws the sprite into the screen"
        r = screen.blit(self.image, self.rect)
        dirtyrects.append(r)

    def erase(self, screen, background):
        "gets the sprite off of the screen"
        r = screen.blit(background, self.rect, self.rect)
        dirtyrects.append(r)


class Player(Actor):
    "Cheer for our hero"
    def __init__(self):
        Actor.__init__(self, Img.player)
        self.rect.centerx = SCREENRECT.centerx
        self.rect.bottom = SCREENRECT.bottom - 10

    def move(self, direction):
        self.rect = self.rect.move(direction[0]*PLAYER_SPEED, direction[1]*PLAYER_SPEED).clamp(SCREENRECT)


class BadGuy(Actor):
    "Destroy him or suffer"
    def __init__(self, startPos, startDir = 1):
        Actor.__init__(self, Img.badGuy)
        #self.facing = random.choice((-1,1)) * BADGUY_SPEED
        #if self.facing < 0:
        #    self.rect.right = SCREENRECT.right
        self.facing = startDir*BADGUY_SPEED
        self.rect.left = startPos[0]
        self.rect.top = startPos[1]


    def update(self):
        global SCREENRECT
        self.rect[0] = self.rect[0] + self.facing
        if not SCREENRECT.contains(self.rect):
            self.facing = -self.facing;
            self.rect = self.rect.clamp(SCREENRECT)

def update_hit_count():
    pass
    

def main():
    "Run me for adrenaline"
    global dirtyrects
    hitCount = 0

    # Initialize SDL components
    pygame.init()
    pygame.display.set_caption('Space Spider')
    screen = pygame.display.set_mode(SCREENRECT.size, 0)
    clock = pygame.time.Clock()

    # Load the Resources
    Img.background = load_image('background.gif', 0)
    Img.badGuy = load_image('megaman spider.gif', 1)
    Img.player = load_image('small ship.gif', 1)

    # Create the background
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, Img.background.get_width()):
        background.blit(Img.background, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    # Initialize Game Actors
    player = Player()
    badGuys = [BadGuy((100, 150)), BadGuy((100, 75), -1), BadGuy((200, 300))]

    # Main loop
    while True:
        clock.tick(FRAMES_PER_SEC)

        # Gather Events
        pygame.event.pump()
        keystate = pygame.key.get_pressed()
        if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
            break

        # Clear screen and update actors
        for actor in [player] + badGuys:
            actor.erase(screen, background)
            actor.update()

        # Move the player
        direction = (keystate[K_RIGHT] - keystate[K_LEFT], keystate[K_DOWN] - keystate[K_UP])
        player.move(direction)

        # Detect collisions
        badGuyrects = []
        for a in badGuys:
            badGuyrects.append(a.rect)



        hit = player.rect.collidelist(badGuys)
        if hit != -1:
            hitCount += 1
            #badGuy = badGuys[hit]
            #badGuys.remove(badGuy)


        # Draw everybody
        for actor in [player] + badGuys:
            actor.draw(screen)

        pygame.display.update(dirtyrects)
        dirtyrects = []

    pygame.time.wait(50)


#if python says run, let's run!
if __name__ == '__main__':
    main()
