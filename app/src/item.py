from common import *

class Item:
	rect = None
	image = None
	state = STATE_NORMAL

	def __init__(self, x, y, w, h, image_filename, WIN = common.WIN):
		self.rect = pygame.Rect(WIN_HEIGHT / 2, 30, w, h)
		self.rect.x = x
		self.rect.y = y
		self.rect.w = w
		self.rect.h = h
		temp = pygame.image.load(os.path.join('res', str(image_filename))).convert_alpha()
		self.image = pygame.transform.scale(temp, (w, h))
		self.WIN = WIN

	def draw(self):
		self.WIN.blit(self.image, (self.rect.x, self.rect.y))

	def move(self, x, y):
		if self.rect.x + x + self.rect.w <= WIN_WIDTH:
			self.rect.x += x * BLOCK_SIZE
		if self.rect.y + y + self.rect.h <= WIN_HEIGHT:
			self.rect.y += y * BLOCK_SIZE