import pygame
from ui import text

class Dialog_Box:

	CLOSE = 2

	def __init__(
		self,
		x,
		y,
		WIN,
		w = 30,
		h = 30,
		button_count = 1,
		bg_image_path = '',
		font_path = '',
		title_text = 'Dialog Box',
		title_center_align = False,
		title_font_size = 32,
		message_text = 'This is a dialog box.',
		message_font_size = 20,
		title_color = (255, 255, 255),
		message_color = (255, 255, 255)):

		self.x, self.y = x, y
		self.w, self.h = w, h
		self.WIN = WIN
		self. button_count = button_count
		self.bg_image_path = bg_image_path
		self.font_path = font_path
		self.title_text = title_text
		self.title_center_align = title_center_align
		self.title_font_size = title_font_size
		self.message_text = message_text
		self.message_font_size = message_font_size
		self.title_color = title_color
		self.message_color = message_color

		self.bg_image = pygame.image.load(self.bg_image_path).convert_alpha()
		self.bg_image = pygame.transform.scale(self.bg_image, (self.w, self.h))

		self.padding = 20
		if self.title_center_align:
			x = self.x + self.w / 2
		else:
			x = self.x + self.padding
		self.ui_title_text = text.Text(
			x = x,
			y = self.y + self.padding,
			WIN = self.WIN,
			text = self.title_text,
			font_path = self.font_path,
			font_size = self.title_font_size,
			text_color = self.title_color,
			text_bg_color = None,
			center_align = self.title_center_align)

	def draw(self):
		self.WIN.blit(self.bg_image, (self.x, self.y))
		self.ui_title_text.draw()

	def check_dialog_collision(self):
		x, y = pygame.mouse.get_pos()
		mouse_buttons = pygame.mouse.get_pressed()
		if ((x <= self.x + self.w) and (x >= self.x) and (y <= self.y + self.h) and (y >= self.y)):
			if mouse_buttons[0]:
				return 0
			else:
				return 1
		else:
			if mouse_buttons[0]:
				return self.CLOSE
			else:
				return 3