import random

import pygame
from pygame.locals import *
from const import *
from pacman import Pacman
from nodes import NodeGroup
from coins import CoinGroup
from ghosts import GhostGroup
from pause import Pause
import searchalgo
from text import TextGroup
from sprites import MazeSprites



class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.searchMode = 0




    def nextLevel(self):
            self.level += 1
            self.showEntities()
            self.pause.paused = True
            self.startGame()
            self.textgroup.updateLevel(self.level)

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.generateMap()
        self.mazesprites = MazeSprites("maze_rnd.txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level % 5)
        self.nodes = NodeGroup("maze_rnd.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        #self.nodes.setupTestNodes()
        #self.pacman = Pacman(self.nodes.nodeList[0])
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12, 14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15, 14), RIGHT)
        self.nodesAdjacent, self.weightsAdjacent = self.nodes.getAdjacent()
        try:
            self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26))
        except AttributeError:
            self.restartGame()
        self.coins = CoinGroup("maze_rnd.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2 + 11.5, 0 + 14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2 + 11.5, 3 + 14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0 + 11.5, 3 + 14))

        spawnkey = self.nodes.constructKey(2 + 11.5, 3 + 14)
        self.ghosts.setSpawnNode(self.nodes.nodesLUT[spawnkey])

    def update(self):
        dt = self.clock.tick(30)/1000.0
        self.textgroup.update(dt)
        self.pacman.update(dt)
        self.coins.update(dt)
        if not self.pause.paused:
         self.ghosts.update(dt)
         self.checkCoinEvents()
         self.checkGhostEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                     self.pause.setPause(playerPaused=True)
                     if not self.pause.paused:
                        self.textgroup.hideText()
                        self.showEntities()
                     else:
                        self.textgroup.showText(PAUSETXT)
                        self.hideEntities()
                elif event.key == K_z:
                    self.searchMode = (self.searchMode + 1) % 4

                elif event.key == K_r:
                    self.restartGame()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def restartGame(self):
            self.lives = 5
            self.level = 0
            self.pause.paused = True
            self.fruit = None
            self.startGame()
            self.score = 0
            self.textgroup.updateScore(self.score)
            self.textgroup.updateLevel(self.level)
            self.textgroup.showText(READYTXT)
    def resetLevel(self):
            self.pause.paused = True
            self.pacman.reset()
            self.ghosts.reset()
            self.textgroup.showText(READYTXT)
    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.coins.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        self.renderPaths(self.screen)
        pygame.display.update()

    def checkCoinEvents(self):
        coin = self.pacman.eatCoins(self.coins.coinList)
        if coin:
            self.coins.numEaten += 1
            self.updateScore(coin.points)
            self.coins.coinList.remove(coin)
            if coin.name == POWERCOIN:
                self.ghosts.startFreight()
            if self.coins.isEmpty():
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def renderPaths(self, screen):
        for num, ghost in enumerate(self.ghosts.ghosts):
            if self.searchMode == 1:
                searchalgo.draw(searchalgo.bfs(self.nodesAdjacent,
                                               ghost.target.position.asTuple(),
                                               self.pacman.target.position.asTuple(),
                                               self.weightsAdjacent), screen, num)
            elif self.searchMode == 2:
                searchalgo.draw(searchalgo.dfs(self.nodesAdjacent,
                                               ghost.target.position.asTuple(),
                                               self.pacman.target.position.asTuple(),
                                               self.weightsAdjacent), screen, num)
            elif self.searchMode == 3:
                searchalgo.draw(searchalgo.ucs(self.nodesAdjacent,
                                               ghost.target.position.asTuple(),
                                               self.pacman.target.position.asTuple(),
                                               self.weightsAdjacent), screen, num)

    def generateMap(self):
        r = open('maze1.txt', 'r')
        w = open('maze_rnd.txt', 'w')
        for line in r.read():
            for char in line:
                if char == '+':
                    if random.random() < 0.05:
                        w.write('1')
                    else:
                        w.write('+')
                else:
                    w.write(char)
        r.close()
        w.close()


if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()
