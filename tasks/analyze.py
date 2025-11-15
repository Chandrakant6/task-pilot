def run(input_data, multiplier=1):
    """
    Mock analysis step.
    Multiply each number by 'multiplier'.
    """
    if input_data is None:
        return None

    analyzed = [x * multiplier for x in input_data]
    return analyzed
