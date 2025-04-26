# Winding Markdown Extension

Winding is a Python module that provides an EBNF (Extended Backus-Naur Form) grammar for the Winding Markdown extension. This extension enhances Markdown, allowing to specify scenes, layout and agentic behaviours.

## Features

- Defines a clear and concise EBNF grammar for the Winding Markdown extension.
- Facilitates the parsing and interpretation of Winding Markdown documents.
- Easy to integrate into existing Markdown processing workflows.

## Installation

You can install the Winding module from PyPI using pip:

```bash
pip install winding
```

## Usage

Here is a simple example of how to use the Winding module:

```python
from winding import grammar

# Example usage of the grammar
ebnf_definition = grammar.load_grammar()
print(ebnf_definition)
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.