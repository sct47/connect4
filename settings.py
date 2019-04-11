class Settings():

    def __init__(self):
        # Game board
        self.square = 100
        self.radius = int(self.square/2 -5)
        self.column_count = 7
        self.row_count = 6

        # Game pieces
        self.player_piece = 1
        self.ai_piece = 2
        self.empty = 0
        self.window_length = 4

        # turns
        self.player = 0
        self.ai = 1

        # Screen size
        self.width = 700
        self.height = 700

        # Board colours
        self.blue = (0,0,255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.yellow = (242,250,43)
        self.white = (255, 255, 255)


