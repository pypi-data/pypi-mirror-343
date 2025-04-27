"""
Conversion Utilities for dict, list, and tuple.
"""

def dict_to_list(data):
    """
    Convert a dictionary to a list of tuples (key, value).
    
    Args:
        data (dict): Dictionary to convert.
        
    Returns:
        list: List of tuples representing key-value pairs.
    """
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")
    return list(data.items())

def list_to_dict(data):
    """
    Convert a list of tuples (key, value) to a dictionary.
    
    Args:
        data (list): List of key-value pairs.
        
    Returns:
        dict: Dictionary representing the input list.
    """
    if not isinstance(data, list):
        raise ValueError("Input must be a list.")
    return dict(data)

def dict_to_tuple(data):
    """
    Convert a dictionary to a tuple of key-value pairs.
    
    Args:
        data (dict): Dictionary to convert.
        
    Returns:
        tuple: Tuple of key-value pairs.
    """
    if not isinstance(data, dict):
        raise ValueError("Input must be a dictionary.")
    return tuple(data.items())

def list_to_tuple(data):
    """
    Convert a list to a tuple.
    
    Args:
        data (list): List to convert.
        
    Returns:
        tuple: Tuple containing elements of the list.
    """
    if not isinstance(data, list):
        raise ValueError("Input must be a list.")
    return tuple(data)

def tuple_to_dict(data):
    """
    Convert a tuple of key-value pairs to a dictionary.
    
    Args:
        data (tuple): Tuple of key-value pairs (tuples).
        
    Returns:
        dict: Dictionary representing the input tuple.
    """
    if not isinstance(data, tuple):
        raise ValueError("Input must be a tuple.")
    return dict(data)

def tuple_to_list(data):
    """
    Convert a tuple to a list.
    
    Args:
        data (tuple): Tuple to convert.
        
    Returns:
        list: List containing elements of the tuple.
    """
    if not isinstance(data, tuple):
        raise ValueError("Input must be a tuple.")
    return list(data)
