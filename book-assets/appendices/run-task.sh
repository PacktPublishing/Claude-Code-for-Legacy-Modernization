#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:?usage: run-task.sh TASK_ID EXPECTED_TYPE}"
EXPECTED_TYPE="${2:?expected type from the admitted contract is required}"
[[ "${TASK_ID}" =~ ^[A-Za-z0-9][A-Za-z0-9_-]*$ ]] || exit 24
CONTRACT_DIR="contracts/tasks/${TASK_ID}"
RUN_DIR="evidence/runs/${TASK_ID}"
SETTINGS_FILE="contracts/policies/controlled-settings.json"

if [[ ! -f "${CONTRACT_DIR}/prompt.txt" ]]; then
  printf 'missing prompt for %s\n' "${TASK_ID}" >&2
  exit 20
fi

if [[ ! -f "${CONTRACT_DIR}/return.schema.json" ]]; then
  printf 'missing return schema for %s\n' "${TASK_ID}" >&2
  exit 21
fi

if [[ -e "${RUN_DIR}" ]]; then
  printf 'run directory already exists: %s\n' "${RUN_DIR}" >&2
  exit 22
fi

mkdir -p "evidence/runs"
mkdir "${RUN_DIR}"  # Atomic refusal of ordinary directory reuse.
cp "${CONTRACT_DIR}/return.schema.json" "${RUN_DIR}/schema.original.json"
printf '%s\n' "${TASK_ID}" "${EXPECTED_TYPE}" > "${RUN_DIR}/invocation.txt"
if python3 tools/contracts/validate_task_return.py --preflight \
  "${RUN_DIR}/schema.original.json" "${TASK_ID}" "${EXPECTED_TYPE}" \
  > "${RUN_DIR}/schema.admitted.json" 2> "${RUN_DIR}/preflight.stderr"; then
  printf '0\n' > "${RUN_DIR}/preflight-status.txt"
else
  PREFLIGHT_STATUS=$?
  printf '%s\n' "${PREFLIGHT_STATUS}" > "${RUN_DIR}/preflight-status.txt"
  exit "${PREFLIGHT_STATUS}"
fi
SCHEMA_JSON="$(<"${RUN_DIR}/schema.admitted.json")"
python3 scripts/capture_changes.py begin "${RUN_DIR}"
claude --version > "${RUN_DIR}/claude-version.txt"

set +e
claude -p \
  --settings "${SETTINGS_FILE}" \
  --permission-mode dontAsk \
  --output-format json \
  --json-schema "${SCHEMA_JSON}" \
  "$(<"${CONTRACT_DIR}/prompt.txt")" \
  > "${RUN_DIR}/stdout.json" \
  2> "${RUN_DIR}/stderr.txt"
TASK_STATUS=$?
set -e

printf '%s\n' "${TASK_STATUS}" > "${RUN_DIR}/exit-status.txt"
python3 scripts/capture_changes.py end "${RUN_DIR}"

if [[ "${TASK_STATUS}" -eq 0 ]]; then
  if ! python3 -c 'import json,sys; from pathlib import Path; sys.path.insert(0,"tools/contracts"); from validate_artifacts import load_data; value=load_data(Path(sys.argv[1]),"json"); payload=value.get("structured_output") if isinstance(value,dict) else None; sys.exit("invalid or absent structured_output") if not isinstance(payload,dict) or value.get("is_error") is True else None; json.dump(payload, open(sys.argv[2], "w"), indent=2)' \
    "${RUN_DIR}/stdout.json" "${RUN_DIR}/agent-return.json"; then
    printf '%s\n' '{"structural_subset_valid":false,"reason":"invalid or absent envelope"}' > "${RUN_DIR}/return-validation.json"
    exit 23
  fi
  python3 tools/contracts/validate_task_return.py \
    "${RUN_DIR}/schema.admitted.json" \
    "${RUN_DIR}/agent-return.json" "${TASK_ID}" "${EXPECTED_TYPE}" \
    > "${RUN_DIR}/return-validation.json"
else
  printf '%s\n' \
    '{"structural_subset_valid":false,"status":"not-run","reason":"claude exit was nonzero"}' \
    > "${RUN_DIR}/return-validation.json"
  exit "${TASK_STATUS}"
fi
