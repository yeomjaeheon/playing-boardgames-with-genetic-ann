import game, dill, random

def convert(map, game_counter):
    if game_counter % 2 == 0:
        return map
    else:
        return [-map[i] for i in range(len(map) - 1, -1, -1)]

print('file name : ', end = '')
file_name = input()

print('width, height : ', end = '')
width, height = map(int, input().split())

print('color : ', end = '')
color = input()

with open(file_name, 'rb') as f:
    agents = dill.load(f)['data']

print(agents.score)

mode = 'best'

if mode == 'random':
    player = agents.get_random_parent()
elif mode == 'best':
    player = agents.get_best_player()

board = game.hexapawn(width, height)

while True:
    if color == 'black':
        print('move : ', end = '')
        move = map(int, input().split())
        if board.play(*move):
            print('you won')
            break
        board.display()
        print('')
        moves = board.search_moves()
        tmp = -10 ** 10
        state_index = 0
        for i, m in enumerate(moves):
            g = player.prop(convert(board.board, board.game_counter) + convert(m['state'], board.game_counter))[0]
            if tmp < g:
                state_index = i
                tmp = g
            elif tmp == g:
                if random.random() <= 0.5:
                    state_index = i
        if board.play(*moves[state_index]['move']):
            print('you lose')
            board.display()
            print('')
            break
        board.display()
        print('')

    if color == 'white':
        moves = board.search_moves()
        tmp = -10 ** 10
        state_index = 0
        for i, m in enumerate(moves):
            g = player.prop(convert(board.board, board.game_counter) + convert(m['state'], board.game_counter))[0]
            if tmp < g:
                state_index = i
                tmp = g
            elif tmp == g:
                if random.random() <= 0.5:
                    state_index = i
        if board.play(*moves[state_index]['move']):
            print('you lose')
            board.display()
            print('')
            break
        board.display()
        print('')
        print('move : ', end = '')
        move = map(int, input().split())
        if board.play(*move):
            print('you won')
            break
        board.display()
        print('')

input()