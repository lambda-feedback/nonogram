import unittest

try:
    from .evaluation import Params, evaluation_function
except ImportError:
    from evaluation import Params, evaluation_function


class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    def test_returns_is_correct_true(self):
        response, answer, params = None, None, Params()
        result = evaluation_function(response, answer, params)

        self.assertEqual(result.get("is_correct"), True)

    def test_I_correct(self):
        response = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        answer = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), True)

    def test_I_incorrect_row(self):
        response = [[0, 0, 1], [0, 1, 0], [0, 0, 1]]
        answer = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

        response = evaluation_function(response, answer, {})

        self.assertEqual(response.get("is_correct"), False)
        self.assertEqual(
            response["feedback"], "Row 1 does not match: Answer: ['1' '0' '0'], Response: ['0' '0' '1']")


if __name__ == "__main__":
    unittest.main()
