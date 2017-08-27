class TextDisplay:

	@staticmethod
	def init(surface, font, color):
		TextDisplay.surface = surface
		TextDisplay.font = font
		#TextDisplay.currentLine = 0
		TextDisplay.color = color
		TextDisplay.textLine = []

	@staticmethod
	def printline(msg):
		text_surface = TextDisplay.font.render(msg, True, TextDisplay.color)
		TextDisplay.textLine.append(text_surface)
		#TextDisplay.surface.blit(text_surface, (0, TextDisplay.currentLine))
		#TextDisplay.currentLine += text_surface.get_height()

	@staticmethod
	def display():
		currentLine = 0
		for text_surface in TextDisplay.textLine:
			TextDisplay.surface.blit(text_surface, (0, currentLine))
			currentLine += text_surface.get_height()
		TextDisplay.textLine = []
		#TextDisplay.currentLine = 0



if __name__ == "__main__":
	import pygame
	pygame.init()
	screen = pygame.display.set_mode((640, 480), 0, 32)
	font = pygame.font.SysFont("arial", 16)
	TextDisplay.init(screen, font, (0, 0, 255))

