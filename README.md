# Scriptor

Scriptor is a small Python library for defining and running simple rule-based scripts. A script is a sequence of conditional rules that, when a condition is met, execute one or more actions.

> Security: Scriptor uses eval() and exec(). Do not run untrusted or unreviewed scripts.

## Features
- Compact rule format (condition -> actions).
- Injection of variables into the script execution environment.
- Optional importing of modules via a prefix in the script.
- Minimal IDE environment (scriptorIDE.py) for editing and running scripts.

## Installation
Clone the repository and (optionally) install it in editable mode:

```bash
pip install py-scriptor
```

Or add the repository folder to PYTHONPATH.

## Script format
A script is a single string of rules separated by semicolons (`;`). Each rule uses `>>>` to separate the condition from the actions. Multiple actions are separated by commas.

Optional imports: prefix the script with module names separated by `::`, followed by the script body.

Format:
module1::module2::...::condition >>> action1, action2; condition2 >>> action3

- condition: a Python expression evaluated with the provided variables (eval).
- action: a Python statement executed with the provided variables (exec).

Examples:
- `x > 0 >>> x -= 1`
- `math::x > 0 >>> print(math.sqrt(x)), x -= 1`

## API

Class: RuleScript (in py_scriptor/__init__.py)

- RuleScript(script: str, vars: dict)
  - script: the script string. To import modules, use the prefix "module::...::script_body".
  - vars: a dict of variables available to conditions and actions. Imported modules are added to this dict under the module name.

- setVar(var: str, value)
  - Sets a variable in the runtime dictionary.

- getVar(var: str) -> Any
  - Retrieves a variable from the runtime dictionary.

- run(max_steps: int = 1000, cps: int = 0) -> bool
  - Executes the rules for up to max_steps iterations. Returns True on successful completion, False on import or execution errors.
  - Note: the cps parameter is not currently used.

- getImports() -> str
  - Returns the import line text for the imported modules (e.g., `import math`).

## Usage examples

Basic example:

```python
from scriptor import RuleScript

script = "x > 0 >>> print(x), x -= 1; x == 0 >>> print('done')"
vars = {"x": 3}

rs = RuleScript(script, vars)
rs.run(max_steps=10)
```

With module import:

```python
script = "math::x > 0 >>> print(math.sqrt(x)), x -= 1"
vars = {"x": 4}
rs = RuleScript(script, vars)
rs.run(max_steps=10)
```

## Security
Scriptor executes Python code using eval/exec. Do not run scripts from unknown sources. For safer execution consider:
- Running in an isolated process/container.
- Parsing the AST and restricting allowed operations.
- Limiting available globals.

## Contributing
Contributions are welcome. Suggestions:
- Improve the parser (multi-line scripts, comments).
- Add a safe execution mode (restricted globals/AST).
- Add unit tests and CI.

Open an issue before larger changes, then submit a pull request with tests.

## License
The LICENSE file contains the MIT license.

## Issues / Contact
Report bugs or feature requests at: https://github.com/libmaster169/py-scriptor/issues
