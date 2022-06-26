from common import *
from item import *

class Fly(Item):
	UP, DOWN = 1, -1
	direction = DOWN
	WING_UP = True
	sprite_wing_up = None
	sprite_wing_down = None
	dead = False
	got_caught = False

	def __init__(self, x, y, w, h, image_filename):
		super().__init__(x, y, w, h, image_filename)
		temp = pygame.image.load(os.path.join("res", str("fly_2.png"))).convert_alpha()
		self.sprite_wing_up = pygame.transform.scale(temp, (self.rect.w, self.rect.h))
		temp = pygame.image.load(os.path.join("res", str("fly.png"))).convert_alpha()
		self.sprite_wing_down = pygame.transform.scale(temp, (self.rect.w, self.rect.h))

	def reset(self):
		self.state = STATE_NORMAL
		self.dead = False
		self.got_caught = False
		self.rect.x = 100 * BLOCK_SIZE
		self.rect.y = 78 * BLOCK_SIZE - 29 * BLOCK_SIZE + 9 * BLOCK_SIZE

	def animate(self, speed = 0.25 * BLOCK_SIZE):
		if self.state == STATE_NORMAL:
			if self.direction == self.DOWN:
				if self.rect.y < 57 * BLOCK_SIZE:
					self.rect.y += speed
					self.image = self.sprite_wing_down
				else:
					self.direction = self.UP
					self.rect.y -= speed
	
			if self.direction == self.UP:
				if self.rect.y > 52 * BLOCK_SIZE:
					self.rect.y -= speed
					self.image = self.sprite_wing_up
				else:
					self.direction = self.DOWN
					self.rect.y += speed
		elif self.state == STATE_FLY_CAUGHT:
			self.rect.x -= BLOCK_SIZE
		elif self.state == STATE_FLY_EATEN:
			self.dead = True

	def draw(self):
		if not self.dead:
			Item.draw(self)
			self.animate()
			if not self.got_caught:
				if ctrl.right_key == True:
					self.move(1, 0)
				if ctrl.left_key == True:
					self.move(-1, 0)

	def check_got_caught(self, frog):
		self.got_caught = frog.tongue.rect.colliderect(self.rect)
		if self.got_caught:
			self.state = STATE_FLY_CAUGHT

	def check_got_eaten(self, frog):
		got_eaten = frog.rect.colliderect(self.rect)
		if got_eaten:
			self.state = STATE_FLY_EATEN
			return True
		return False