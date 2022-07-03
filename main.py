import game

b = game.hexapawn(4, 4)
while True:
    code = input()
    exec(code)
    b.display()
    print(b.win())