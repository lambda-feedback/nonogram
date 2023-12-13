from typing import Any, TypedDict
import numpy as np


class Params(TypedDict):
    pass


class Result(TypedDict):
    is_correct: bool


def evaluation_function(response: Any, answer: Any, params: Params) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    # Check for empty fields in answer and/or response
    answer_ok = process_element(answer)
    if not answer_ok:
        raise Exception("Answer has empty fields.")
    response_ok = process_element(response)
    if not response_ok:
        return {"is_correct": False, "feedback": "Response has empty fields."}

    # Convert the response and answer to numpy arrays of strings
    try:
        res_str = np.array(response, dtype=str)
        ans_str = np.array(answer, dtype=str)
    except Exception as e:
        raise Exception(
            "Failed to convert to string arrays", detail=repr(e))

    # Check if the arrays have the same shape
    if res_str.shape != ans_str.shape:
        return {"is_correct": False, "feedback": "Response and answer shapes do not match."}

    # Element-wise comparison for string match
    is_correct = np.all(res_str == ans_str)

    if not is_correct:
        found = False
        for i in range(len(ans_str)):
            if (ans_str[i] != res_str[i]).any():
                feedback = f"Row {i+1} does not match: Answer: {ans_str[i]}, Response: {res_str[i]}"
                print(feedback)
                found = True
                break  # Exit after the first mismatch is found
        if not found:
            # Assumes all rows have the same number of columns
            for j in range(len(ans_str[0])):
                # Extracting columns
                ans_col = ans_str[:, j]
                res_col = res_str[:, j]

                if (ans_col != res_col).any():
                    feedback = f"Column {j+1} does not match: Answer Column: {ans_col}, Response Column: {res_col}"
                    print(feedback)
                    found = True
                    break  # Exit after the first mismatch is found

    else:
        feedback = "correct"

        # print(res_str, '\n', ans_str, is_correct)

    return {"is_correct": is_correct, "feedback": feedback}


def process_element(element):  # Test for empty elements
    is_ok = True
    if isinstance(element, list):
        for e in element:
            is_ok = process_element(e)
    else:
        if isinstance(element, str):
            element = element.strip()
            if len(element) == 0 or "element" == "undefined":
                is_ok = False
            else:
                element = float(element)
    return is_ok
