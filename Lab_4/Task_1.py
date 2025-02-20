def read_input(file):
    with open(file) as f:
        N, K, V = map(int, f.readline().strip().split())
        stations = [list(map(int, f.readline().strip().split())) for _ in range(N)]
    return N, K, V, stations
