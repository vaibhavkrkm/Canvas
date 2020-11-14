import pygame
import colors
import tkinter as tk
import sys
from pathlib import Path
import os
import winsound


class Grid:
	selected_color = colors.earth_green

	def __init__(self, cell_size):
		self.cell_size = cell_size
		self.rows = SCREENHEIGHT // self.cell_size
		self.cols = SCREENWIDTH // self.cell_size
		self.cell_data = {}
		self.cell_data_temp = {}

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
		try:
			for CELL in self.cell_data:
				self._fill(game_display, CELL[0], CELL[1], self.cell_data[CELL])
		except Exception as e:
			winsound.PlaySound("*", winsound.SND_ASYNC)
			corrupted_file_dialog(e)
			self.cell_data = self.cell_data_temp

	def clear_cells(self):
		self.cell_data.clear()

	def grid_events(self, surface):
		mouse_click = pygame.mouse.get_pressed()
		selected_col = selected_row = None
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

			if(mouse_click[0] == 1):
				self.cell_data[(selected_row, selected_col)] = Grid.selected_color
			elif(mouse_click[1] == 1):
				cell_color = None
				delta_row = delta_col = 0
				working_row = cell_row = selected_row
				working_col = cell_col = selected_col
				try:
					if(self.cell_data[(selected_row, selected_col)] != Grid.selected_color):
						cell_color = self.cell_data[(selected_row, selected_col)]
				except KeyError:
					cell_color = colors.white
				delta_row = -1
				delta_col = -1
				for i in range(0, 2):
					while True:
						try:
							if(self.cell_data[(working_row, working_col)] != cell_color or (working_row > grid.rows - 1 or working_row < 0)):
								delta_row *= -1
								working_row = cell_row + 1
								break
						except KeyError:
							if(colors.white != cell_color or (working_row > grid.rows - 1 or working_row < 0)):
								delta_row *= -1
								working_row = cell_row + 1
								break
						for j in range(0, 2):
							while True:
								try:
									if(self.cell_data[(working_row, working_col)] != cell_color or (working_col > grid.cols - 1 or working_col < 0)):
										delta_col *= -1
										working_col = cell_col + 1
										break
								except KeyError:
									if(colors.white != cell_color or (working_col > grid.cols - 1 or working_col < 0)):
										delta_col *= -1
										working_col = cell_col + 1
										break

								# fill
								self.cell_data[(working_row, working_col)] = Grid.selected_color

								working_col += delta_col

						working_row += delta_row
						working_col = cell_col
			elif(mouse_click[2] == 1):
				self.cell_data.pop((selected_row, selected_col), None)

	@classmethod
	def set_color(cls, color):
		cls.selected_color = color


class Tool:
	def __init__(self, cmds_list, x, y, width, height, color=colors.white, caption="", border = 0):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.cmds_list = cmds_list
		self.color = color
		self.caption = caption
		self.border = border
		if(self.caption != ""):
			self.text_surface = BASIC_FONT.render(self.caption, True, colors.black)
		else:
			self.text_surface = None

	def execute(self):
		for CMD in self.cmds_list:
			eval(CMD)

	def draw(self, surface):
		pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), self.border)
		if(self.text_surface is not None):
			surface.blit(self.text_surface, (self.x + self.width // 2 - self.text_surface.get_width() // 2, self.y + self.height // 2 - self.text_surface.get_height() // 2))

	def tool_events(self):
		mouse_click = pygame.mouse.get_pressed()
		if(mouse_click[0] == 1):
			mouse_pos = pygame.mouse.get_pos()
			if(mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height):
				self.execute()


def QUIT():
	pygame.quit()
	sys.exit()


def get_screen_size(tk_root):
	width = tk_root.winfo_screenwidth()
	height = tk_root.winfo_screenheight()
	return width, height


def corrupted_file_dialog(e):
	root = tk.Tk()
	root.resizable(False, False)
	root.title("Corrupted File Detected!")
	screen_size = get_screen_size(root)
	root.geometry(f"600x150+{screen_size[0] // 2 - 300}+{screen_size[1] // 2 - 75}")

	label_corrupted_info = tk.Label(root, text="Sorry, the file you're looking for seems bad/corrupted in some way!")
	label_corrupted_info.pack()

	label_corrupted_exception = tk.Label(root, text="EXCEPTION : " + str(e))
	label_corrupted_exception.pack()

	button_ok = tk.Button(root, text="OK", command=root.destroy)
	button_ok.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def update_color_text(text_surface):
	global color_text
	color_text = text_surface


def load():
	def load_project():
		global current_file_name
		cvp_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".cvp")
		try:
			with open(os.path.join(cvp_path), 'r') as f:
				grid.cell_data_temp = grid.cell_data
				try:
					cell_data = eval(f.read())
					grid.cell_data = cell_data
					current_file_name = entry_file_name.get()
					set_title()
				except Exception as e:
					winsound.PlaySound("*", winsound.SND_ASYNC)
					corrupted_file_dialog(e)

			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Load Project...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_projects_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()

	button_load = tk.Button(root, text="Load .CVP (Canvas Project)", command=load_project)
	button_load.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def save():
	def save_project():
		global current_file_name
		cvp_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".cvp")
		try:
			with open(os.path.join(cvp_path), 'w') as f:
				f.write(repr(grid.cell_data))
				current_file_name = entry_file_name.get()
				set_title()

			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Save Project...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_projects_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()
	entry_file_name.insert(0, current_file_name)

	button_save = tk.Button(root, text="Save .CVP (Canvas Project)", command=save_project)
	button_save.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


