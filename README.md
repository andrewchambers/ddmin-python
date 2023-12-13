# ddmin: Delta Debugging Minimizer

## Overview
ddmin is a Python library and command line tool designed for minimizing a data set while still retaining a specific property, typically for the purpose of debugging. It employs the technique of delta debugging, a systematic approach to isolate the minimal cause of a bug in complex input data. This library is especially useful for developers and testers who work on debugging software and need to identify the minimal test case that reproduces a bug.

## Requirements
- Python 3.x

## Installation
Clone the repository or download the source code. No external dependencies are required.

## Usage

### As a Library
Import `delta_debug` from ddmin and use it in your Python scripts:

```python
from ddmin import delta_debug

# Define your 'interesting_test' function
def interesting_test(input_data):
    for line in lines:
        if "bug" in line:
            return True
    return False
minimized_data = delta_debug(interesting_test, ["a", "b", "bug", "c", "bug", "bug"])
# minimized data is now a single bug causing input: ["bug"]
```

### Command-Line Tool
ddmin can be used as a command-line tool to minimize files:

```bash
python ddmin.py --interesting [path_to_interesting_test_script] --to-minimize [path_to_file_to_minimize] [--bytes]
```

- `--interesting`: Path to the script that returns exit code 0 if the current state of the file is interesting.
- `--to-minimize`: Path to the file that you want to minimize. The file will be modified in place.
- `--bytes`: Optional flag to minimize by bytes instead of lines.

### Example
To minimize a text file `example.txt` using a test script `test_script.py`:

```bash
python ddmin.py --interesting test_script.py --to-minimize example.txt
```

## Contributing
Contributions to ddmin are welcome! Please read the contributing guidelines before submitting pull requests.

