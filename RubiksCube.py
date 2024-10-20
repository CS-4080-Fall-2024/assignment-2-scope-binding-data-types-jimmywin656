# Class that represents a face of a Rubik's cube
class Face:
    def __init__(self, size, color):
        # Initialize a face with a grid of size 'size' and set it as color
        self.grid = [[color] * size for _ in range(size)]

    # Rotate face either clockwise (cw) or counterclockwise (ccw), default is clockwise
    def rotate(self, counter=False):
        if counter:
            self.grid = self.rotate_ccw()  # Call counterclockwise rotation if specified
        else:
            self.grid = self.rotate_cw()    # Otherwise, rotate clockwise

    def rotate_cw(self):
        # Rotate face 90 degrees clockwise
        return [list(reversed(col)) for col in zip(*self.grid)]

    def rotate_ccw(self):
        # Rotate face 90 degrees counterclockwise
        return [list(col) for col in reversed(list(zip(*self.grid)))]

    # Getter for the bottom row of the face
    def get_bot_row(self):
        return self.grid[-1][:]

    # Getter for the top row of the face
    def get_top_row(self):
        return self.grid[0][:]

    # Getter for the left column of the face
    def get_left_col(self):
        return [self.grid[i][0] for i in range(len(self.grid))]

    # Getter for the right column of the face
    def get_right_col(self):
        return [self.grid[i][-1] for i in range(len(self.grid))]

    # Setter for the bottom row of the face
    def set_bot_row(self, row):
        self.grid[-1] = row[:]

    # Setter for the top row of the face
    def set_top_row(self, row):
        self.grid[0] = row[:]

    # Setter for the left column of the face
    def set_left_col(self, col):
        for i in range(len(self.grid)):
            self.grid[i][0] = col[i]

    # Setter for the right column of the face
    def set_right_col(self, col):
        for i in range(len(self.grid)):
            self.grid[i][-1] = col[i]


