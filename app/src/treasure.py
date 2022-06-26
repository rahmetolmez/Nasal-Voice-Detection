from common import *
from item import *

class Treasure(Item):
	UP, DOWN = 1, -1
	direction = DOWN

	def __init__(self, x, y, w, h, image_filename):
		super().__init__(x, y, w, h, image_filename)
		temp = pygame.image.load(os.path.join("res", str("treasure_chest.png"))).convert_alpha()
		self.sprite = pygame.transform.scale(temp, (self.rect.w, self.rect.h))

	def reset(self):
		self.state = STATE_NORMAL
		self.rect.x = 55 * BLOCK_SIZE
		self.rect.y = 110 * BLOCK_SIZE - 29 * BLOCK_SIZE

	def animate(self, speed = 0.25 * BLOCK_SIZE):
		'''if self.state == STATE_NORMAL:
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
					self.rect.y += speed'''
		a = 1

	def draw(self):
		Item.draw(self)
		self.animate()
		#if ctrl.right_key == True:
		#	self.move(1, 0)
		#if ctrl.left_key == True:
		#	self.move(-1, 0)

	def check_reached(self, diver):
		reached = diver.rect.colliderect(self.rect)
		if reached:
			#self.state = STATE_FLY_EATEN
			return True
		return False