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

    gigapaleta = [(230, 25, 75), (60, 180, 75), (255, 225, 25), (0, 130, 200), (245, 130, 48), (145, 30, 180), (70, 240, 240), (240, 50, 230), (210, 245, 60), (250, 190, 212), (0, 128, 128), (220, 190, 255), (170, 110, 40), (255, 250, 200), (128, 0, 0), (170, 255, 195), (128, 128, 0), (255, 215, 180), (0, 0, 128), (128, 128, 128)]
    pastelpaleta = [(243, 210, 241), (215, 241, 211), (246, 243, 215), (216, 231, 247), (246, 203, 203)]
    #     I’ll try to create that.

    # Here is a cute uwu kawaii color palette of 10 colors as a Python list of RGB tuples:
    cute_uwu_kawaii_palette = [
        (255, 0, 102),  # pink
        (255, 204, 204),  # light pink
        (255, 255, 153),  # yellow
        (255, 102, 102),  # red
        (255, 204, 153),  # peach
        (204, 255, 204),  # light green
        (153, 255, 255),  # light blue
        (204, 153, 255),  # lavender
        (255, 153, 255),  # magenta
        (255, 153, 204)  # light purple
    ]