def export():
	def export_png():
		png_path = os.path.join(entry_file_path.get(), entry_file_name.get() + ".png")
		sub_surface = game_display.subsurface((0, 0, SCREENWIDTH, SCREENHEIGHT))
		try:
			pygame.image.save(sub_surface, png_path)
			root.destroy()
		except Exception:
			winsound.PlaySound("*", winsound.SND_ASYNC)

	root = tk.Tk()
	root.resizable(False, False)
	screen_size = get_screen_size(root)
	root.geometry(f"400x200+{screen_size[0] // 2 - 200}+{screen_size[1] // 2 - 100}")
	root.title("Export .PNG...")

	label_file_path = tk.Label(root, text="File Path : ")
	label_file_path.pack()

	entry_file_path = tk.Entry(root)
	entry_file_path.insert(0, canvas_path)
	entry_file_path.pack()

	label_file_name = tk.Label(root, text="File Name : ")
	label_file_name.pack()

	entry_file_name = tk.Entry(root)
	entry_file_name.pack()

	button_export = tk.Button(root, text="Export .PNG", command=export_png)
	button_export.pack()

	root.call("wm", "attributes", '.', "-topmost", '1')
	root.mainloop()


pygame.init()

# constants
SCREENWIDTH = 1080
SCREENHEIGHT = 600
FPS = 120
CLOCK = pygame.time.Clock()
BASIC_FONT = pygame.font.SysFont("comicsans", 40)

# making the game display surface
game_display = pygame.display.set_mode((SCREENWIDTH + 300, SCREENHEIGHT))

# current file name variable
current_file_name = "New Canvas Project"

# setting the title
set_title = lambda: pygame.display.set_caption(f"{current_file_name} - Canvas")
set_title()

# creating the empty grid of size 20 ppc (px. per cell)
grid = Grid(20)

# loading drawing pointer images
pencil_surface = pygame.image.load("pencil.png").convert_alpha()
eraser_surface = pygame.transform.scale(pygame.image.load("eraser.png").convert_alpha(), (48, 48))
fill_bucket_surface = pygame.transform.scale(pygame.image.load("fill.png").convert_alpha(), (48, 48))

