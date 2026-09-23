import json

from app.services.data_agent import ask_data_agent


def load_questions():
    with open("tests/evaluation_questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_result(data):
    """
    Convert database tuples into JSON-like lists
    so they can be compared with expected results.
    """
    if not data:
        return []

    if len(data) == 1:
        return list(data[0])

    return [list(row) for row in data]


def run_evaluation():
    questions = load_questions()

    passed = 0
    failed = 0

    for item in questions:
        print("=" * 80)
        print(f"Question: {item['question']}")

        try:
            result = ask_data_agent(item["question"])

            actual = normalize_result(result["data"])
            expected = item["expected"]

            is_correct = actual == expected

            if is_correct:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(f"\nExpected: {expected}")
            print(f"Actual:   {actual}")
            print(f"Status:   {status}")

            print(f"\nSQL:\n{result['sql']}")
            print(f"\nAnswer:\n{result['answer']}")

        except Exception as error:
            failed += 1

            print("\nStatus: FAIL")
            print(f"Error: {error}")

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print("=" * 80)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")


if __name__ == "__main__":
    run_evaluation()