import turtle

hugo = turtle.Turtle()


def draw_square(n):
    hugo.forward(n)
    hugo.left(90)
    hugo.forward(n)
    hugo.left(90)
    hugo.forward(n)
    hugo.left(90)
    hugo.forward(n)

for i in range(1,10,1):
    draw_square(50)
