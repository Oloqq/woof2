WINDOW_SIZE = (1000, 600) # outside Params class because it will never be settable via a config file

class Params:
    grid_size: tuple[int, int] = (200, 200)

    herd_territory_size = 12
    deer_max_tolerated_distance_from_wolves = 40
    herd_size: int = 15
    min_herd_num: int = 6

    pack_territory_length: int = 5
    pack_size: int = 9
    pack_territory_centers = [(50, 0), (199, 20), (0, 170), (199, 199)]
    wolf_hunger_threshold: int = 300
    wolf_max_endurance: int = 500