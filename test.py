import game, dill, random

print('file name : ', end = '')
file_name = input()

print('width, height : ', end = '')
width, height = map(int, input().split())

print('color : ', end = '')
color = input()

with open(file_name, 'rb') as f:
    agents = dill.load(f)

print(len(agents))

#print(agents[-1].score)

mode = 'random'

if mode == 'random':
    player = agents[-1].get(random.randint(0, agents[-1].num_ann - 1))
elif mode == 'best':
    player = agents[-1].get_best_player()

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
            g = player.prop(m['state'])[0] * -1 #백색 진영의 경우는 상태 평가를 -1를 곱해 반전
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
            g = player.prop(m['state'])[0] * 1
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