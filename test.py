import game, dill, random

print('file name : ', end = '')
file_name = input()

with open(file_name, 'rb') as f:
    agent = dill.load(f)

player = agent.get_best_player()

board = game.hexapawn(4, 4)

while True:
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
        break
    board.display()
    print('')