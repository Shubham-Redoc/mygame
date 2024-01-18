import pygame as pg
import sys
import random

import asyncio

pg.mixer.init()
pg.font.init()

pg.display.set_caption("Pygame Web Test")

class Player:
	def __init__(self,game) -> None:
		self.game = game
		self.spr = pg.image.load("player.png").convert_alpha()
		self.rect = pg.rect.Rect(100,100,self.spr.get_width(),self.spr.get_height())
		self.sound = pg.mixer.Sound("sound.ogg")
		self.score = 0
		self.coinspr = pg.image.load("coin.png").convert_alpha()
		self.coinrect = pg.rect.Rect(random.randint(40,450),random.randint(40,450),self.coinspr.get_width(),self.coinspr.get_height())
	def draw(self):
		self.game.screen.blit(self.spr,self.rect.topleft)

		self.game.screen.blit(self.coinspr,self.coinrect.topleft)

		self.game.screen.blit(self.game.font.render(str(self.score),False,'black'),(10,10))

		
	def move(self,dt):
		keys = pg.key.get_pressed()
		speed = 0.3
		if keys[pg.K_w] or keys[pg.K_UP]:
			self.rect.y += -speed *dt
		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.rect.x += -speed *dt
		if keys[pg.K_s] or keys[pg.K_DOWN]:
			self.rect.y += speed *dt
		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.rect.x += speed *dt

		if self.rect.colliderect(self.coinrect):
			self.score += 1
			self.sound.play() #play coin pickup sound
			self.coinrect.x,self.coinrect.y = random.randint(40,450),random.randint(40,450)

	

		

class Game:
	def __init__(self) -> None:
		self.screen = pg.display.set_mode((512,512))
		self.clock = pg.time.Clock()
		self.player = Player(self)
		self.font = pg.font.Font("FFFFORWA.TTF",24)
		self.dt = 1

	def draw(self):
		self.screen.fill('grey')

		self.player.draw()

	def update(self):
		self.player.move(self.dt)

	async def run(self):

		while True:
			self.dt = self.clock.tick(60)
			
			for key in pg.event.get():
				if key.type == pg.QUIT:
					sys.exit()

			self.update()
			self.draw()

			pg.display.update()
			await asyncio.sleep(0)

if __name__ == '__main__':
	app = Game()
	#app.run()
	asyncio.run(app.run())
