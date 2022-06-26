from common import *
from item import *

class Frog(Item):
	tongue = None
	normal_image = None
	eyes_closed_image = None
	speed = 0
	eyes_closed, inhaled, jumped = False, False, False
	wink_start_time = None
	breathe_time = None
	last_breathe_time = None
	last_wink_time = None
	last_jump_time = None

	def __init__(self, x, y, w, h, image_filename, disable_tongue = False):
		super().__init__(x, y, w, h, image_filename)
		temp = pygame.image.load(os.path.join('res', str('frog.png'))).convert_alpha()
		self.normal_image = pygame.transform.scale(temp, (w, h))
		temp = pygame.image.load(os.path.join('res', str('frog_eyes_closed.png'))).convert_alpha()
		self.eyes_closed_image = pygame.transform.scale(temp, (w, h))
		self.tongue = Item(self.rect.x + 22 * BLOCK_SIZE, self.rect.y + 9 * BLOCK_SIZE, 1 * BLOCK_SIZE, 2 * BLOCK_SIZE, "frog_tongue.png")
		self.last_breathe_time = pygame.time.get_ticks()
		self.last_wink_time = pygame.time.get_ticks()
		self.last_jump_time = pygame.time.get_ticks()
		self.disable_tongue = disable_tongue

	#def init(self):
	#	speed = 0
	#	eyes_closed, inhaled, jumped = False, False, False
	#	wink_start_time = None
	#	breathe_time = None

	def reset(self):
		self.state = STATE_NORMAL

	def draw(self):
		if not self.disable_tongue:
			self.tongue.draw()
		#self.breathe()
		self.wink2()

		if self.state == STATE_NORMAL:
			if ctrl.d_key:
				self.tongue.image = pygame.transform.scale(self.tongue.image, (self.tongue.rect.w, self.tongue.rect.h))
				self.tongue.rect.w += 1
			elif ctrl.a_key:
				self.tongue.image = pygame.transform.scale(self.tongue.image, (self.tongue.rect.w, self.tongue.rect.h))
				self.tongue.rect.w -= 1
			if self.tongue.rect.w < BLOCK_SIZE:
				self.tongue.rect.w = BLOCK_SIZE
		elif self.state == STATE_FLY_CAUGHT:
			self.tongue.image = pygame.transform.scale(self.tongue.image, (self.tongue.rect.w, self.tongue.rect.h))
			self.tongue.rect.w -= 1 * BLOCK_SIZE
			if self.tongue.rect.w < BLOCK_SIZE:
				self.tongue.rect.w = BLOCK_SIZE
				if self.wink():
					self.state = STATE_NORMAL
				#if self.jump():
				#	self.state = STATE_NORMAL
				#	self.state = STATE_GAME_END


		Item.draw(self)

	def move(self, x, y):
		Item.move(self, x, y)
		self.tongue.move(x, y)

	def goto_pos(self, x, y):
		self.rect.x = x
		self.rect.y = y
		self.tongue.rect.x = self.rect.x + 22 * BLOCK_SIZE
		self.tongue.rect.y = self.rect.y + 9 * BLOCK_SIZE

	def check_fly_caught(self, fly):
		is_fly_caught = fly.rect.colliderect(self.tongue.rect)
		if is_fly_caught:
			self.state = STATE_FLY_CAUGHT

	# returns true if winking finished
	def wink(self):
		if not self.eyes_closed:
			self.wink_start_time = pygame.time.get_ticks()
			self.image = self.eyes_closed_image
			self.eyes_closed = True
			return False

		current_time = pygame.time.get_ticks()
		if (current_time - self.wink_start_time) / 1000 > 0.2:
			self.image = self.normal_image
			self.eyes_closed = False
			return True

	def breathe(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.last_breathe_time) / 1000 > 2:	
			if not self.inhaled:
				self.breathe_start_time = pygame.time.get_ticks()
				self.move(0, -1)
				self.inhaled = True
				return False
	
			if (current_time - self.breathe_start_time) / 1000 > 0.5:
				self.move(0, 1)
				self.inhaled = False
				self.last_breathe_time = current_time
				return True
			
	def wink2(self):
		current_time = pygame.time.get_ticks()
		if (current_time - self.last_wink_time) / 1000 > 2 + random.uniform(0, 1):	
			if not self.eyes_closed:
				self.wink_start_time = pygame.time.get_ticks()
				self.image = self.eyes_closed_image
				self.eyes_closed = True
				return False
	
			if (current_time - self.wink_start_time) / 1000 > 0.2:
				self.image = self.normal_image
				self.eyes_closed = False
				self.last_wink_time = current_time
				return True

	def jump(self):
		if not self.jumped:
			self.speed = -5
			self.jumped = True
			self.move(0, self.speed)
			return False
		
		self.speed -= GRAVITY
		self.move(0, self.speed)
		if self.rect.y > (78 * BLOCK_SIZE - 29 * BLOCK_SIZE):
			self.goto_pos(self.rect.x, (78 * BLOCK_SIZE - 29 * BLOCK_SIZE))
			self.jumped = False
			self.speed = 0
			return True