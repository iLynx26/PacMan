def get_opposite_direction(dir):
    if dir == 'right':
        return 'left'
    if dir == 'left':
        return 'right'
    if dir == 'up':
        return 'down'
    if dir == 'down':
        return 'up'
    return None