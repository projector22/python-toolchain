def add_leading_zero(value, num_of_zeros: int = 1) -> str:
    """Add leading zeros to integers. Non numeric input is returned as
    is and numbers greater than the number of zeros required are also 
    returned as is.

    Examples:
        - add_leading_zero(5)        -> returns '05'
        - add_leading_zero(5, 2)     -> returns '005'
        - add_leading_zero(0, 1)     -> returns '00'
        - add_leading_zero(12)       -> returns '12'
        - add_leading_zero('12')     -> returns '12'
        - add_leading_zero('cheese') -> returns 'cheese'

    Args:
        value (mixed): A number or numeric string to have a leading zero attached.
        num_of_zeros (int, optional): The number of leading zeros to add. Defaults to 1.

    Raises:
        Exception: Exception if num_of_zeros is parsed as 0 or less.

    Returns:
        string: The formatted number as a string with leading zeros attached.
    """
    if num_of_zeros < 1:
        raise Exception("Number of leading zeros must be 1 or higher")
    value = str(value)
    if value.isnumeric() == False:
        return value
    zero_string = "0"
    for i in range(num_of_zeros):
        zero_string += "0"
    value = value[::-1]
    k = 0
    for i in value:
        zero_string = zero_string[:k] + i + zero_string[k + 1:]
        k += 1
    return zero_string[::-1]
