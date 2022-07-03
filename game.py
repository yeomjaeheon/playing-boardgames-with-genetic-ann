import copy

class hexapawn: #흑색 진영이 먼저 시작, 상태 평가는 흑색 진영 기준으로 진행
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.game_counter = 0
        self.value = {'black' : 1, 'white' : -1, 'empty' : 0}

        #보드 초기화
        self.board = [0 for i in range(0, width * height)]
        for i in range(0, width):
            self.board[i] = self.value['black']
            self.board[width * height - (1 + i)] = self.value['white']

    def play(self, pos, move, count): #주어진 수가 가능한 수인지 반환, 이동 : 0 -> 앞으로 전진, 1 -> 좌측 폰 잡기, 2 -> 우측 폰 잡기
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
                if self.board[pos + move_direction * self.width] == self.value['empty']:
                    self.board[pos] = self.value['empty']
                    self.board[pos + move_direction * self.width] = player_value
                else:
                    return False
            elif move == 1:
                if 0 <= x + left < self.width:
                    if self.board[pos + move_direction * self.width + left] == enemy_value:
                        self.board[pos] = self.value['empty']
                        self.board[pos + move_direction * self.width + left] = player_value
                else:
                    return False
            elif move == 2:
                if 0 <= x + right < self.width:
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

    def win(self):
        for i in range(0, self.width):
            if self.board[i] == self.value['white']:
                return 'white'
            elif self.board[self.width * self.height - (1 + i)] == self.value['black']:
                return 'black'
        return None

    def display(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                print({1 : 'B', -1 : 'W', 0 : '.'}[self.board[i * self.width + j]], end = '')
            print('')

    def reset(self):
        self.__init__(self.width, self.height)