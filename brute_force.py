from reversi import GameState, BLACK, WHITE

START_BOARD = {
    (3, 3): BLACK,
    (3, 4): WHITE,
    (4, 3): WHITE,
    (4, 4): BLACK,
}

def calc_score(gs):
    return sum([1 if x == BLACK else -1 for x in gs.board.values()])

def play_out(gs, depth=0, max_depth=4):
    if depth > max_depth:
        return calc_score(gs)

    playable = False
    max_score = 0

    for pos in gs.edge:
        try:
            sub_gs = gs.play(pos)
            sub_max_score = play_out(sub_gs, depth=depth+1, max_depth=max_depth)
            max_score = max(max_score, sub_max_score)
            playable = True
        except:
            pass

    if not playable:
        return calc_score(gs)
    else:
        return max_score

def best_move(gs):
    best_pos = None
    best_score = None
    for pos in gs.edge:
        try:
            sub_gs = gs.play(pos)
            sub_best_score = play_out(sub_gs)
            if not best_pos or sub_best_score > best_score:
                best_pos = pos
                best_score = sub_best_score
        except:
            pass

    return best_pos, best_score

black_wins = 0
white_wins = 0
gs = GameState(START_BOARD)

while True:
    print(gs)
    best_pos, score = best_move(gs)
    print(f'Best move: {best_pos} {score}')
    gs = gs.play(best_pos)
    print(gs)
    while True:
        opponent_move = eval(input('Opponent:'))
        try:
            gs = gs.play(opponent_move)
            break
        except:
            pass
