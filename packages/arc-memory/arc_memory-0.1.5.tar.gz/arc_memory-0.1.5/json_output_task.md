**Specification: Add JSON Output Format to `arc trace file` CLI Command and Release**

**1. Goal:**
Modify the existing `arc trace file` command within the Arc Memory SDK's Command Line Interface (CLI) to support outputting the trace results in JSON format. This provides a stable, machine-readable interface for programmatic consumers like the VS Code extension. Subsequently, release this updated version to PyPI for user availability.

**2. Target Command:**
`arc trace file <file_path> <line_number> [options]`

**3. Proposed Change: Add `--format` argument**
Introduce a new optional argument, `--format`, to the `arc trace file` command.

*   **Argument Name:** `--format`
*   **Accepted Values:**
    *   `text` (default): Maintains the current human-readable output format.
    *   `json`: Outputs the results as a JSON array of objects.
*   **Default Behavior:** If the `--format` argument is omitted, the command should behave exactly as it does currently, outputting the results in the human-readable text format.

**4. Behavior with `--format=json`:**

*   The command should parse the `file_path` and `line_number` arguments as usual.
*   It should invoke the underlying Python function responsible for fetching the trace history (likely similar or identical to `arc_memory.trace.trace_history_for_file_line` described in `sdk-docs/api/trace.md`).
*   The options provided to the CLI command (e.g., `--max-results`, `--max-hops` if they exist or are added) should be passed to the underlying function.
*   The function will return a list of dictionaries, where each dictionary represents a node in the history trail (e.g., commit, PR, issue, ADR).
*   Instead of formatting this list into human-readable text, the CLI handler should:
    *   Take the **entire list of dictionaries** returned by the function.
    *   Use Python's standard `json` library (specifically `json.dumps()`) to serialize this list into a single JSON string.
    *   Print this resulting JSON string directly to **standard output (stdout)**.
    *   Ensure no other text (like informational logs) is printed to stdout when `json` format is selected. stderr should still be used for errors.

**5. Output Specification (`--format=json`):**

The JSON output printed to stdout MUST be a valid JSON array (`[...]`). Each element in the array will be a JSON object (`{...}`) corresponding directly to one dictionary returned by the underlying `trace_history_for_file_line` function.

Based on `sdk-docs/api/trace.md`, each object in the JSON array should contain at least the following keys:

*   `type` (string): e.g., "commit", "pr", "issue", "adr", "file"
*   `id` (string or int): Unique identifier.
*   `title` (string): Title of the node.
*   `timestamp` (string): Timestamp in ISO format.

And potentially type-specific keys:

*   For `commit`: `author` (string), `sha` (string)
*   For `pr`: `number` (int), `state` (string), `url` (string)
*   For `issue`: `number` (int), `state` (string), `url` (string)
*   For `adr`: `status` (string), `decision_makers` (list of strings), `path` (string)

The array should be sorted chronologically, newest event first, matching the behavior of the underlying Python function.

**6. Example Usage:**

```bash
# Existing behavior (implicit --format=text)
arc trace file src/auth/service.py 900

# New behavior with JSON output
arc trace file src/auth/service.py 900 --format=json --max-results=2
```

**7. Example JSON Output (`stdout`):**

```json
[
  {
    "type": "pr",
    "id": "PR_kwDOK9Z4x85qXE9P",
    "title": "Refactor token expiry logic",
    "timestamp": "2024-03-21T10:30:00Z",
    "number": 298,
    "state": "MERGED",
    "url": "https://github.com/example/repo/pull/298"
  },
  {
    "type": "adr",
    "id": "ADR_12",
    "title": "Standardize Token Expiry Durations",
    "timestamp": "2024-03-05T15:00:00Z",
    "status": "accepted",
    "decision_makers": ["lead_architect@example.com"],
    "path": "docs/adr/012-token-expiry.md"
  }
]
```
*(Note: `id` formats are illustrative)*

**8. Implementation Notes:**

*   Integrate the `--format` argument using the existing CLI framework (e.g., `argparse`, `click`, `Typer`).
*   Use a conditional check on the parsed `format` value to determine whether to format as text or serialize as JSON using `json.dumps(results, indent=None)` (no indentation needed for machine parsing).
*   Ensure the underlying call to the trace function remains the same.

**9. Error Handling:**

*   If the underlying trace function encounters an error (e.g., file not found, database issue, git blame failure), the CLI command should still exit with a non-zero status code and print error messages to **standard error (stderr)**, regardless of the selected format. It should *not* print partial or error-representing JSON to stdout in these cases.
*   If the trace function returns an empty list (`[]`), the JSON output to stdout should be exactly `'[]'`.

**10. Release and Distribution:**

*   **Version Increment:** After implementing and testing the `--format=json` feature, the SDK's version number in `pyproject.toml` (or equivalent) **MUST** be incremented according to semantic versioning principles (e.g., from `0.1.0` to `0.1.1` for a backwards-compatible addition, or `0.2.0` if other breaking changes are included).
*   **Build Package:** Generate the distribution archives (wheel and source distribution) using standard Python packaging tools (e.g., `python -m build`).
*   **Publish to PyPI:** Upload the newly built distribution files to the Python Package Index (PyPI) [https://pypi.org/project/arc-memory/] using a tool like `twine` (e.g., `python -m twine upload dist/*`).
*   **Rationale:** Publishing the updated version to PyPI is essential so that users installing `arc-memory` via `pip` or `uv` receive the version containing the `--format=json` capability, which is required for the VS Code extension to function correctly.

---

This updated specification now includes the crucial final step of versioning and publishing the changes to PyPI.
