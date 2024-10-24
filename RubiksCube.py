class Face:
    def __init__(self, size, color):
        # initialize a face with all cells of size x size = color
        self.grid = [[color] * size for _ in range(size)]

    # limit rotation to only clockwise
    # if user wants ccw then we will do clockwise 3x
    def rotate(self):
        self.grid = [list(reversed(col)) for col in zip(*self.grid)]
    
    # FACE GETTERS
    def get_rightmost_col(self):
        rightmost_col = [self.grid[i][-1] for i in range(len(self.grid))]
        return list((rightmost_col))
    def get_leftmost_col(self):
        leftmost_col = [self.grid[i][0] for i in range(len(self.grid))]
        return list((leftmost_col))
    def get_top_row(self):
        return self.grid[0]
    def get_bot_row(self):
        return self.grid[-1]
    
    # FACE SETTERS
    def set_rightmost_col(self, right_col):
        for i in range(len(self.grid)):
            self.grid[i][-1] = right_col[i]
    def set_leftmost_col(self, left_col):
        for i in range(len(self.grid)):
            self.grid[i][0] = left_col[i]
    def set_top_row(self, row):
        self.grid[0] = row
    def set_bot_row(self, row):
        self.grid[-1] = row

class RubiksCube:
    # CONSTANT COLORS
    WHITE = "W"
    RED = "R"
    BLUE = "B"
    GREEN = "G"
    ORANGE  = "O"
    YELLOW = "Y"

    def __init__(self, size):
        self.size = size
        self.faces = {
            "Up": Face(size, self.WHITE),
            "Down": Face(size, self.YELLOW),
            "Front": Face(size, self.RED),
            "Back": Face(size, self.ORANGE),
            "Left": Face(size, self.GREEN),
            "Right": Face(size, self.BLUE)
        }
        # adjacent rows of bottom, left, top, right adjacent faces of given face
        self.face_adjacents = {
            "Up": ["Front", "Left", "Back", "Right"],
            "Down": ["Back", "Left", "Front", "Right"],
            "Front": ["Down", "Left", "Up", "Right"],
            "Back": ["Down", "Right", "Up", "Left"],
            "Left": ["Down", "Back", "Up", "Front"],
            "Right": ["Down", "Front", "Up", "Back"]
        }

    # dictionary to map the corresponding functions based on a given "face"
    # this returns the relative row of the adjacent faces that we need to manipulate/move to other adjacent 
    # sides uninvolved with the main face (this is to edit the surrounding faces not the current "face")
    def get_adjacent_face_functions(self, face):
        face_function_map = {
            "Up": [
                lambda f: self.faces[f].get_top_row(),
                lambda f: self.faces[f].get_top_row(),
                lambda f: self.faces[f].get_top_row(),
                lambda f: self.faces[f].get_top_row()
            ],
            "Down": [
                lambda f: self.faces[f].get_bot_row(),
                lambda f: self.faces[f].get_bot_row(),
                lambda f: self.faces[f].get_bot_row(),
                lambda f: self.faces[f].get_bot_row()
            ],
            "Front": [
                lambda f: self.faces[f].get_top_row(),
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_bot_row(),
                lambda f: self.faces[f].get_leftmost_col()
            ],
            "Back": [
                lambda f: self.faces[f].get_bot_row(),
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_top_row(),
                lambda f: self.faces[f].get_leftmost_col()
            ],
            "Left": [
                lambda f: self.faces[f].get_leftmost_col(),
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_leftmost_col(),
                lambda f: self.faces[f].get_leftmost_col()
            ],
            "Right": [
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_rightmost_col(),
                lambda f: self.faces[f].get_leftmost_col()
            ]
        }
        return face_function_map.get(face, [])
    
    # some rows are reversed due to the way I print and hold the cube on certain faces
    def set_adj_face_functions(self, face):
        face_function_map = {
            "Up": [
                lambda f, row: self.faces[f].set_top_row(row),
                lambda f, row: self.faces[f].set_top_row(row),
                lambda f, row: self.faces[f].set_top_row(row),
                lambda f, row: self.faces[f].set_top_row(row)
            ],
            "Down": [
                lambda f, row: self.faces[f].set_bot_row(row),
                lambda f, row: self.faces[f].set_bot_row(row),
                lambda f, row: self.faces[f].set_bot_row(row),
                lambda f, row: self.faces[f].set_bot_row(row)
            ],
            "Front": [
                lambda f, row: self.faces[f].set_top_row(list(reversed(row))),
                lambda f, row: self.faces[f].set_rightmost_col(row),
                lambda f, row: self.faces[f].set_bot_row(list(reversed(row))),
                lambda f, row: self.faces[f].set_leftmost_col(row)
            ],
            "Back": [
                lambda f, row: self.faces[f].set_bot_row(row),
                lambda f, row: self.faces[f].set_rightmost_col(list(reversed(row))),
                lambda f, row: self.faces[f].set_top_row(row),
                lambda f, row: self.faces[f].set_leftmost_col(list(reversed(row)))
            ],
            "Left": [
                lambda f, row: self.faces[f].set_leftmost_col(row),
                lambda f, row: self.faces[f].set_rightmost_col(list(reversed(row))),
                lambda f, row: self.faces[f].set_leftmost_col(list(reversed(row))),
                lambda f, row: self.faces[f].set_leftmost_col(row)
            ],
            "Right": [
                lambda f, row: self.faces[f].set_rightmost_col(list(reversed(row))),
                lambda f, row: self.faces[f].set_rightmost_col(row),
                lambda f, row: self.faces[f].set_rightmost_col(row),
                lambda f, row: self.faces[f].set_leftmost_col(list(reversed(row)))
            ]
        }
        return face_function_map.get(face, [])

    # rotates a face on the rubik's cube and adjusts all other faces accordingly
    def rotate_face_cw(self, face):
        # rotate the current face
        self.faces[face].rotate()

        # gets adjacent face names
        adjacent_faces = self.face_adjacents[face]
        # determine what set of functions we need depending on "face"
        get_face_functions = self.get_adjacent_face_functions(face)

        # get rows of interest from adjacent faces
        adjacent_rows = [get_face_functions[i](adjacent_faces[i]) for i in range(len(adjacent_faces))]
        # Rotate adjacent rows in circular fashion 
        # (the rows taken need to move to the next row in line because of the clockwise spin)
        new_rows = adjacent_rows[-1:] + adjacent_rows[:-1]  # Right shift

        # define setter functions for each face
        set_face_functions = self.set_adj_face_functions(face)

        # loop through adjacent_faces and new_rows, applying the setters
        for i in range(len(adjacent_faces)):
            set_face_functions[i](adjacent_faces[i], new_rows[i])

    # counter clockwise on a rubiks cube is = to 3 clockwise rotations
    def rotate_face_ccw(self, face):
        self.rotate_face_cw(face)
        self.rotate_face_cw(face)
        self.rotate_face_cw(face)

    # display rubiks cube
    def display(self):
        for name, face in self.faces.items():
            print(f"{name} Face:")
            for row in face.grid:
                print(" ".join(row))
            print()


cube = RubiksCube(3)

# Test the following moves
# clockwise spin on a rubiks cube is a spin to the right
# counterclockwise spin is a spin to the left (when holding the face towards you)
cube.rotate_face_cw("Front")
cube.rotate_face_cw("Up")
cube.rotate_face_cw("Down")
cube.rotate_face_cw("Left")
cube.rotate_face_cw("Left")
cube.rotate_face_cw("Right")
cube.rotate_face_cw("Back")
cube.rotate_face_ccw("Front")   # counter clockwise

# HOW THE CUBE FACES ARE DISPLAYED
###############################################################################
# FRONT = RED side (WHITE above, YELLOW below, GREEN left, BLUE right)
# UP = WHITE side (ORANGE, above, RED below, GREEN left, BLUE right)
# DOWN = YELLOW side (RED above, ORANGE below, GREEN left, BLUE right)
# LEFT = GREEN side (WHITE above, YELLOW below, ORANGE left, RED right)
# RIGHT = BLUE side (WHITE above, YELLOW below, RED left, ORANGE right)
# BACK = ORANGE side (WHITE above, YELLOW below, BLUE left, GREEN right)
cube.display()