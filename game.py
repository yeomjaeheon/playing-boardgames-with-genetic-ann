class hexapawn: #검은색 진영이 먼저 시작
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.game_counter = 0
        self.value = {'black' : 1, 'white' : -1, 'empty' : 0}
        self.winner = None

        #board initiation
        self.board = [0 for i in range(0, width * height)]
        for i in range(0, width):
            self.board[i] = self.value['black']
            self.board[width * height - (1 + i)] = self.value['white']

    def play(self, pos, move): #주어진 수가 가능한 수인지 반환, 이동 : 0 -> 앞으로 전진, 1 -> 좌측 폰 잡기, 2 -> 우측 폰 잡기
        x, y = pos % self.width, pos // self.width
        player = ['black', 'white'][self.game_counter % 2]
        player_value = self.value[player]
        move_direction = player_value
        left, right = player_value, -player_value #진영 색에 맞추어서 좌, 우 방향을 정함, 하나의 신경망으로 분석할 수 있도록 서로 회전대칭 관계임
        if self.board[pos] == player:
            if move == 0:
                if 
            elif move == 1:
                pass
            elif move == 2:
                pass
            self.game_counter += 1
            return True
        else:
            return False

    def win(self):
        pass