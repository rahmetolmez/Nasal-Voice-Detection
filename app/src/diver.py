from common import *
from item import *

class Diver(Item):
	UP, DOWN = 1, -1
	direction = DOWN

	def __init__(self, x, y, w, h, image_filename):
		super().__init__(x, y, w, h, image_filename)
		temp = pygame.image.load(os.path.join("res", str("diver.png"))).convert_alpha()
		self.sprite = pygame.transform.scale(temp, (self.rect.w, self.rect.h))

	def reset(self):
		self.state = STATE_NORMAL
		self.rect.x = WIN_WIDTH / 2 + 23 * BLOCK_SIZE
		self.rect.y = 1 * BLOCK_SIZE

	def animate(self, speed = 0.25 * BLOCK_SIZE):
		if self.state == STATE_NORMAL:
			if self.direction == self.DOWN:
				if self.rect.y < 57 * BLOCK_SIZE:
					self.rect.x -= speed
					self.rect.y += speed
					self.image = self.sprite
				else:
					self.direction = self.UP
					self.rect.x += speed
					self.rect.y -= speed
	
			if self.direction == self.UP:
				if self.rect.y > 52 * BLOCK_SIZE:
					self.rect.x += speed
					self.rect.y -= speed
					self.image = self.sprite
				else:
					self.direction = self.DOWN
					self.rect.x -= speed
					self.rect.y += speed

	def draw(self):
		Item.draw(self)
		#self.animate()
		if ctrl.d_key:
			if ((self.rect.x - 0.25 * BLOCK_SIZE) > 0 and ((self.rect.x - 0.25 * BLOCK_SIZE) + self.rect.w) < WIN_WIDTH) and ((self.rect.y + 0.25 * BLOCK_SIZE) > 0 and ((self.rect.y + 0.25 * BLOCK_SIZE) + self.rect.h) < WIN_HEIGHT):
				self.move(-0.25, 0.25)
		elif ctrl.a_key:
			if ((self.rect.x + 0.25 * BLOCK_SIZE) > 0 and ((self.rect.x + 0.25 * BLOCK_SIZE) + self.rect.w) < WIN_WIDTH) and ((self.rect.y - 0.25 * BLOCK_SIZE) > 0 and ((self.rect.y - 0.25 * BLOCK_SIZE) + self.rect.h) < WIN_HEIGHT):
				self.move(0.25, -0.25)