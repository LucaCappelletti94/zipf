def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)
