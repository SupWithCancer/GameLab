import pygame
from vector import Vector2
from const import *
import numpy as np


class Coin(object):
    def __init__(self, row, column):
        self.name = COIN
        self.position = Vector2(column * TILEWIDTH, row * TILEHEIGHT)
        self.color = WHITE
        self.radius = int(4 * TILEWIDTH / 16)
        self.collideRadius = int(4 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)


class PowerCoin(Coin):
    def __init__(self, row, column):
        Coin.__init__(self, row, column)
        self.name = POWERCOIN
        self.radius = int(8 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0


class CoinGroup(object):
    def __init__(self, coinfile):
        self.coinList = []
        self.powerCoins = []
        self.createCoinList(coinfile)
        self.numEaten = 0

    def update(self, dt):
        for powercoin in self.powerCoins:
         powercoin.update(dt)

    def createCoinList(self, coinfile):
        data = self.readCoinfile(coinfile)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.coinList.append(Coin(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerCoin(row, col)
                    self.coinList.append(pp)
                    self.powerCoins.append(pp)

    def readCoinfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')

    def isEmpty(self):
        if len(self.coinList) == 0:
            return True
        return False

    def render(self, screen):
        for coin in self.coinList:
            coin.render(screen)


