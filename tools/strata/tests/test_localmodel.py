"""Unit tests for tools/strata/localmodel against a fake OpenAI-compatible server.

They check the plumbing (transport, JSON repair, schema retries, format fallback, cache,
grading, text extraction). They can't check how good a real model's answers are.

    python3 -m unittest discover -s tools/strata/tests
"""

import json
import os
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from localmodel import claims, shots, sprites  # noqa: E402
from localmodel.client import read_bytes, Client, LocalModelError, extract_json, run_batch, strict_schema, validate  # noqa: E402


class FakeServer:
    """Serves /v1/models and /v1/chat/completions. `replies` is a list of strings (or
    callables taking the request body) consumed in order; the last one repeats."""

    def __init__(self, replies, models=("fake-vl",), refuse_formats=()):
        self.replies, self.models, self.refuse = list(replies), list(models), set(refuse_formats)
        self.requests = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *a):
                pass

            def send(self, code, obj):
                data = json.dumps(obj).encode()
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self.send(200, {"data": [{"id": m} for m in outer.models]})

            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                fmt = (body.get("response_format") or {}).get("type")
                if fmt in outer.refuse:
                    return self.send(400, {"error": f"response_format {fmt} not supported"})
                outer.requests.append(body)
                reply = outer.replies.pop(0) if len(outer.replies) > 1 else outer.replies[0]
                text = reply(body) if callable(reply) else reply
                self.send(200, {"choices": [{"message": {"content": text}}],
                                "usage": {"prompt_tokens": 10, "completion_tokens": 5}})

        self.httpd = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.httpd.server_port}/v1"

    def close(self):
        self.httpd.shutdown()
        self.httpd.server_close()


SCHEMA = {"type": "object", "required": ["n", "tags"],
          "properties": {"n": {"type": "integer"}, "tags": {"type": "array", "items": {"type": "string"}}}}


class ClientTest(unittest.TestCase):
    def serve(self, *replies, **kw):
        server = FakeServer(replies, **kw)
        self.addCleanup(server.close)
        return server, Client(url=server.url, cache="off")

    def test_extract_json_from_prose_fences_and_reasoning(self):
        self.assertEqual(extract_json('Sure!\n```json\n{"a": [1, 2]}\n```\nDone.'), {"a": [1, 2]})
        self.assertEqual(extract_json('<think>{"a": 0}</think> {"a": 1}'), {"a": 1})
        self.assertEqual(extract_json('reasoning with {braces} </think>{"a": 2}'), {"a": 2})
        with self.assertRaises(ValueError):
            extract_json("no json here")

    def test_validate(self):
        self.assertEqual(validate({"n": 1, "tags": ["x"]}, SCHEMA), [])
        self.assertTrue(validate({"n": "1", "tags": []}, SCHEMA))
        self.assertTrue(validate({"n": True, "tags": []}, SCHEMA))  # a bool is not an integer
        self.assertTrue(validate({"tags": []}, SCHEMA))
        self.assertTrue(validate({"n": 1, "tags": [3]}, SCHEMA))
        self.assertTrue(validate("x", {"type": "string", "enum": ["a", "b"]}))
        self.assertFalse(strict_schema(SCHEMA)["additionalProperties"])

    def test_single_model_is_picked_and_two_need_a_choice(self):
        _, client = self.serve("hi")
        self.assertEqual(client.model(), "fake-vl")
        _, client = self.serve("hi", models=("a", "b"))
        with self.assertRaisesRegex(LocalModelError, "STRATA_LLM_MODEL.*a, b"):
            client.model()

    def test_ask_json_retries_with_the_error(self):
        server, client = self.serve("I think the answer is five.", '{"n": "5", "tags": []}', '{"n": 5, "tags": ["ok"]}')
        self.assertEqual(client.ask_json("count", SCHEMA), {"n": 5, "tags": ["ok"]})
        self.assertEqual(len(server.requests), 3)
        self.assertIn("rejected", server.requests[2]["messages"][-1]["content"])
        self.assertIn("n must be integer", server.requests[2]["messages"][-1]["content"])

    def test_ask_json_gives_up(self):
        _, client = self.serve("never json")
        with self.assertRaisesRegex(LocalModelError, "did not give valid JSON"):
            client.ask_json("count", SCHEMA, retries=1)

    def test_response_format_falls_back_once(self):
        server, client = self.serve('{"n": 1, "tags": []}', refuse_formats=("json_schema",))
        client.ask_json("a", SCHEMA)
        client.ask_json("b", SCHEMA)
        self.assertEqual([r["response_format"]["type"] for r in server.requests], ["json_object", "json_object"])
        self.assertEqual(client.formats, ["json_object", None])

    def test_images_are_sent_as_data_urls_to_the_vision_model(self):
        server = FakeServer(["ok"], models=("text", "vl"))
        self.addCleanup(server.close)
        client = Client(url=server.url, model="text", vision_model="vl", cache="off")
        client.chat("look", images=[b"\x89PNG fake"])
        client.chat("read")
        self.assertEqual([r["model"] for r in server.requests], ["vl", "text"])
        part = server.requests[0]["messages"][0]["content"][1]
        self.assertTrue(part["image_url"]["url"].startswith("data:image/png;base64,"))

    def test_cache_skips_the_server(self):
        server = FakeServer(["first", "second"])
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as d:
            client = Client(url=server.url, cache=d)
            self.assertEqual(client.chat("q"), "first")
            self.assertEqual(client.chat("q"), "first")
            self.assertEqual(client.chat("other"), "second")
            self.assertEqual((client.calls, client.cache_hits), (2, 1))

    def test_unreachable_server_says_how_to_fix_it(self):
        client = Client(url="http://127.0.0.1:1/v1", cache="off", timeout=2)
        with self.assertRaisesRegex(LocalModelError, "no local model at.*STRATA_LLM_URL"):
            client.models()

    def test_batch_keeps_going_after_one_bad_item_but_not_without_a_server(self):
        def fn(i):
            if i == 2:
                raise LocalModelError("fake did not give valid JSON")
            return {"v": i}
        self.assertEqual(run_batch([1, 2, 3], fn, quiet=True), [{"v": 1}, {"error": "fake did not give valid JSON"}, {"v": 3}])
        dead = Client(url="http://127.0.0.1:1/v1", cache="off", timeout=2)
        with self.assertRaises(LocalModelError):
            run_batch([1], lambda i: {"m": dead.models()}, quiet=True)


