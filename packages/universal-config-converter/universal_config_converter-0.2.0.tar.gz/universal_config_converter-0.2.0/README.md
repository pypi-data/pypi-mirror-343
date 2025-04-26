# Universal Config Converter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Tired of manually converting configuration files between JSON, YAML, TOML, .env, and others?** This simple command-line tool aims to make your life easier by automating the conversion process.

`config-converter` allows you to effortlessly switch between common configuration formats, saving you time and reducing potential errors.

## Goals

*   Provide a **single, reliable CLI tool** for converting between the most popular configuration formats.
*   Ensure the conversion process is **accurate and preserves data structure**.
*   Maintain a **simple and intuitive user interface**.
*   Build a **community-driven tool** that adapts to new formats and user needs.

## Features & Roadmap

Here's what the tool can do and what's planned for the future:

*   [x] **Command-Line Interface (CLI):** Easy-to-use commands via `click`.
*   [x] **Core Conversion Logic:** Foundation for loading and saving data.
*   [x] **JSON Support:** Convert to/from JSON (`.json`).
*   [x] **YAML Support:** Convert to/from YAML (`.yaml`, `.yml`).
*   [x] **TOML Support:** Convert to/from TOML (`.toml`).
*   [x] **.env Support:** Convert to/from environment variable files (`.env`).
*   [x] **INI Support:** Convert to/from INI files (`.ini`).
*   [x] **XML Support:** Convert to/from XML files (`.xml`).
*   [ ] **Comment Preservation:** Attempt to keep comments intact during conversion.
    *   [x] YAML (using `ruamel.yaml`, load/save cycle preserves comments)
    *   [ ] INI (Difficult with standard `configparser`, potential future enhancement)
    *   [x] TOML (using `tomlkit`, load/save cycle preserves comments)
    *   Note: Comments are generally lost for JSON, .env, XML conversions.
*   [x] **Data Validation:** Option to validate input/output against a JSON schema.
*   [x] **Basic Unit Tests:** Initial tests for core functionality.
*   [x] **Comprehensive Test Suite:** More tests covering edge cases and all formats (Further additions welcome!).
*   [x] **Pre-commit Hooks:** Ensure code quality and consistency.
*   [x] **PyPI Packaging:** Make it easily installable via `pip install config-converter`.
*   [x] **GitHub Actions CI:** Automate testing on pushes and pull requests.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/velibenek/universal-config-converter.git
    cd universal-config-converter
    ```
2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # Also install pytest for running tests
    pip install pytest
    ```

## Usage

Convert a file from one format to another:

```bash
config-converter -i <input_path> -s <format> -t <format> -o <output_path> [options]
```

**Example:** Convert `config.json` to `config.yaml`:

```bash
config-converter -i config.json -s json -t yaml -o config.yaml
```

**Example with Input Validation:** Validate `config.json` against `schema.json` before converting:

```bash
config-converter -i config.json -s json -t yaml -o config.yaml --input-schema schema.json
```

**Example with Output Validation:** Convert `config.json` to `config.yaml` and validate the result against `schema.json` before saving:

```bash
config-converter -i config.json -s json -t yaml -o config.yaml --output-schema schema.json
```

Supported formats currently: `json`, `yaml`, `toml`, `env`, `ini`, `xml`.

## Contributing

Contributions are welcome! If you'd like to help improve `config-converter`, please feel free to:

*   Report bugs or suggest features by opening an issue.
*   Submit pull requests with bug fixes or new features (especially those on the roadmap!).
*   Improve the documentation.

Please check the `CONTRIBUTING.md` file (to be created) for more detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[Homepage](https://github.com/velibenek/universal-config-converter)
[Issues](https://github.com/velibenek/universal-config-converter/issues)