# creating tools
# colors
color_red = Tool(["Grid.set_color(colors.really_red)", "update_color_text(BASIC_FONT.render('Red', True, colors.really_red))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 1, 50, 50, colors.really_red)
color_green = Tool(["Grid.set_color(colors.earth_green)", "update_color_text(BASIC_FONT.render('Green', True, colors.earth_green))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 1, 50, 50, colors.earth_green)
color_blue = Tool(["Grid.set_color(colors.really_blue)", "update_color_text(BASIC_FONT.render('Blue', True, colors.really_blue))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 3, 50, 50, colors.really_blue)
color_pink = Tool(["Grid.set_color(colors.bright_pink)", "update_color_text(BASIC_FONT.render('Pink', True, colors.bright_pink))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 3, 50, 50, colors.bright_pink)
color_purple = Tool(["Grid.set_color(colors.purple)", "update_color_text(BASIC_FONT.render('Purple', True, colors.purple))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 5, 50, 50, colors.purple)
color_yellow = Tool(["Grid.set_color(colors.bright_yellow)", "update_color_text(BASIC_FONT.render('Yellow', True, colors.bright_yellow))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 5, 50, 50, colors.bright_yellow)
color_toothpaste = Tool(["Grid.set_color(colors.toothpaste)", "update_color_text(BASIC_FONT.render('Toothpaste', True, colors.toothpaste))"], SCREENWIDTH + 25 + 50 * 1, 0 + 50 * 7, 50, 50, colors.toothpaste)
color_cream = Tool(["Grid.set_color(colors.cream)", "update_color_text(BASIC_FONT.render('Cream', True, colors.cream))"], SCREENWIDTH + 25 + 50 * 3, 0 + 50 * 7, 50, 50, colors.cream)
# other tools
save_project = Tool(["save()"], SCREENWIDTH + 25 + 75, 0 + 50 * 9 - 25, 100, 35, colors.really_blue, "Save", 2)
open_project = Tool(["load()"], SCREENWIDTH + 25 + 75, 0 + 50 * 10 - 25, 100, 35, colors.really_blue, "Open", 2)
export_image = Tool(["export()"], SCREENWIDTH + 25 + 75, 0 + 50 * 11 - 25, 100, 35, colors.bright_pink, "Export", 2)

colors_tuple = (color_red, color_green, color_blue, color_pink, color_purple, color_yellow, color_toothpaste, color_cream)
other_tools_tuple = (save_project, open_project, export_image)

color_text = BASIC_FONT.render("Green", True, colors.earth_green)
clear_text_temp = BASIC_FONT.render("C : Clear", True, colors.really_red)
clear_text = pygame.transform.scale(clear_text_temp, (clear_text_temp.get_width() - 5, clear_text_temp.get_height() - 5))

# making directories and related variables
home_dir = str(Path.home())
canvas_path = os.path.join(home_dir, "Pictures", "Canvas")
canvas_projects_path = os.path.join(home_dir, "Documents", "Canvas Projects")
# Canvas directory
if(os.path.isdir(canvas_path)):
	pass
else:
	os.mkdir(canvas_path)
# Canvas projects directory
if(os.path.isdir(canvas_projects_path)):
	pass
else:
	os.mkdir(canvas_projects_path)

run = True
while run:
	# event section start
	for event in pygame.event.get():
		if(event.type == pygame.QUIT):
			QUIT()
		elif(event.type == pygame.KEYUP):
			if(event.key == pygame.K_c):
				grid.clear_cells()
	# event section end

	game_display.fill(colors.white)

	grid.grid_events(game_display)
	grid.draw(game_display, pygame.Color(255, 255, 255))
	grid.draw_cells(game_display)

	pygame.draw.line(game_display, colors.black, (SCREENWIDTH + 25, 0 + 25), (SCREENWIDTH + 25, SCREENHEIGHT - 25))

	# colors tuple iteration
	for COLOR_BUTTON in colors_tuple:
		COLOR_BUTTON.draw(game_display)
		COLOR_BUTTON.tool_events()

	# other tools iteration
	for OTHER_BUTTON in other_tools_tuple:
		OTHER_BUTTON.draw(game_display)
		OTHER_BUTTON.tool_events()

	# blitting text(s)
	game_display.blit(color_text, (SCREENWIDTH + 25 + 100, 0 + 25 - color_text.get_height() // 2))
	game_display.blit(clear_text, (SCREENWIDTH + 25 + 68, SCREENHEIGHT - 20 - clear_text.get_height() // 2))

	mouse_pos = pygame.mouse.get_pos()
	if(mouse_pos[0] <= SCREENWIDTH):
		pygame.mouse.set_visible(False)
		mouse_click = pygame.mouse.get_pressed()
		if(mouse_click[0] == 1):
			game_display.blit(pencil_surface, (mouse_pos[0], mouse_pos[1] - pencil_surface.get_height()))
		elif(mouse_click[1] == 1):
			game_display.blit(fill_bucket_surface, (mouse_pos[0], mouse_pos[1] - fill_bucket_surface.get_height()))
		elif(mouse_click[2] == 1):
			game_display.blit(eraser_surface, (mouse_pos[0], mouse_pos[1] - eraser_surface.get_height()))
		else:
			game_display.blit(pencil_surface, (mouse_pos[0], mouse_pos[1] - pencil_surface.get_height()))
	else:
		pygame.mouse.set_visible(True)

	pygame.display.update()
	CLOCK.tick(FPS)

pygame.quit()
quit()
