"""Unit test for signal averager."""
import LucasNumber


def test_lucas_number_generator():
    """
    Test Lucas number generator (Simple Test).

    Test Overview:
    --------------
    The test will look for the following:
    a) Is the sequence correct? This is verified through a simple lookup test.
    This test only looks at the first 10 numbers generated.
    The Golden ratio is not checked. It is assumed that if the sequence is correct
    the ratio will be valid.

    Parameters
    ----------
    max_lucas_number: int
        Maximum Lucas number to generate before stopping.
    """
    max_lucas_number = 500
    expected_lucas_sequence = [3, 4, 7, 11, 18, 29, 47, 76, 123, 199]
    generated_sequence = []

    # Create generator
    lng = LucasNumber.lucas_number_generator([2, 1])

    # Iterate through generating valid Lucas numbers. Of particular interest is number 76 (EE6:76)
    for lucas in lng:
        print(lucas)
        generated_sequence.append(lucas)
        try:
            # Stop the generation (and yielding) when the 'max_lucas_number' is reached.
            if lucas[0] > max_lucas_number:
                lng.close()
            lng.send(lucas[0])
        except StopIteration:
            break

    print("Done!")

    # Iterate through the generated sequence and compare to the expected sequence.
    for i in range(len(expected_lucas_sequence)):
        assert generated_sequence[i][0] == expected_lucas_sequence[i]


""" Debug: Uncomment to run individual methods"""
test = test_lucas_number_generator()
