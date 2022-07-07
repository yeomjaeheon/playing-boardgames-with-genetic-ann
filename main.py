from numpy import save
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
            g = players[board.game_counter % 2].prop(board.board + m['state'])[0] * [1, -1][board.game_counter % 2] #백색 진영의 경우는 상태 평가를 -1를 곱해 반전
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
            parent1 = self.get_random_parent()
            parent2 = self.get_random_parent()
            self.anns.append(ann.crossover(parent1, parent2))
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
        print(self.score[index])
        return self.anns[index]

width, height = 5, 5
generation = 30
population = 500
num_evaluation_unit = 5
ann_structure = [width * height * 2, 50, 1]

#이전에 저장된 과정을 이어서 진행
default_name_intermediat_storage = 'intsto' #중간 저장 파일 기본 이름

try:
    with open(default_name_intermediat_storage, 'rb') as f:
        save_file = dill.load(f)
    using_previous_file = True
except:
    using_previous_file = False
    save_file = searching_space(population, ann_structure)

if using_previous_file:
    pass

else:
    gen_alpha = searching_space(population, ann_structure)
    best_player_prev = gen_alpha.get_best_player()
    win_count = 0

    for j in range(0, population):
        if (j + 1) % 100 == 0:
            print('.', end = '')
        if play_game(save_file.get(j), best_player_prev, width, height) == 0:
            save_file.reward(j)
            win_count += 1
        if play_game(best_player_prev, save_file.get(j), width, height) == 0:
            save_file.reward(j)
            win_count += 1

    for i in range(0, generation):
        print('{0}세대 : 진행중'.format(i + 1))
        best_player_prev = save_file.get_best_player()
        win_count = 0
        while win_count < population:
            save_file_tmp = copy.deepcopy(save_file)
            save_file_tmp.update()
            for j in range(0, population):
                if play_game(save_file_tmp.get(j), best_player_prev, width, height) == 0:
                    save_file_tmp.reward(j)
                    win_count += 1
                if play_game(best_player_prev, save_file_tmp.get(j), width, height) == 0:
                    save_file_tmp.reward(j)
                    win_count += 1

        save_file = copy.deepcopy(save_file_tmp)
        with open(default_name_intermediat_storage, 'wb') as f:
            dill.dump(save_file, f)
        print('{0}세대 : 중간 저장 완료'.format(i + 1))

with open('gen{0}_{1}_{2}'.format(generation, width, height), 'wb') as f:
        dill.dump(save_file, f)
        print('저장 완료')