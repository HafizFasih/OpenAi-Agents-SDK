from agents.function_schema import generate_func_documentation
from rich import print

def sum_in_google_docstring(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b

def sum_in_numpy_docstring(a: int, b: int) -> int:
    """Add two numbers.

    Parameters
    ----------
    a : int
        The first number.
    b : int
        The second number.

    Returns
    -------
    int
        The sum of the two numbers.

    Examples
    --------
    >>> sum(1, 2)
    3
    >>> sum(10, -5)
    5
    """
    return a + b

def sum_in_sphinx_docstring(a: int, b: int) -> int:
    """Add two numbers.

    :param a: The first number.
    :type a: int
    :param b: The second number.
    :type b: int
    :returns: The sum of the two numbers.
    :rtype: int
    """
    return a + b

docs_google=generate_func_documentation(
    func=sum_in_google_docstring,
    style="google"
)
docs_numpy=generate_func_documentation(
    func=sum_in_numpy_docstring,
    style="numpy"
)
docs_sphinx=generate_func_documentation(
    func=sum_in_sphinx_docstring,
    style="sphinx"
)


print(docs_google)
print(docs_numpy)
print(docs_sphinx)