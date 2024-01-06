WINDOW_SIZE = (1000, 600) # outside Params class because it will never be settable via a config file

class Params:
    grid_size: tuple[int, int] = (250, 250)

    deer_herd_territory_length = 12
    deer_herd_safety_distance = 40
    deer_herd_size: int = 15
    min_herd_num: int = 6
    wolves_pack_territory_length: int = 5
    wolves_pack_size: int = 9
    pack_territory_centers = [(50, 0), (199, 20), (0, 170), (199, 199)]
    wolf_hunger_threshold: int = 300
    wolf_max_endurance: int = 500