import numpy as np
from copy import deepcopy

BOARD_SIZE = 8
BLACK = 1
WHITE = 2

def valid_pos(pos):
    return pos[0] >= 0 and pos[0] < 8 and pos[1] >= 0 and pos[1] < 8

def move(pos, dx, dy):
    return (pos[0] + dx, pos[1] + dy)

def neighbors(pos):
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighbor = move(pos, dx, dy)
            if valid_pos(neighbor):
                yield neighbor

class GameState(object):

    def __init__(self, board, turn=BLACK, edge=None):
        self.board = board
        self.turn = turn
        if edge:
            self.edge = edge
        else:
            self.edge = set()
        for piece in self.board:
            for neighbor in neighbors(piece):
                if neighbor not in self.board:
                    self.edge.add(neighbor)

    def _bookend(self, pos, dx, dy):
        next_pos = move(pos, dx, dy)
        first_neighbor = self.board.get(next_pos)
        if not first_neighbor or first_neighbor == self.turn or not valid_pos(next_pos):
            return None

        betweens = [next_pos]
        while True:
            next_pos = move(next_pos, dx, dy)
            if not valid_pos(next_pos):
                return None
            next_neighbor = self.board.get(next_pos)
            if not next_neighbor:
                return None
            elif next_neighbor == self.turn:
                return next_pos, betweens
            else:
                betweens.append(next_pos)



    def _bookends(self, pos):
        bookends = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                bookend = self._bookend(pos, dx, dy)
                if bookend:
                    bookends.append(bookend)
        return bookends

    def play(self, pos):
        bookends = self._bookends(pos)
        if not bookends:
            raise Exception("Cannot play there")

        # TODO (mitchg) - this would use less memory in a functional language because caching?
        new_board = deepcopy(self.board)
        new_edge = deepcopy(self.edge)

        new_board[pos] = self.turn
        for _, betweens in bookends:
            for between in betweens:
                new_board[between] = self.turn

        new_edge.remove(pos)
        for neighbor in neighbors(pos):
            if not new_board.get(neighbor):
                new_edge.add(neighbor)

        return GameState(new_board, turn=WHITE if self.turn == BLACK else BLACK, edge=new_edge)

    def __str__(self):
        out = ''
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                out_char = {WHITE: 'W', BLACK: 'B'}.get(self.board.get((x,y)), ' ')
                out_char = out_char if (x,y) not in self.edge else '?'
                out += out_char + ' '
            out += '\n'
        return out
