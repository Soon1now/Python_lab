class Vertex:
    def __init__(self, x_1, y_1):
        self.x = x_1
        self.y = y_1

    def move_vertex(self, dx, dy):
        self.x += dx
        self.y += dy


class Triangle:
    def __init__(self, x1, x2, x3, y1, y2, y3):
        self.vertex1 = Vertex(x1, y1)
        self.vertex2 = Vertex(x2, y2)
        self.vertex3 = Vertex(x3, y3)

    def move(self, dx, dy):
        self.vertex1.move_vertex(dx, dy)
        self.vertex2.move_vertex(dx, dy)
        self.vertex3.move_vertex(dx, dy)

    def get_vertices(self):
        return [(self.vertex1.x, self.vertex1.y),
                (self.vertex2.x, self.vertex2.y),
                (self.vertex3.x, self.vertex3.y)]


class Tetragon:
    def __init__(self, x1, x2, x3, x4, y1, y2, y3, y4):
        self.vertex1 = Vertex(x1, y1)
        self.vertex2 = Vertex(x2, y2)
        self.vertex3 = Vertex(x3, y3)
        self.vertex4 = Vertex(x4, y4)

    def move(self, dx, dy):
        self.vertex1.move_vertex(dx, dy)
        self.vertex2.move_vertex(dx, dy)
        self.vertex3.move_vertex(dx, dy)
        self.vertex4.move_vertex(dx, dy)

    def get_vertices(self):
        return [(self.vertex1.x, self.vertex1.y),
                (self.vertex2.x, self.vertex2.y),
                (self.vertex3.x, self.vertex3.y),
                (self.vertex4.x, self.vertex4.y)]


def point_in_polygon(point, polygon):

    x, y = point
    n = len(polygon)
    inside = False
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        if y > min(y1, y2):
            if y <= max(y1, y2):
                if x <= max(x1, x2):
                    if y1 != y2:
                        xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1
                    if y1 == y2:
                        if y == y1 and x <= max(x1, x2):
                            inside = not inside
                    elif x1 == x2 or x <= xinters:
                        inside = not inside
    return inside


def is_shape_inside(shape1, shape2):

    vertices1 = shape1.get_vertices()
    polygon2 = shape2.get_vertices()

    for vertex in vertices1:
        if not point_in_polygon(vertex, polygon2):
            return False
    return True



triangle = Triangle(1, 2, 1.5, 1, 3, 2)
tetragon = Tetragon(0, 3, 3, 0, 0, 0, 3, 3)


if is_shape_inside(triangle, tetragon):
    print("Треугольник находится внутри четырёхугольника.")
else:
    print("Треугольник не находится внутри четырёхугольника.")


if is_shape_inside(tetragon, triangle):
    print("Четырёхугольник находится внутри треугольника.")
else:
    print("Четырёхугольник не находится внутри треугольника.")