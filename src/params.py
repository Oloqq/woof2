WINDOW_SIZE = (1000, 600) # outside Params class because it will never be settable via a config file

class Params:
    grid_size: tuple[int, int] = (100, 100)

    deer_herd_territory_length = 8
    deer_herd_safety_distance = 20
    deer_herd_size: int = 20
    min_herd_num: int = 6
    wolves_pack_territory_length: int = 5
    wolves_pack_size: int = 6
    pack_num: int = 3