# Class that represents a Rubik's cube
class RubiksCube:
    # Color constants for each face of the cube
    WHITE = "W"
    RED = "R"
    BLUE = "B"
    GREEN = "G"
    ORANGE = "O"
    YELLOW = "Y"

    def __init__(self, size):
        # Initialize the size of Rubik's cube (this determines the grid size of each face)
        self.size = size
        # Initialize the cube faces with their respective colors
        self.faces = {
            "Up": Face(size, self.WHITE),
            "Down": Face(size, self.YELLOW),
            "Front": Face(size, self.RED),
            "Back": Face(size, self.ORANGE),
            "Left": Face(size, self.GREEN),
            "Right": Face(size, self.BLUE)
        }

    def rotate_face(self, face, clockwise=True):
        # Rotate the specified face of the cube
        if face in self.faces:
            self.faces[face].rotate(counter=not clockwise)  # Rotate the face based on direction
        else:
            raise ValueError("Face does not exist")  # Raise an error if the face is invalid
        
        # Call appropriate function to update adjacent edges based on the rotated face
        if face == "Front":
            self.rotate_edges_front(clockwise)
        elif face == "Back":
            self.rotate_edges_back(clockwise)
        elif face == "Up":
            self.rotate_edges_up(clockwise)
        elif face == "Down":
            self.rotate_edges_down(clockwise)
        elif face == "Left":
            self.rotate_edges_left(clockwise)
        elif face == "Right":
            self.rotate_edges_right(clockwise)

    def rotate_edges_front(self, clockwise):
        """Updates the edges when rotating the front face."""
        if clockwise:
            # Store the bottom row of the Up face to rotate
            top_row = self.faces["Up"].get_bot_row()
            # Update edges accordingly
            self.faces["Up"].set_bot_row(self.faces["Left"].get_right_col()[::-1])
            self.faces["Left"].set_right_col(self.faces["Down"].get_top_row())
            self.faces["Down"].set_top_row(self.faces["Right"].get_left_col()[::-1])
            self.faces["Right"].set_left_col(top_row)
        else:
            # Perform counterclockwise edge updates
            top_row = self.faces["Up"].get_bot_row()
            self.faces["Up"].set_bot_row(self.faces["Right"].get_left_col())
            self.faces["Right"].set_left_col(self.faces["Down"].get_top_row()[::-1])
            self.faces["Down"].set_top_row(self.faces["Left"].get_right_col())
            self.faces["Left"].set_right_col(top_row[::-1])

    # Updating the adjacent edges when rotating the back face
    def rotate_edges_back(self, clockwise):
        if clockwise:
            # Store the top row of the Up face to rotate
            top_row = self.faces["Up"].get_top_row()
            # Update edges accordingly
            self.faces["Up"].set_top_row(self.faces["Right"].get_right_col())
            self.faces["Right"].set_right_col(self.faces["Down"].get_bot_row()[::-1])
            self.faces["Down"].set_bot_row(self.faces["Left"].get_left_col())
            self.faces["Left"].set_left_col(top_row[::-1])
        else:
            # Perform counterclockwise edge updates
            top_row = self.faces["Up"].get_top_row()
            self.faces["Up"].set_top_row(self.faces["Left"].get_left_col()[::-1])
            self.faces["Left"].set_left_col(self.faces["Down"].get_bot_row())
            self.faces["Down"].set_bot_row(self.faces["Right"].get_right_col()[::-1])
            self.faces["Right"].set_right_col(top_row)

    # Updating the adjacent edges when rotating the up face
    def rotate_edges_up(self, clockwise):
        if clockwise:
            # Store the top row of the Front face to rotate
            front_row = self.faces["Front"].get_top_row()
            # Update edges accordingly
            self.faces["Front"].set_top_row(self.faces["Right"].get_top_row())
            self.faces["Right"].set_top_row(self.faces["Back"].get_bot_row()[::-1])
            self.faces["Back"].set_bot_row(self.faces["Left"].get_top_row()[::-1])
            self.faces["Left"].set_top_row(front_row)
        else:
            # Perform counterclockwise edge updates
            front_row = self.faces["Front"].get_top_row()
            self.faces["Front"].set_top_row(self.faces["Left"].get_top_row())
            self.faces["Left"].set_top_row(self.faces["Back"].get_bot_row()[::-1])
            self.faces["Back"].set_bot_row(self.faces["Right"].get_top_row()[::-1])
            self.faces["Right"].set_top_row(front_row)

    # Updating the adjacent edges when rotating the down face
    def rotate_edges_down(self, clockwise):
        if clockwise:
            # Store the bottom row of the Front face to rotate
            front_row = self.faces["Front"].get_bot_row()
            # Update edges accordingly
            self.faces["Front"].set_bot_row(self.faces["Left"].get_bot_row())
            self.faces["Left"].set_bot_row(self.faces["Back"].get_top_row()[::-1])
            self.faces["Back"].set_top_row(self.faces["Right"].get_bot_row()[::-1])
            self.faces["Right"].set_bot_row(front_row)
        else:
            # Perform counterclockwise edge updates
            front_row = self.faces["Front"].get_bot_row()
            self.faces["Front"].set_bot_row(self.faces["Right"].get_bot_row())
            self.faces["Right"].set_bot_row(self.faces["Back"].get_top_row()[::-1])
            self.faces["Back"].set_top_row(self.faces["Left"].get_bot_row()[::-1])
            self.faces["Left"].set_bot_row(front_row)

    # Updating the adjacent edges when rotating the left face
    def rotate_edges_left(self, clockwise):
        if clockwise:
            # Store the left column of the Front face to rotate
            front_col = self.faces["Front"].get_left_col()
            # Update edges accordingly
            self.faces["Front"].set_left_col(self.faces["Up"].get_left_col())
            self.faces["Up"].set_left_col(self.faces["Back"].get_right_col()[::-1])
            self.faces["Back"].set_right_col(self.faces["Down"].get_left_col()[::-1])
            self.faces["Down"].set_left_col(front_col)
        else:
            # Perform counterclockwise edge updates
            front_col = self.faces["Front"].get_left_col()
            self.faces["Front"].set_left_col(self.faces["Down"].get_left_col())
            self.faces["Down"].set_left_col(self.faces["Back"].get_right_col()[::-1])
            self.faces["Back"].set_right_col(self.faces["Up"].get_left_col()[::-1])
            self.faces["Up"].set_left_col(front_col)

    # Updating the adjacent edges when rotating the right face
    def rotate_edges_right(self, clockwise):
        if clockwise:
            # Store the right column of the Front face to rotate
            front_col = self.faces["Front"].get_right_col()
            # Update edges accordingly
            self.faces["Front"].set_right_col(self.faces["Down"].get_right_col())
            self.faces["Down"].set_right_col(self.faces["Back"].get_left_col())
            self.faces["Back"].set_left_col(self.faces["Up"].get_right_col()[::-1])
            self.faces["Up"].set_right_col(front_col[::-1])
        else:
            # Perform counterclockwise edge updates
            front_col = self.faces["Front"].get_right_col()
            self.faces["Front"].set_right_col(self.faces["Up"].get_right_col())
            self.faces["Up"].set_right_col(self.faces["Back"].get_left_col()[::-1])
            self.faces["Back"].set_left_col(self.faces["Down"].get_right_col()[::-1])
            self.faces["Down"].set_right_col(front_col)

    # display rubiks cube
    def display(self):
        for name, face in self.faces.items():
            print(f"{name} Face:")
            for row in face.grid:
                print(" ".join(row))
            print()


# Example usage
cube = RubiksCube(3)
# cube.display()

# Test the following moves
cube.rotate_face("Front")
cube.rotate_face("Right")
cube.rotate_face("Up")
# cube.rotate_face("Up")
# cube.rotate_face("Left")
# cube.rotate_face("Down", clockwise=False)
cube.display()
