import pygame
import os

class CRT:
	def __init__(self, WIN, w, h):
		self.w, self.h = w, h
		self.image_scanlines = pygame.image.load(os.path.join('res', 'scanlines.png')).convert_alpha()
		#self.image_scanlines = pygame.transform.scale(self.image_scanlines, (w, h))
		self.image_tv = pygame.image.load(os.path.join('res', 'tv.png')).convert_alpha()
		self.image_tv = pygame.transform.scale(self.image_tv, (w, h))
		self.WIN = WIN

	def draw(self):
		self.WIN.blit(self.image_scanlines, (0, 0))
		self.WIN.blit(self.image_tv, (0, 0))