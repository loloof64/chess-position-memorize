from tkinter import *

class MainWindow(Tk):

	PICTURES_SIZE = 40

	def __init__(self):
		Tk.__init__(self)
		self.winfo_toplevel().title("Chess Position Memorize")
		self._add_widgets()

		self._pieces_images_list = []
		self.load_position("c8f4", "  k / ppp/    /QB R/    ")

		self._update_board()

	def load_position(self, corner_cells, pieces):
		self._pieces = pieces
		self._corner_cells = corner_cells
		self._pieces_codes = list(map(lambda x: list(x), self._pieces.split("/")))
		self._update_board()

	def _add_widgets(self):
		self._canvas = Canvas(self,
			width=MainWindow.PICTURES_SIZE*9,
			height=MainWindow.PICTURES_SIZE*9,
			bg = '#128812'
		)
		self._canvas.pack()

	def _update_board(self):
		self._canvas.delete("all")
		self._pieces_images_list[:] = []
		self._compute_board_size()
		self._compute_top_left_cell_absolute_coords()
		self._canvas.config(
			width = (self._board_size[0]+1) * MainWindow.PICTURES_SIZE,
			height = (self._board_size[1]+1) * MainWindow.PICTURES_SIZE
		)

		for cell_y in range(0, len(self._pieces_codes)):
			for cell_x in range(0, len(self._pieces_codes[cell_y])):
				self._draw_single_cell((cell_y, cell_x))

		self._create_piece_images()
		self._draw_cells_coordinates()

	def _compute_board_size(self):
		corner_cells_num = list(map(ord, self._corner_cells))
		width = corner_cells_num[2] - corner_cells_num[0] + 1
		height = corner_cells_num[1] - corner_cells_num[3] + 1
		self._board_size = (width, height)

	def _compute_top_left_cell_absolute_coords(self):
		corner_cells_num = list(map(ord, self._corner_cells))
		self._top_left_cell_absolute_coords = (
			corner_cells_num[1] - ord('1'),
			corner_cells_num[0] - ord('a')
		)

	def _draw_single_cell(self, cell_coord):
		absolute_coord = (
			cell_coord[1] - self._top_left_cell_absolute_coords[1],
			cell_coord[0] - self._top_left_cell_absolute_coords[0],
		)

		is_white_cell = (absolute_coord[0] + absolute_coord[1]) %2 != 0
		bg_color = '#f5f6ce' if is_white_cell else '#CD853F'

		square_y = (self._board_size[0] - cell_coord[0] + 0.5) * MainWindow.PICTURES_SIZE
		square_x = (cell_coord[1] + 0.5) * MainWindow.PICTURES_SIZE

		self._canvas.create_rectangle(
			square_x,
			square_y,
			square_x + MainWindow.PICTURES_SIZE,
			square_y + MainWindow.PICTURES_SIZE,
			fill = bg_color
		)

	def caesar_char(c, step):
		return chr(ord(c) + step)

	def _create_piece_images(self):
		for cell_y in range(0, len(self._pieces_codes)):
			for cell_x in range(0, len(self._pieces_codes[cell_y])):
				piece = self._pieces_codes[cell_y][cell_x]
				piece_image = self._piece_image_from_code(piece)

				if piece_image != "":
					picture = PhotoImage(file = piece_image)
					picture = picture.subsample(int(80 / MainWindow.PICTURES_SIZE))
					self._pieces_images_list.append(picture)
					square_y = (cell_y + 0.5) * MainWindow.PICTURES_SIZE
					square_x = (cell_x + 0.5) * MainWindow.PICTURES_SIZE
					self._canvas.create_image(square_x, square_y, image=picture, anchor = 'nw')

	def _draw_cells_coordinates(self):
		font = 'Arial 9 bold'
		letters_coll = [MainWindow.caesar_char(self._corner_cells[0], step).upper() for step in range(self._board_size[0])]
		for letter_index, letter in enumerate(letters_coll) :
			x = MainWindow.PICTURES_SIZE * (0.9 + letter_index)
			y1 = MainWindow.PICTURES_SIZE * 0.15
			y2 = MainWindow.PICTURES_SIZE * (0.65 + self._board_size[1])
			self._canvas.create_text(x,y1, text = letter, anchor='nw', font=font)
			self._canvas.create_text(x,y2, text = letter, anchor='nw', font=font)

		letters_coll = [MainWindow.caesar_char(self._corner_cells[3], step).upper() for step in range(self._board_size[1])]
		for letter_index, letter in enumerate(list(reversed(letters_coll))) :
			x1 = MainWindow.PICTURES_SIZE * 0.12
			x2 = MainWindow.PICTURES_SIZE * (0.62 + self._board_size[0])
			y = MainWindow.PICTURES_SIZE * (0.9 + letter_index)
			self._canvas.create_text(x1,y, text = letter, anchor='nw', font=font)
			self._canvas.create_text(x2,y, text = letter, anchor='nw', font=font)

	def _piece_image_from_code(self, piece):
		if piece == 'P':
			return "WhitePawn.png"
		if piece == 'N' :
			return "WhiteKnight.png"
		if piece == 'B' :
			return "WhiteBishop.png"
		if piece == 'R' :
			return "WhiteRook.png"
		if piece == 'Q' :
			return "WhiteQueen.png"
		if piece == 'K' :
			return "WhiteKing.png"
		if piece == 'p' :
			return "BlackPawn.png"
		if piece == 'n' :
			return "BlackKnight.png"
		if piece == 'b' :
			return "BlackBishop.png"
		if piece == 'r' :
			return "BlackRook.png"
		if piece == 'q' :
			return "BlackQueen.png"
		if piece == 'k' :
			return "BlackKing.png"
		return ""

if __name__ == "__main__":
	MainWindow().mainloop()
