"""
Clase del problema general
"""
from typing import List
from loguru import logger
from random import randint

from coating_mod_2d.block import Block


class CoatingMod2D:
    def __init__(
        self,
        name: str,
        num_blocks: int,
        space_width: int,
    ) -> None:
        self.name = name
        self.num_blocks = num_blocks
        self.space_width = space_width
        self.blocks = self.generate_blocks()
        self.info()

    def generate_blocks(self) -> List[Block]:
        """
        Genera los bloque n que entraran al espacio de diseño
        """
        new_blocks = []
        for n in range(self.num_blocks):
            block = Block(
                n = n+1,
                width = randint(1, int(self.space_width/1.8)),
                height = randint(1, int(self.space_width/1.8)),
            )
            new_blocks.append(block)
        return new_blocks

    def info(self) -> None:
        logger.info(self.__str__())

    def __repr__(self) -> str:
        return "CoatingMod2D({}, space_width: {}, num_block: {})".format(
            self.name,
            self.space_width,
            self.num_blocks
        )

    def __str__(self) -> str:
        return "CoatingMod2D({}, space_width: {}, num_block: {})".format(
            self.name,
            self.space_width,
            self.num_blocks
        )
