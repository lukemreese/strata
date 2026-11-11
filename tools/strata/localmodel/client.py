"""OpenAI-compatible chat client for a local model server. Standard library only.

Environment:
    STRATA_LLM_URL     base URL, default http://localhost:11434/v1 (Ollama). llama.cpp's
                       llama-server is :8080/v1, LM Studio :1234/v1, vLLM :8000/v1.
    STRATA_LLM_MODEL   model name for text. Unset: the server's only model, else an error
                       that lists what it serves.
    STRATA_VLM_MODEL   model name for requests with images (default: STRATA_LLM_MODEL).
    STRATA_LLM_KEY     bearer token if the server wants one (default "local").
    STRATA_LLM_CACHE   cache folder (default <repo>/.cache/strata-local); "off" disables.
    STRATA_LLM_TIMEOUT seconds per request (default 300).

Weak models fail in three known ways, and each is handled here rather than in callers:
they wrap JSON in prose or code fences (extract_json), they leave reasoning in the reply
(<think> blocks are stripped), and they return the wrong shape (ask_json validates against
a small schema and re-asks with the error, up to `retries` times).
"""

import base64
import hashlib
import json
import os
import re
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DEFAULT_URL = "http://localhost:11434/v1"


def read_bytes(path):
    with open(path, "rb") as f:
        return f.read()


class LocalModelError(Exception):
    """The server can't be reached, or the model kept answering in the wrong shape."""


# --- JSON out of free text ---------------------------------------------------------

_THINK = re.compile(r"<think>.*?</think>", re.S)


def strip_reasoning(text):
    text = _THINK.sub("", text)
    if "</think>" in text:  # an unopened block: the template ate the opening tag
        text = text.split("</think>", 1)[1]
    return text.strip()


def extract_json(text):
    """The first JSON object or array in `text` (prose and code fences around it are
    ignored). Raises ValueError when there is none."""
    text = strip_reasoning(text)
    decoder = json.JSONDecoder()
    for i, ch in enumerate(text):
        if ch in "{[":
            try:
                return decoder.raw_decode(text, i)[0]
            except ValueError:
                continue
    raise ValueError("no JSON in the reply")


# --- Schema --------------------------------------------------------------------------

_TYPES = {"string": str, "boolean": bool, "integer": int, "number": (int, float),
          "array": list, "object": dict}


