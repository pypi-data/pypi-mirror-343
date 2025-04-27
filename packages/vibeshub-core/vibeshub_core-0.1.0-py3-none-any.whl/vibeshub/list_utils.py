# vibeshub/list_utils.py

def chunk_list(lst, size):
    """
    Yield successive chunks of a list with the given size.

    Args:
        lst (list): The list to be chunked.
        size (int): The size of each chunk.

    Yields:
        list: A chunk of the original list.

    Raises:
        ValueError: If size is not greater than 0.
    """
    if size <= 0:
        raise ValueError("size must be greater than 0")
    for i in range(0, len(lst), size):
        yield lst[i:i + size]
