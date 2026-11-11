from __future__ import annotations

import json
import sys
from pathlib import Path

from validate_artifacts import ValidationError, load_data, validate, validate_schema_dialect


def admit_schema(path: Path, task_id: str, task_type: str) -> dict:
    schema = load_data(path, 'json')
    validate_schema_dialect(schema)
    if not task_id.strip() or not task_type.strip():
        raise ValidationError('expected identity and type must be nonblank')
    properties = schema.setdefault('properties', {})
    for key, expected in (('task_id', task_id), ('task_type', task_type)):
        validate(expected, properties.get(key, {}))
        properties.setdefault(key, {})['const'] = expected
    required = schema.setdefault('required', [])
    for key in ('task_id', 'task_type'):
        if key not in required:
            required.append(key)
    validate_schema_dialect(schema)
    return schema


def main() -> None:
    try:
        if len(sys.argv) == 5 and sys.argv[1] == '--preflight':
            schema = admit_schema(Path(sys.argv[2]), sys.argv[3], sys.argv[4])
            print(json.dumps(schema, sort_keys=True, allow_nan=False))
            return
        if len(sys.argv) != 5:
            raise ValidationError('usage: validate_task_return.py SCHEMA RETURN TASK_ID EXPECTED_TYPE; or --preflight SCHEMA TASK_ID EXPECTED_TYPE')
        schema = load_data(Path(sys.argv[1]), 'json')
        value = load_data(Path(sys.argv[2]), 'json')
        validate(value, schema)
        if not isinstance(value, dict):
            raise ValidationError('return must be an object')
        task_id = value.get('task_id')
        if not isinstance(task_id, str) or not task_id.strip():
            raise ValidationError('task_id must be nonblank')
        if task_id != sys.argv[3]:
            raise ValidationError('task_id does not match invocation')
        if not sys.argv[4].strip() or value.get('task_type') != sys.argv[4]:
            raise ValidationError('task_type does not match admitted invocation')
        if sys.argv[4] == 'discovery' and value.get('files_changed') != []:
            raise ValidationError('read-only discovery must have no agent file changes')
    except (ValidationError, ValueError, TypeError, OSError) as error:
        print(json.dumps({'structural_subset_valid': False, 'error': str(error)}, sort_keys=True))
        raise SystemExit(1)
    print(json.dumps({'structural_subset_valid': True, 'task_id': task_id}, sort_keys=True))


if __name__ == '__main__':
    main()
