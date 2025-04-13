from typing import List

def is_sorted_non_decreasing(arr: List[float]) -> bool:
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """
    Check if in given list of numbers, there are any two numbers closer to each other than
    the given threshold.
    
    Preconditions:
      - numbers is a list of floats or ints.
      - threshold is a positive float.
    
    Postconditions:
      - Returns True if there exists at least one pair of distinct elements in the list
        whose absolute difference is strictly less than threshold, otherwise False.

    Examples:
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    """

    assert isinstance(numbers, list), "numbers must be a list"
    for num in numbers:
        assert isinstance(num, (int, float)), "each element in numbers must be int or float"
    assert isinstance(threshold, (int, float)), "threshold must be a number"
    assert threshold > 0, "threshold must be positive"

    if len(numbers) < 2:
        return False

    sorted_numbers = sorted(numbers)
    
    assert is_sorted_non_decreasing(sorted_numbers), "sorted_numbers must be sorted in non-decreasing order"

    for i in range(len(sorted_numbers) - 1):
        for j in range(i):
            diff = abs(sorted_numbers[j+1] - sorted_numbers[j])
            assert diff >= threshold, (
                f"Loop invariant failed: difference {diff} between indices {j} and {j+1} is less than threshold {threshold}"
            )
        
        diff = abs(sorted_numbers[i+1] - sorted_numbers[i])
        assert diff >= 0, "Difference computed should be non-negative"
        
        if diff < threshold:
            result = True
            assert any(abs(sorted_numbers[k+1] - sorted_numbers[k]) < threshold for k in range(len(sorted_numbers)-1)), \
                "Postcondition failed: Expected a close pair in sorted_numbers"
            return result

    result = False
    for i in range(len(sorted_numbers) - 1):
        diff = abs(sorted_numbers[i+1] - sorted_numbers[i])
        assert diff >= threshold, (f"Final check: found a difference {diff} which is less than threshold {threshold}")
    
    assert isinstance(result, bool), "The result must be a boolean value"
    return result