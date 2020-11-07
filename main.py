import pygame
import colors


class Grid:
	selected_color = colors.earth_green

	def __init__(self, cell_size):
		self.cell_size = cell_size
		self.rows = SCREENHEIGHT // self.cell_size
		self.cols = SCREENWIDTH // self.cell_size
		self.cell_data = {}

	def draw(self, surface, color):
		# drawing columns
		for col in range(0, self.cols + 1):
			pygame.draw.line(surface, color, (0 + self.cell_size * col, 0), (0 + self.cell_size * col, SCREENHEIGHT))

		# drawing rows
		for row in range(0, self.rows):
			pygame.draw.line(surface, color, (0, 0 + self.cell_size * row), (SCREENWIDTH, 0 + self.cell_size * row))

	def _fill(self, surface, row, col, color):
		surface.fill(color, (0 + self.cell_size * col, 0 + self.cell_size * row, self.cell_size + 1, self.cell_size + 1))

	def draw_cells(self, surface):
		for CELL in self.cell_data:
			self._fill(game_display, CELL[0], CELL[1], self.cell_data[CELL])

	def grid_events(self, surface):
		mouse_click = pygame.mouse.get_pressed()
		selected_col = selected_row = None
		if(mouse_click[0] == 1):
			mouse_pos = pygame.mouse.get_pos()
			if(mouse_pos[0] <= SCREENWIDTH and mouse_pos[1] < SCREENHEIGHT):
			
				# finding column
				for col in range(1, self.cols + 2):
					if(col * self.cell_size < mouse_pos[0]):
						continue
					else:
						selected_col = col - 1
						break

				# finding row
				for row in range(1, self.rows + 2):
					if(row * self.cell_size < mouse_pos[1]):
						continue
					else:
						selected_row = row - 1
						break

				# filling the cell
				# self._fill(game_display, selected_row, selected_col, colors.earth_green)
				self.cell_data[(selected_row, selected_col)] = Grid.selected_color

	@classmethod
	def set_color(cls, color):
		cls.selected_color = color


class Tool:
	def __init__(self, cmds_list, x, y, width, height, color = colors.white, caption = ""):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.cmds_list = cmds_list
		self.color = color
		self.caption = caption

	def execute(self):
		for CMD in self.cmds_list:
			eval(CMD)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

	def tool_events(self):
		mouse_click = pygame.mouse.get_pressed()
		if(mouse_click[0] == 1):
			mouse_pos = pygame.mouse.get_pos()
			if(mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height):
				self.execute()


def update_color_text(text_surface):
	global color_text
	color_text = text_surface


pygame.init()

# constants
SCREENWIDTH = 1080
SCREENHEIGHT = 600
FPS = 120
CLOCK = pygame.time.Clock()
BASIC_FONT = pygame.font.SysFont("comicsans", 40)

# making the game display surface
game_display = pygame.display.set_mode((SCREENWIDTH + 300, SCREENHEIGHT))

# setting the title
pygame.display.set_caption("Canvas")

# creating the empty grid of size 20 ppc (px. per cell)
grid = Grid(20)

# creating tools
color_red = Tool(["Grid.set_color(colors.really_red)", "update_color_text(BASIC_FONT.render('Red', True, colors.really_red))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 1, 50, 50, colors.really_red)
color_green = Tool(["Grid.set_color(colors.earth_green)", "update_color_text(BASIC_FONT.render('Green', True, colors.earth_green))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 1, 50, 50, colors.earth_green)
color_blue = Tool(["Grid.set_color(colors.really_blue)", "update_color_text(BASIC_FONT.render('Blue', True, colors.really_blue))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 3, 50, 50, colors.really_blue)
color_pink = Tool(["Grid.set_color(colors.bright_pink)", "update_color_text(BASIC_FONT.render('Pink', True, colors.bright_pink))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 3, 50, 50, colors.bright_pink)
color_purple = Tool(["Grid.set_color(colors.purple)", "update_color_text(BASIC_FONT.render('Purple', True, colors.purple))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 5, 50, 50, colors.purple)
color_yellow = Tool(["Grid.set_color(colors.bright_yellow)", "update_color_text(BASIC_FONT.render('Yellow', True, colors.bright_yellow))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 5, 50, 50, colors.bright_yellow)
color_toothpaste = Tool(["Grid.set_color(colors.toothpaste)", "update_color_text(BASIC_FONT.render('Toothpaste', True, colors.toothpaste))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 7, 50, 50, colors.toothpaste)
color_cream = Tool(["Grid.set_color(colors.cream)", "update_color_text(BASIC_FONT.render('Cream', True, colors.cream))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 7, 50, 50, colors.cream)

colors_tuple = (color_red, color_green, color_blue, color_pink, color_purple, color_yellow, color_toothpaste, color_cream)

color_text = BASIC_FONT.render("Green", True, colors.earth_green)

run = True
while run:
	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			pygame.quit()
			quit()
	# event section end

	game_display.fill(colors.white)

	grid.grid_events(game_display)
	grid.draw(game_display, pygame.Color(255, 255, 255))
	grid.draw_cells(game_display)

	pygame.draw.line(game_display, colors.black, (SCREENWIDTH + 25, 0 + 25), (SCREENWIDTH + 25, SCREENHEIGHT - 25))

	for COLOR_BUTTON in colors_tuple:
		COLOR_BUTTON.draw(game_display)
		COLOR_BUTTON.tool_events()

	game_display.blit(color_text, (SCREENWIDTH + 25 + 100, 0 + 25 - color_text.get_height() // 2))

	pygame.display.update()
	CLOCK.tick(FPS)

pygame.quit()
quit()
