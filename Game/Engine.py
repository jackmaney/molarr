import pygame
from Game.Shared.GameConstants import *
from Molarr import Molarr
from Candy import Candy
import sys
import warnings
import os


class Engine(object):

    def __init__(self):

        self.player = None
        self.playerGroup = None
        self.candies = pygame.sprite.Group()

        self.allCandies = [pygame.image.load(img) for img in CANDY_FILES]

        self.score = 0

        self.screen = None
        self.clock = None

        self.eventHandlers = [self.handleEvents]

        self.player = Molarr(self)

        self.pressedKeys = None

        pygame.init()
        pygame.mixer.init()

        impactSound = pygame.mixer.Sound(SOUND_IMPACT_FILE)

        self.sounds = {
            "impact": impactSound
        }

    def playSound(self, soundName):
        sound = self.sounds[soundName]
        sound.stop()
        sound.play()


    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

    def startGame(self):



        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.candies.add(Candy(self))
        print len(self.candies)

        while True:
            self.clock.tick(MAX_FPS)

            self.pressedKeys = pygame.key.get_pressed()

            handlers_to_remove = []
            events = pygame.event.get()

            for handler in self.eventHandlers:
                try:
                    handler(events)
                except Exception:
                    warnings.warn(
                        "WARNING: Found zombie event handler. Removing...")
                    handlers_to_remove.append(handler)

            self.screen.blit(BACKGROUND, (0, 0))

            self.player.update()
            self.candies.update()

            candidateCandies = pygame.sprite.spritecollide(self.player, self.candies, False)
            for candy in candidateCandies:
                if self.player.bodyRect().colliderect(candy.rect):
                    print "Body Blow!"
                elif self.player.isSwinging and self.player.hammerHeadRect().colliderect(candy.rect):
                    print "Hammer hit!"
                    self.playSound("impact")
                    candy.kill()
                    print len(self.candies)

            self.player.render()

            self.candies.draw(self.screen)

            pygame.display.update()
