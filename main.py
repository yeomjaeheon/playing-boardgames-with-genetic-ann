import game, ann, random, dill, time, copy

#각 신경망이 받아들이는 보드의 값은 동일함, 보드 상태 평가는 흑색 진영을 기준으로 진행됨, 평가된 상태는 백색 진영의 경우 -1을 곱해 반전시킬 것
#speciation이 필요한지 고려해 볼 것

def play_game(player1, player2, width, height):
    players = [player1, player2]
    board = game.hexapawn(width, height)
    while True:
        moves = board.search_moves()
        tmp = -10 ** 10
        state_index = 0
        for i, m in enumerate(moves):
            g = players[board.game_counter % 2].prop(m['state'])[0] * [1, -1][board.game_counter % 2] #백색 진영의 경우는 상태 평가를 -1를 곱해 반전
            if tmp < g:
                state_index = i
                tmp = g
            elif tmp == g:
                if random.random() <= 0.5:
                    state_index = i
        if board.play(*moves[state_index]['move']):
            return board.game_counter % 2
        #board.display()
        #print(*moves[state_index]['move'])

class searching_space:
    def __init__(self, num_ann, structure):
        self.num_ann, self.structure = num_ann, structure
        self.anns = []
        self.score = []
        for i in range(0, num_ann):
            self.anns.append(ann.ann(structure))
            self.score.append(1)

    def update(self):
        for i in range(0, self.num_ann):
            self.anns.append(ann.crossover(self.get_random_parent(), self.get_random_parent()))
            self.anns[-1].mut()
        del self.anns[:self.num_ann]
        self.score = [1 for i in range(0, self.num_ann)]

    def get_random_parent(self):
        n = random.randint(0, sum(self.score))
        s = 0
        for i in range(0, self.num_ann):
            s += self.score[i]
            if n <= s:
                return self.get(i)

    def get(self, index):
        return self.anns[index]

    def reward(self, index):
        self.score[index] += 1

    def get_best_player(self):
        index = 0
        tmp = 0
        for i in range(0, self.num_ann):
            if tmp < self.score[i]:
                tmp = self.score[i]
                index = i
        return self.anns[index]

savings = []
generation = 30
population = 300
width, height = 4, 4
agent = searching_space(population, [width * height, 30, 30, 1])
savings.append(copy.deepcopy(agent))
time_takes = 0

try:
    with open('ints', 'rb') as f:
        intermediate_storage = dill.load(f)
    if intermediate_storage[-1].structure == agent.structure and len(intermediate_storage) < generation:
        print('이전 진행 과정을 이어서 진행(Y/N)', end = '')
        if input() == 'Y':
            mode = 'prev'
        else:
            mode = 'new'
    
except:
    mode = 'new'

if mode == 'new':
    for i in range(0, generation):
        t = time.time()
        for j in range(0, population):
            if (j + 1) % 10 == 0:
                print('{0}세대 : {1}/{2} 완료'.format(i + 1, j + 1, population))
            for k in range(j + 1, population):
                winner = play_game(agent.get(j), agent.get(k), width, height)
                agent.reward([j, k][winner])
        agent.update()
        savings.append(copy.deepcopy(agent))
        with open('ints', 'wb') as f:
            dill.dump(savings, f)
        time_takes += (time.time() - t)
        print('{0}세대 : 저장 완료, {1}분 경과, {2}분 남음(예상)'.format(i + 1, (time.time() - t) / 60, (time_takes / (i + 1)) * (generation - (i + 1)) / 60))
    with open('gen{0}_{1}_{2}'.format(generation, width, height), 'wb') as f:
        dill.dump(savings, f)

elif mode == 'prev':
    for i in range(len(intermediate_storage) - 1, generation):
        t = time.time()
        for j in range(0, population):
            if (j + 1) % 10 == 0:
                print('{0}세대 : {1}/{2} 완료'.format(i + 1, j + 1, population))
            for k in range(j + 1, population):
                winner = play_game(agent.get(j), agent.get(k), width, height)
                agent.reward([j, k][winner])
        agent.update()
        intermediate_storage.append(copy.deepcopy(agent))
        with open('ints', 'wb') as f:
            dill.dump(intermediate_storage, f)
        time_takes += (time.time() - t)
        print('{0}세대 : 저장 완료, {1}분 경과, {2}분 남음(예상)'.format(i + 1, (time.time() - t) / 60, (time_takes / (i + 1)) * (generation - (i + 1)) / 60))
    with open('gen{0}_{1}_{2}'.format(generation, width, height), 'wb') as f:
        dill.dump(intermediate_storage, f)