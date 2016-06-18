# REF: https://www.jeffknupp.com/blog/2013/12/09/improve-your-python-understanding-unit-testing/


def is_prime(number):
    """Return True if *number* is prime."""

    if number < 1:
        return False

    for element in range(2, number):
        if number % element == 0:
            return False

    return True


def print_next_prime(number):
    """Print the closest prime number larger than *number*."""
    index = number
    while True:
        index += 1
        if is_prime(index):
            print(index)
            break
