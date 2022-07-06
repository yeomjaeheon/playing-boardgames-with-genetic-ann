import game, ann, random, dill, time, copy

#각 신경망이 다른 모든 신경망과 두 가지 진영 이상으로 경기를 하도록 수정할 것, n**2으로

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
        self.delay_counter = 0
        self.num_ann, self.structure = num_ann, structure
        self.anns = []
        self.score = []
        for i in range(0, num_ann):
            self.anns.append(ann.ann(structure))
            self.score.append(1)

    def update(self):
        threshold = 100000
        for i in range(0, self.num_ann):
            parent1 = self.get_random_parent()
            parent2 = self.get_random_parent()
            while ann.distance(parent1, parent2) > threshold:
                parent1 = self.get_random_parent()
                parent2 = self.get_random_parent()
            self.anns.append(ann.crossover(parent1, parent2))
            self.anns[-1].mut()
        del self.anns[:self.num_ann]
        self.score = [1 for i in range(0, self.num_ann)]
        if self.delay_counter > 2 * self.num_ann:
            print('지연 중({0}%), threshold를 높일 것'.format(self.delay_counter / (2 * self.num_ann) * 100))
        self.delay_counter = 0

    def get_random_parent(self):
        self.delay_counter += 1
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
        print(self.score[index])
        return self.anns[index]

width, height = 4, 4
generation = 100
population = 300
ann_structure = [width * height, 50, 1]

try:
    with open('intsto', 'rb') as f:
        backup = dill.load(f)
    
    if backup['gene_pool'][-1].structure == ann_structure and len(backup['gene_pool']) < generation:
        mode = 'prev'
    else:
        mode = 'new'
except:
    mode = 'new'

if mode == 'new':
    gene_pool = searching_space(population, ann_structure)
    savings = []
    for j in range(0, population):
        print('.', end = '')
        if (j + 1) % 10 == 0:
            print('')
            print('평가 중({0} / {1})'.format(j + 1, population))
        for k in range(0, population):
            if j != k:
                gene_pool.reward([j, k][play_game(gene_pool.get(j), gene_pool.get(k), width, height)])
    savings.append(copy.deepcopy(gene_pool))

    for i in range(0, generation):
        sum_time = 0
        t = time.time()

        gene_pool_next_generation = copy.deepcopy(savings[-1])
        gene_pool_next_generation.update()
        for j in range(0, population):
            print('.', end = '')
            if (j + 1) % 10 == 0:
                print('')
                print('평가 중({0} / {1})'.format(j + 1, population))
            for k in range(0, population):
                if j != k:
                    gene_pool_next_generation.reward([j, k][play_game(gene_pool_next_generation.get(j), gene_pool_next_generation.get(k), width, height)])
        
        while play_game(gene_pool_next_generation.get_best_player(), savings[-1].get_best_player(), width, height) != 0:
            print('삭제하고 새로운 세대 생성중')
            gene_pool_next_generation = copy.deepcopy(savings[-1])
            gene_pool_next_generation.update()
            for j in range(0, population):
                print('.', end = '')
                if (j + 1) % 10 == 0:
                    print('')
                    print('평가 중({0} / {1})'.format(j + 1, population))
                for k in range(0, population):
                    if j != k:
                        gene_pool_next_generation.reward([j, k][play_game(gene_pool_next_generation.get(j), gene_pool_next_generation.get(k), width, height)])
        
        savings.append(copy.deepcopy(gene_pool_next_generation))

        now = time.time()
        sum_time += (now - t)
        with open('intsto', 'wb') as f:
            dill.dump({'gene_pool' : savings, 'sum_time' : sum_time}, f)

        print('{0}세대 : 중간 저장 완료, 소요 시간 : {1}분, 남은 시간(예상) : {2}분'.format(i + 1, (now - t) / 60, sum_time / (i + 1) * (generation - (i + 1)) / 60))

elif mode == 'prev':
    print('중간 저장 파일을 이어서 진행')
    sum_time = backup['sum_time']
    savings = backup['gene_pool']
    for i in range(len(savings) - 1, generation):
        t = time.time()

        gene_pool_next_generation = copy.deepcopy(savings[-1])
        gene_pool_next_generation.update()
        for j in range(0, population):
            print('.', end = '')
            if (j + 1) % 10 == 0:
                print('')
                print('평가 중({0} / {1})'.format(j + 1, population))
            for k in range(0, population):
                if j != k:
                    gene_pool_next_generation.reward([j, k][play_game(gene_pool_next_generation.get(j), gene_pool_next_generation.get(k), width, height)])
        
        while play_game(gene_pool_next_generation.get_best_player(), savings[-1].get_best_player(), width, height) != 0:
            print('삭제하고 다시 새로운 세대 생성중')
            gene_pool_next_generation = copy.deepcopy(savings[-1])
            gene_pool_next_generation.update()
            for j in range(0, population):
                print('.', end = '')
                if (j + 1) % 10 == 0:
                    print('')
                    print('평가 중({0} / {1})'.format(j + 1, population))
                for k in range(0, population):
                    if j != k:
                        gene_pool_next_generation.reward([j, k][play_game(gene_pool_next_generation.get(j), gene_pool_next_generation.get(k), width, height)])
        
        savings.append(copy.deepcopy(gene_pool_next_generation))

        now = time.time()
        sum_time += (now - t)
        with open('intsto', 'wb') as f:
            dill.dump({'gene_pool' : savings, 'sum_time' : sum_time}, f)

        print('{0}세대 : 중간 저장 완료, 소요 시간 : {1}분, 남은 시간(예상) : {2}분'.format(i + 1, (now - t) / 60, sum_time / (i + 1) * (generation - (i + 1)) / 60))

with open('gen{0}_{1}_{2}'.format(generation, width, height), 'wb') as f:
    dill.dump({'gene_pool' : savings, 'sum_time' : sum_time}, f)

print('{0}세대 : 최종 저장 완료, 소요 시간 : {1}분, 남은 시간(예상) : {2}분'.format(i + 1, (now - t) / 60, (sum_time / (i + 1)) * (generation - (i + 1)) / 60))