def validate(value, schema, path="answer"):
    """Errors (strings) for `value` against the JSON Schema subset the tools use:
    type, properties, required, items, enum, maxItems. Empty list = valid."""
    kind = schema.get("type")
    if kind:
        want = _TYPES[kind]
        if not isinstance(value, want) or (kind in ("integer", "number") and isinstance(value, bool)):
            return [f"{path} must be {kind}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        return [f"{path} must be one of {schema['enum']}, got {value!r}"]
    errors = []
    if kind == "object":
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key} is missing")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors += validate(value[key], sub, f"{path}.{key}")
    elif kind == "array":
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{path} has more than {schema['maxItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                errors += validate(item, schema["items"], f"{path}[{i}]")
    return errors


def strict_schema(schema):
    """The same schema with additionalProperties: false on every object, as the strict
    json_schema response format wants."""
    out = dict(schema)
    if out.get("type") == "object":
        out["additionalProperties"] = False
        out["properties"] = {k: strict_schema(v) for k, v in out.get("properties", {}).items()}
    if "items" in out:
        out["items"] = strict_schema(out["items"])
    return out


# --- Client --------------------------------------------------------------------------

class Client:
    def __init__(self, url=None, model=None, vision_model=None, key=None, cache=None, timeout=None):
        env = os.environ
        self.url = (url or env.get("STRATA_LLM_URL") or DEFAULT_URL).rstrip("/")
        self._model = model or env.get("STRATA_LLM_MODEL")
        self._vision_model = vision_model or env.get("STRATA_VLM_MODEL")
        self.key = key or env.get("STRATA_LLM_KEY") or "local"
        self.timeout = float(timeout or env.get("STRATA_LLM_TIMEOUT") or 300)
        cache = cache if cache is not None else env.get("STRATA_LLM_CACHE")
        self.cache_dir = None if cache == "off" else (cache or os.path.join(ROOT, ".cache", "strata-local"))
        self.formats = ["json_schema", "json_object", None]  # tried in order; ones the server refuses are dropped
        self.calls = self.cache_hits = 0
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    # -- transport --

    def _request(self, path, body=None):
        req = urllib.request.Request(
            self.url + path, data=json.dumps(body).encode() if body is not None else None,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:400]
            raise LocalModelError(f"{self.url}{path}: HTTP {e.code} {detail}") from e
        except (urllib.error.URLError, OSError, ValueError) as e:
            raise LocalModelError(
                f"no local model at {self.url} ({getattr(e, 'reason', e)}). Start the server, or set "
                f"STRATA_LLM_URL; see .claude/skills/strata-local-model/SKILL.md") from e

    def models(self):
        return [m["id"] for m in self._request("/models").get("data", [])]

    def model(self, vision=False):
        if vision and self._vision_model:
            return self._vision_model
        if not self._model:
            served = self.models()
            if len(served) != 1:
                raise LocalModelError(
                    "set STRATA_LLM_MODEL (and STRATA_VLM_MODEL for images); the server has: "
                    + (", ".join(served) or "no models"))
            self._model = served[0]
        return self._model

    # -- chat --

    def chat(self, prompt, system=None, images=(), response_format=None, max_tokens=1024, temperature=0):
        """One reply as text (reasoning stripped). `images` are PNG bytes."""
        content = prompt
        if images:
            content = [{"type": "text", "text": prompt}] + [
                {"type": "image_url",
                 "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()}}
                for png in images]
        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": content}]
        body = {"model": self.model(vision=bool(images)), "messages": messages,
                "temperature": temperature, "max_tokens": max_tokens}
        if response_format:
            body["response_format"] = response_format

        key = hashlib.sha256(json.dumps([self.url, body], sort_keys=True).encode()).hexdigest()
        path = self.cache_dir and os.path.join(self.cache_dir, key[:2], key + ".json")
        if path and os.path.exists(path):
            self.cache_hits += 1
            with open(path) as f:
                return json.load(f)["text"]

        reply = self._request("/chat/completions", body)
        self.calls += 1
        for k in self.usage:
            self.usage[k] += (reply.get("usage") or {}).get(k) or 0
        try:
            text = strip_reasoning(reply["choices"][0]["message"]["content"] or "")
        except (KeyError, IndexError, TypeError) as e:
            raise LocalModelError(f"unexpected reply from {self.url}: {str(reply)[:300]}") from e
        if path:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump({"model": body["model"], "text": text}, f)
        return text

    def ask_json(self, prompt, schema, system=None, images=(), retries=2, max_tokens=1024):
        """A reply that validates against `schema` (an object schema), as a dict."""
        example = json.dumps(_example(schema))
        base = f"{prompt}\n\nAnswer with one JSON object and nothing else, in this shape:\n{example}"
        ask, problem = base, None
        for _ in range(retries + 1):
            text = self._chat_formatted(ask, schema, system, images, max_tokens)
            try:
                value = extract_json(text)
                errors = validate(value, schema)
            except ValueError as e:
                errors = [str(e)]
            if not errors:
                return value
            problem = "; ".join(errors[:4])
            ask = (f"{base}\n\nYour previous answer was rejected: {problem}. "
                   f"Previous answer:\n{text[:600]}\nAnswer again with the JSON object only.")
        raise LocalModelError(f"{self.model(bool(images))} did not give valid JSON: {problem}")

    def _chat_formatted(self, prompt, schema, system, images, max_tokens):
        """chat() with the strictest response format the server accepts."""
        while True:
            fmt = self.formats[0]
            response_format = {
                "json_schema": {"type": "json_schema",
                                "json_schema": {"name": "answer", "strict": True, "schema": strict_schema(schema)}},
                "json_object": {"type": "json_object"},
                None: None}[fmt]
            try:
                return self.chat(prompt, system, images, response_format, max_tokens)
            except LocalModelError as e:
                if fmt is None or "HTTP 4" not in str(e):
                    raise
                self.formats.pop(0)  # this server doesn't take that format: never try it again


def _example(schema):
    """A placeholder value with the schema's shape, to show the model."""
    if "enum" in schema:
        return "|".join(str(v) for v in schema["enum"])
    kind = schema.get("type")
    if kind == "object":
        return {k: _example(v) for k, v in schema.get("properties", {}).items()}
    if kind == "array":
        return [_example(schema.get("items", {"type": "string"}))]
    return {"string": schema.get("description", "..."), "boolean": False, "integer": 0, "number": 0}.get(kind)


# --- Batches -------------------------------------------------------------------------

def run_batch(items, fn, label=lambda item: str(item), quiet=False):
    """fn(item) for each item, printing progress. One item's failure doesn't stop the
    batch: its result is {"error": "..."}. An unreachable server does stop it."""
    results = []
    for i, item in enumerate(items, 1):
        try:
            result = fn(item)
        except LocalModelError as e:
            if "no local model at" in str(e) or "set STRATA_LLM_MODEL" in str(e):
                raise
            result = {"error": str(e)}
        results.append(result)
        if not quiet:
            mark = "ERR " if "error" in result else "    "
            print(f"{mark}[{i}/{len(items)}] {label(item)}", flush=True)
    return results