class SpritesTest(unittest.TestCase):
    def test_every_species_has_keywords(self):
        self.assertEqual(sprites.missing_keywords(), [])

    def test_keyword_tables_name_real_plans_and_species(self):
        import sprites as art
        self.assertEqual(set(sprites.PLAN_ACCEPT), set(art.TAXONOMY))
        self.assertEqual(set(sprites.SPECIES_ACCEPT) - set(art.SPECIES_PLAN), set())

    def test_grading(self):
        horse = sprites.accept("equus")
        self.assertEqual(sprites.grade(["Horse", "donkey"], horse), "top1")
        self.assertEqual(sprites.grade(["deer", "a small horses", "dog"], horse), "top3")
        self.assertEqual(sprites.grade(["seahorse", "cow"], horse), "miss")
        self.assertEqual(sprites.grade(["cattle"], sprites.accept("panthera")), "miss")  # "cat" is a whole word
        self.assertEqual(sprites.grade(["saber-toothed cat"], sprites.accept("hoplophoneus")), "top1")
        self.assertEqual(sprites.grade(["deer"], sprites.accept("eohippus")), "top1")  # dawn horses only
        self.assertEqual(sprites.grade([], horse), "miss")

    def test_review_renders_asks_and_reports(self):
        server = FakeServer(['{"guesses": ["rat", "squirrel"], "sees": "small furry body"}'])
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as out:
            rows = sprites.review(Client(url=server.url, cache="off"), out, ["mesodma", "knightia"], quiet=True)
            self.assertEqual({r["folder"]: r["grade"] for r in rows}, {"mesodma": "top1", "knightia": "miss"})
            png = read_bytes(os.path.join(out, "sprites", "mesodma.png"))
            self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
            self.assertEqual(png[16:24], (384).to_bytes(4, "big") * 2)
            text = sprites.report(rows, "fake-vl")
            self.assertIn("1 missed", text)
            self.assertIn("*Mesodma*", text)


class ClaimsTest(unittest.TestCase):
    def test_absolutes_need_no_hedge(self):
        text = ("It was the largest predator of its time. It was probably the first true dog. "
                "Among the oldest known bats. It never climbed. The last of the raptors.")
        self.assertEqual([w.lower() for _, w in claims.absolutes(text)], ["the largest", "the last of"])

    def test_codex_and_map_texts(self):
        codex = dict(claims.codex_texts())
        self.assertEqual(len(codex), len(claims.SPECIES))
        self.assertIn("Site:", codex["codex:Mesodma"])
        maps = dict(claims.map_texts())
        text = maps["map:StrataLevee_Text_ReturnToCamp"]
        self.assertEqual(text, "The air shimmers at the edge of the reconstruction. Return to camp?")

    def test_extract_and_report(self):
        server = FakeServer([json.dumps({"claims": [
            {"claim": "Mesodma weighed 50 g", "kind": "size", "hedged": False, "risk": "high"},
            {"claim": "Mesodma probably ate seeds", "kind": "ecology", "hedged": True, "risk": "low"}]})])
        self.addCleanup(server.close)
        items = [("codex:Mesodma", "It was the first. It probably ate seeds.")]
        extracted = claims.extract(Client(url=server.url, cache="off"), items, quiet=True)
        text = claims.report(items, extracted, "fake")
        self.assertIn('"It was the first." (**the first**)', text)
        self.assertLess(text.index("weighed 50 g"), text.index("probably ate seeds"))
        self.assertIn("None.", claims.report([("x", "It may be old.")], None, None))


class ShotsTest(unittest.TestCase):
    def test_flagged_first(self):
        server = FakeServer([
            '{"screen": "A battle.", "text": "", "faults": [], "note": ""}',
            '{"screen": "A sign.", "text": "The lev", "faults": ["text_cut_off"], "note": "second line"}'])
        self.addCleanup(server.close)
        with tempfile.TemporaryDirectory() as d:
            for name in ("001_a.png", "002_b.png"):
                with open(os.path.join(d, name), "wb") as f:
                    f.write(b"\x89PNG" + name.encode())
            files = shots.find([d])
            rows = shots.review(Client(url=server.url, cache="off"), files, quiet=True)
            text = shots.report(rows, "fake", d)
            self.assertIn("2 screenshots, **1 to look at**", text)
            self.assertIn("| `002_b.png` | text_cut_off | second line |", text)

    def test_invalid_fault_is_rejected_then_retried(self):
        server = FakeServer(['{"screen": "x", "text": "", "faults": ["ugly"], "note": ""}',
                             '{"screen": "x", "text": "", "faults": [], "note": ""}'])
        self.addCleanup(server.close)
        with tempfile.NamedTemporaryFile(suffix=".png") as f:
            rows = shots.review(Client(url=server.url, cache="off"), [f.name], quiet=True)
        self.assertEqual(rows[0]["faults"], [])
        self.assertEqual(len(server.requests), 2)


if __name__ == "__main__":
    unittest.main()
