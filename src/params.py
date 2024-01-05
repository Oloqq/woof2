WINDOW_SIZE = (1000, 600) # outside Params class because it will never be settable via a config file

class Params:
    grid_size: tuple[int, int] = (200, 200)

    deer_herd_territory_length = 12
    deer_herd_safety_distance = 30
    deer_herd_size: int = 15
    min_herd_num: int = 6
    wolves_pack_territory_length: int = 5
    wolves_pack_size: int = 9
    pack_num: int = 3
    wolf_hunger_threshold: int = 300
    wolf_max_endurance: int = 500