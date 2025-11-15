def run(input_data, threshold=5):
    """
    Mock cleaning step.
    - If input_data is None, start with a raw list.
    - Filter numbers greater than or equal to threshold.
    """
    if input_data is None:
        input_data = [1, 3, 5, 10, 2, 8]

    cleaned = [x for x in input_data if x >= threshold]
    return cleaned
