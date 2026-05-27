import json
import unittest

from app.web import RequestError, parse_answer_request


class WebValidationTests(unittest.TestCase):
    def test_valid_request_defaults(self) -> None:
        request = parse_answer_request(json.dumps({"question": "P1 outage"}))
        self.assertEqual(request["question"], "P1 outage")
        self.assertEqual(request["mode"], "instant")
        self.assertEqual(request["voice"], "natural")
        self.assertEqual(request["limit"], 3)

    def test_empty_question_rejected(self) -> None:
        with self.assertRaises(RequestError):
            parse_answer_request(json.dumps({"question": "   "}))

    def test_bad_limit_rejected(self) -> None:
        with self.assertRaises(RequestError):
            parse_answer_request(json.dumps({"question": "P1 outage", "limit": 99}))


if __name__ == "__main__":
    unittest.main()
