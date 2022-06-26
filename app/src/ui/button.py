import pygame

class Button:
	RELEASED = 0
	CLICKED = 1
	HOVERED = 2

	def __init__(
		self,
		x,
		y,
		WIN,
		w = 50,
		h = 30,
		off_image = None,
		on_image = None,
		bg_image = None,
		on_click_function = None,
		text = 'Button',
		font_path = '',
		font_size = 32,
		text_color = (255, 255, 255)):

		self.x, self.y, self.w, self.h = x, y, w, h
		self.normal_y, self.clicked_y, self.hovered_y = self.y, self.y + 20, self.y + 5
		self.off_image, self.on_image, self.bg_image = off_image, on_image, bg_image
		self.WIN = WIN
		self.on_click_function = on_click_function
		self.on_image = pygame.image.load(self.on_image).convert_alpha()
		self.off_image = pygame.image.load(self.off_image).convert_alpha()
		self.on_image = pygame.transform.scale(self.on_image, (w, h))
		self.off_image = pygame.transform.scale(self.off_image, (w, h))
		self.state = self.RELEASED
		self.clicked_and_onclick_called = False

		# text
		self.text = text
		self.text_color = text_color
		self.font = pygame.font.Font(font_path, font_size)
		self.py_text = self.font.render(self.text, True, self.text_color)
		self.font_path = font_path
		self.font_size = font_size
		self.text_rect = self.py_text.get_rect()
		self.text_rect.x = self.x + self.w / 2 - self.text_rect.w / 2
		self.text_rect.y = self.y + self.h / 2 - self.text_rect.h / 2
		self.text_rect_normal = self.text_rect
		self.text_rect_clicked = self.py_text.get_rect()
		self.text_rect_clicked.x = self.text_rect.x
		self.text_rect_clicked.y = self.text_rect.y + 20
		self.text_rect_hovered = self.py_text.get_rect()
		self.text_rect_hovered.x = self.text_rect.x
		self.text_rect_hovered.y = self.text_rect.y + 5

	def draw(self):
		if self.state == self.RELEASED:
			self.y = self.normal_y
			self.text_rect = self.text_rect_normal
			self.WIN.blit(self.on_image, (self.x, self.y))
		elif self.state == self.HOVERED:
			self.y = self.hovered_y
			self.text_rect = self.text_rect_hovered
			self.WIN.blit(self.on_image, (self.x, self.y))
		elif self.state == self.CLICKED:
			self.y = self.clicked_y
			self.text_rect = self.text_rect_clicked
			self.WIN.blit(self.off_image, (self.x, self.y))
		self.WIN.blit(self.py_text, self.text_rect)



	def button_pressed(self):
		x, y = pygame.mouse.get_pos()
		if (x >= self.x) and (x <= self.x + self.w) and (y >= self.normal_y) and (y <= self.normal_y + self.h):
			mouse_buttons = pygame.mouse.get_pressed()
			if mouse_buttons[0]:
				if self.state == self.HOVERED:
					self.state = self.CLICKED
					return self.CLICKED
			else:
				if self.state == self.CLICKED:
					self.state = self.RELEASED
					if not self.clicked_and_onclick_called:
						self.on_click()
						self.clicked_and_onclick_called = True
				self.state = self.HOVERED
				self.clicked_and_onclick_called = False
				return self.HOVERED
		else:
			self.state = self.RELEASED
			self.clicked_and_onclick_called = False
			return self.RELEASED

	def on_click(self):
		if not self.on_click_function == None:
			self.on_click_function()

	def set_pos(self, x, y):
		self.x = x
		self.y = y 
		self.text_rect.x = self.x + self.w / 2 - self.text_rect.w / 2
		self.text_rect.y = self.y + self.h / 2 - self.text_rect.h / 2
		self.text_rect_normal = self.text_rect
		self.text_rect_clicked = self.py_text.get_rect()
		self.text_rect_clicked.x = self.text_rect.x
		self.text_rect_clicked.y = self.text_rect.y + 20
		self.text_rect_hovered = self.py_text.get_rect()
		self.text_rect_hovered.x = self.text_rect.x
		self.text_rect_hovered.y = self.text_rect.y + 5