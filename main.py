import game, ann

#각 신경망이 받아들이는 보드의 값은 동일함, 보드 상태 평가는 흑색 진영을 기준으로 진행됨, 평가된 상태는 백색 진영의 경우 -1을 곱해 반전시킬 것

class searching_space:
    def __init__(self, num_ann, structure):
        self.num_ann, self.structure = num_ann, structure
        self.anns = []
        for i in range(0, num_ann):
            self.anns.append(ann.ann(structure))
        