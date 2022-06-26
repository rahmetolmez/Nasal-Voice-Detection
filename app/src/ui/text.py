import pygame

class Text:
	FONT = None

	def __init__(
		self,
		x,
		y,
		WIN,
		text = 'Text',
		font_path = '',
		font_size = 32,
		text_color = (255, 255, 255),
		text_bg_color = None,
		center_align = False):

		pygame.init()
		self.x, self.y = x, y
		self.center_align = center_align
		self.WIN = WIN
		self.text = text
		self.font_path = font_path
		self.font_size = font_size
		self.text_color = text_color
		self.text_bg_color = text_bg_color

		self.FONT = pygame.font.Font(self.font_path, self.font_size)
		self.text_render = self.FONT.render(self.text, True, self.text_color, self.text_bg_color)
		self.text_rect = self.text_render.get_rect()
		self.text_rect.x, self.text_rect.y = self.x, self.y

		if self.center_align:
			self.x -= self.text_rect.w / 2
			self.text_rect.x -= self.text_rect.w / 2

	def draw(self):
		self.WIN.blit(self.text_render, self.text_rect)

	def set_text(self, text):
		self.text = text
		self.text_render = self.FONT.render(self.text, True, self.text_color)

	def set_color(self, color, bg_color):
		self.text_color = color
		self.text_bg_color = bg_color
		self.text_render = self.FONT.render(self.text, True, self.text_color, self.text_bg_color)

	def set_size(self, size):
		self.font_size = size
		self.FONT = pygame.font.Font(self.font_path, self.font_size)
		self.text_render = self.FONT.render(self.text, True, self.text_color)

	def set_pos(self, x, y):
		self.x, self.y = x, y
		self.text_rect.x, self.text_rect = self.x, self.y