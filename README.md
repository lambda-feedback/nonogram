# Nonogram Evaluation Function

An AWS Lambda evaluation function for grading nonogram (picross) puzzle responses. Given a student's completed nonogram grid and the correct solution, it compares them element-by-element and returns pass/fail feedback identifying the first mismatched row or column.

## Table of Contents
- [Repository Structure](#repository-structure)
- [How it works](#how-it-works)
  - [Evaluation Logic](#evaluation-logic)
  - [Docker & Amazon Web Services (AWS)](#docker--amazon-web-services-aws)
  - [GitHub Actions](#github-actions)
- [Development](#development)
- [Contact](#contact)

## Repository Structure

```
app/
    evaluation.py        # Main evaluation function
    preview.py           # Preview function
    evaluation_tests.py  # Unit tests for evaluation_function
    preview_tests.py     # Unit tests for preview_function
    requirements.txt     # Python dependencies (numpy)
    Dockerfile           # Container image for AWS Lambda
    docs/
        user.md          # Teacher-facing documentation
        dev.md           # Developer documentation

.github/
    workflows/
        test-and-deploy.yml  # CI/CD pipeline

config.json   # Evaluation function name ("nonogram")
.gitignore
```

## How it works

### Evaluation Logic

The function receives a `response` and `answer`, both 2D arrays representing nonogram grids (e.g. `[[1, 0, 0], [0, 1, 0], [0, 0, 1]]`).

1. **Empty check** — validates that neither the answer nor response contain empty or undefined cells.
2. **Shape check** — ensures the response grid has the same dimensions as the answer.
3. **Element-wise comparison** — uses NumPy to compare all cells. If incorrect, it scans rows first, then columns, and returns feedback identifying the first mismatch.

Example response:

```json
{
  "is_correct": false,
  "feedback": "Row 1 does not match: Answer: ['1' '0' '0'], Response: ['0' '0' '1']"
}
```

### Docker & Amazon Web Services (AWS)

The function runs on AWS Lambda using a Docker container image. Docker bundles the app and its dependencies (numpy) into a single image, which is pushed to a shared ECR repository on each deployment. For more on Docker, see this [introduction to containerisation](https://www.freecodecamp.org/news/a-beginner-friendly-introduction-to-containers-vms-and-docker-79a9e3e119b/).

The base infrastructure and middleware that handles request routing, schema validation, and command dispatch is provided by [BaseEvaluationFunctionLayer](https://github.com/lambda-feedback/BaseEvalutionFunctionLayer). This function only needs to implement `evaluation_function()` and `preview_function()`.

### GitHub Actions

Merging to the default branch triggers `.github/workflows/test-and-deploy.yml`, which:

1. Runs the unit tests in `evaluation_tests.py` and `preview_tests.py`.
2. Builds and pushes the Docker image to ECR.
3. Calls the backend `grading-function/ensure` route to deploy the updated function.

Tests also run on the deployed function whenever it receives a `healthcheck` command.

## Development

**Prerequisites:** Python 3.8+, `git`, a code editor.

Install dependencies locally:

```bash
pip install -r app/requirements.txt
```

Run tests:

```bash
python -m pytest app/
```

Key files to edit:

| File | Purpose |
|---|---|
| `app/evaluation.py` | Grading logic, called on `eval` command |
| `app/preview.py` | Preview rendering, called on `preview` command |
| `app/evaluation_tests.py` | Unit tests for evaluation |
| `app/preview_tests.py` | Unit tests for preview |
| `app/docs/user.md` | Teacher-facing docs (served via `docs` command) |
| `app/docs/dev.md` | Developer docs |

## Contact

This function is part of the [lambda-feedback](https://github.com/lambda-feedback) project.