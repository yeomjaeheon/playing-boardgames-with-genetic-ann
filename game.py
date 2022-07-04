import copy

class hexapawn: #흑색 진영이 먼저 시작, 상태 평가는 흑색 진영 기준으로 진행
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.game_counter = 0
        self.value = {'black' : 1, 'white' : -1, 'empty' : 0}

        self.possible_moves = {'black' : [], 'white' : []}

        #보드 초기화
        self.board = [0 for i in range(0, width * height)]
        for i in range(0, width):
            self.board[i] = self.value['black']
            self.board[-(i + 1)] = self.value['white']

    def play(self, pos, move):
        self.simulate(pos, move, count = True)
        return self.win()

    def simulate(self, pos, move, count = False): #주어진 수가 가능한 수인지 반환, 이동 : 0 -> 앞으로 전진, 1 -> 좌측 폰 잡기, 2 -> 우측 폰 잡기
        x, y = pos % self.width, pos // self.width
        player = ['black', 'white'][self.game_counter % 2]
        enemy = ['black', 'white'][(self.game_counter + 1) % 2]
        player_value = self.value[player]
        enemy_value = self.value[enemy]
        move_direction = player_value
        left, right = player_value, -player_value #진영 색에 맞추어서 좌, 우 방향을 정함, 하나의 신경망으로 분석할 수 있도록 서로 회전대칭 관계임
        if count:
            self.game_counter += 1
        else:
            self.board_backup = copy.deepcopy(self.board)
        if self.board[pos] == player_value:
            if move == 0:
                #조건 순서 바꾸지 말 것, index error를 막기 위해 y값 검증을 앞에 배치함
                if 0 <= y + move_direction < self.height and self.board[pos + move_direction * self.width] == self.value['empty']:
                    self.board[pos] = self.value['empty']
                    self.board[pos + move_direction * self.width] = player_value
                else:
                    return False
            elif move == 1:
                if 0 <= x + left < self.width and 0 <= y + move_direction < self.height:
                    if self.board[pos + move_direction * self.width + left] == enemy_value:
                        self.board[pos] = self.value['empty']
                        self.board[pos + move_direction * self.width + left] = player_value
                else:
                    return False
            elif move == 2:
                if 0 <= x + right < self.width and 0 <= y + move_direction < self.height:
                    if self.board[pos + move_direction * self.width + right] == enemy_value:
                        self.board[pos] = self.value['empty']
                        self.board[pos + move_direction * self.width + right] = player_value
                else:
                    return False
            self.board_simulate = copy.deepcopy(self.board)
            if not count:
                self.board = copy.deepcopy(self.board_backup)
            return self.board_simulate
        else:
            return False

    def search(self):
        moves = []
        for i in range(0, len(self.board)):
            for j in range(0, 3):
                state = self.simulate(i, j, False)
                if state:
                    moves.append(state)
        return moves

    def win(self): #말 이동 후 호출할 것
        for i in range(0, self.width): #각 진영이 상대방 진영으로 말을 보냈을때
            if (self.game_counter - 1) % 2 == 0: #이전의 수로 game_counter가 가산되었으므로 이전 진영의 승패를 판정하기 위해 1을 뺌
                if self.board[-(i + 1)] == self.value['black']:
                    return True
            else:
                if self.board[i] == self.value['white']:
                    return True
        self.possible_moves[['black', 'white'][self.game_counter % 2]] = self.search() #상대 진영이 가능한 수가 없을 경우 승리 판정
        if not self.possible_moves[['black', 'white'][self.game_counter % 2]]:
            return True
        return False

    def search_moves(self):
        return self.possible_moves[['black', 'white'][self.game_counter % 2]]

    def display(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                print({1 : 'B', -1 : 'W', 0 : '.'}[self.board[i * self.width + j]], end = '')
            print('')

    def reset(self):
        self.__init__(self.width, self.height)