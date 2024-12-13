class Field:
    def __init__(self, size=208):
        """
        Initialize the field as a 2D grid.
        Each cell represents a 1-foot by 1-foot square.
        """
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]

    def display(self):
        """
        Display the field as a simple text-based grid.
        For now, we'll just print the first letter of the resource name if present.
        """
        for row in self.grid:
            print(" ".join(["." if cell is None else cell.name[0].upper() for cell in row]))