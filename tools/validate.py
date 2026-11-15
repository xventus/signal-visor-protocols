"""Checks every protocol definition in this repository.

    pip install jsonschema==4.23.0
    python tools/validate.py

Runs the JSON schema and the rules the schema cannot express: a definition lives in
<group>/<id>/<id>.json, and no two definitions share an id. Exits non-zero on any problem.
"""
import json
import pathlib
import sys

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parent.parent
GROUPS = ("remotes", "sensors")


def main() -> int:
    schema = json.loads((ROOT / "schema" / "protocol.schema.json").read_text(encoding="utf-8"))
    validator_class = jsonschema.validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)

    problems = []
    seen = {}
    files = sorted(p for group in GROUPS for p in (ROOT / group).rglob("*.json"))
    for path in files:
        name = path.relative_to(ROOT).as_posix()
        try:
            definition = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            problems.append(f"{name}: not valid JSON: {error}")
            continue

        for error in validator.iter_errors(definition):
            where = "/".join(str(part) for part in error.absolute_path) or "(top)"
            problems.append(f"{name}: {where}: {error.message}")

        definition_id = definition.get("id")
        if definition_id and (path.stem != definition_id or path.parent.name != definition_id):
            problems.append(f"{name}: should be <group>/{definition_id}/{definition_id}.json")
        if definition_id in seen:
            problems.append(f"{name}: id '{definition_id}' is already used by {seen[definition_id]}")
        seen.setdefault(definition_id, name)

    for problem in problems:
        print(problem)
    print(f"{len(files)} definition(s) checked, {len(problems)} problem(s).")
    return 1 if problems or not files else 0


if __name__ == "__main__":
    sys.exit(main())
