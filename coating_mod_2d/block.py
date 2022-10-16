"""
Clase de bloque
"""

class Block:
    """
    Clase de bloque que se pondra en el espacio de trabajo
    """
    def __init__(
        self,
        n: int,
        width: int,
        height: int,
        left: int = None,
        bottom: int = None,
    ) -> None:
        self.n = n
        self.width = width
        self.height = height
        self.area = self.width * self.height
        if left is not None and bottom is not None:
            self.localize(left, bottom)
        else:
            self.left = None
            self.top = None
            self.right = None
            self.bottom = None

    def localize(self, left: int, bottom: int) -> None:
        """
        Localiza el bloque en una posicion
        """
        self.left = left
        self.bottom = bottom
        self.right = self.left + self.width - 1
        self.top = self.bottom + self.height - 1

    def rotate(self) -> None:
        """
        Rota el bloque
        """
        self.width, self.height = self.height, self.width
        if self.left is not None and self.bottom is not None:
            self.localize(self.left, self.bottom)

    def intersection(self, block2: "Block") -> bool:
        """
        Calcula si dos bloques se intersectan
        """
        return self.intersection_area(block2) > 0

    def intersection_area(self, block2: "Block") -> int:
        """
        calcula el area de la interseccion de dos bloques.
        """
        x_min = max(self.left, block2.left)   
        y_min = max(self.bottom, block2.bottom) 
        x_max = min(self.right, block2.right) 
        y_max = min(self.top, block2.top)     
        dx = max(x_max - x_min + 1, 0) 
        dy = max(y_max - y_min + 1, 0)
        return dx * dy

    def __repr__(self) -> str:
        return "Block(n: {}, width: {}, heigth: {}, [({}, {}), ({}, {})])".format(
            self.n,
            self.width,
            self.height,
            self.left,
            self.bottom,
            self.right,
            self.top
        )

    def __str__(self) -> str:
        return "Block(n: {}, width: {}, heigth: {}, [({}, {}), ({}, {})])".format(
            self.n,
            self.width,
            self.height,
            self.left,
            self.bottom,
            self.right,
            self.top
        )