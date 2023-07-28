block_size = 40
difficulty = 0

def lerp_difficulty(min_value, max_value):
    return min_value + (max_value-min_value) * difficulty