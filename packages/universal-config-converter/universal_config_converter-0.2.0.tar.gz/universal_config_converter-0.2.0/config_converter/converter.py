import json

# import yaml # Keep it commented or remove if fully replaced by ruamel
import tomlkit  # Use tomlkit instead of toml
from dotenv import dotenv_values, set_key
import os
import configparser  # Import configparser
import xmltodict  # Import xmltodict
from ruamel.yaml import YAML  # Import ruamel
from ruamel.yaml.comments import CommentedMap, CommentedSeq  # Import specific types
from jsonschema import validate  # Import validate function
from jsonschema.exceptions import ValidationError
from tomlkit.items import Table, Array

# We will add dotenv later if needed


def load_config(file_path, format):
    """Loads configuration from a file based on the format."""
    if format == "env":
        # dotenv_values reads the file and returns a dict
        # It automatically handles comments and empty lines
        return dotenv_values(file_path)
    elif format == "ini":
        config = configparser.ConfigParser()
        config.read(file_path)
        # Convert ConfigParser object to a nested dict for consistency
        data = {section: dict(config.items(section)) for section in config.sections()}
        # Include items in the default section if any (items without a section header)
        # Note: configparser reads default section keys only if they are accessed directly
        # This might require adjustment based on how default sections are handled
        default_section = config.defaults()
        if default_section:
            # Merge defaults carefully, maybe under a specific key like 'DEFAULT'
            # or handle based on expected structure.
            # Simple approach: merge into a special key if not empty.
            # A more complex approach might be needed depending on INI structure conventions.
            data["DEFAULT"] = dict(default_section)
        return data
    elif format == "xml":
        with open(file_path, "r", encoding="utf-8") as f:
            # process_namespaces=True can be useful for complex XML
            return xmltodict.parse(f.read())
    elif format == "yaml":  # Add yaml handling here
        yaml_loader = YAML(typ="rt")  # typ='rt' (round-trip) preserves comments/styling
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml_loader.load(f)
    elif format == "toml":  # Use tomlkit for loading
        with open(file_path, "r", encoding="utf-8") as f:
            return tomlkit.load(f)
    with open(file_path, "r", encoding="utf-8") as f:
        if format == "json":
            return json.load(f)
        # elif format == "yaml": # Remove old yaml handling
        #     return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported source format: {format}")


def save_config(data, file_path, format):
    """Saves configuration data to a file based on the format."""
    if format == "env":
        # Ensure the output file exists or create it for set_key
        # Create the file if it doesn't exist, otherwise do nothing
        if not os.path.exists(file_path):
            open(file_path, "w").close()
        elif (
            os.path.getsize(file_path) > 0
        ):  # Clear the file if it exists and is not empty
            open(file_path, "w").close()

        # Write key-value pairs, converting basic types to string
        # Note: This flattens the structure and only saves top-level keys.
        # Complex structures (dicts, lists) are ignored for .env.
        # set_key modifies the file directly.
        temp_env_vars = {}
        for key, value in data.items():
            if isinstance(value, (str, int, float, bool)):
                # Convert bool to lower case string as per common .env practice
                str_value = (
                    str(value).lower() if isinstance(value, bool) else str(value)
                )
                set_key(
                    file_path, key, str_value, quote_mode="never"
                )  # Avoid unnecessary quotes
                temp_env_vars[key] = str_value  # Keep track of what was written
            elif isinstance(value, dict):
                print(
                    f"Warning: Skipping nested dictionary for key '{key}' "
                    f"when saving to .env"
                )
            elif isinstance(value, list):
                print(f"Warning: Skipping list for key '{key}' when saving to .env")
            # Optionally, log a warning for other skipped complex types
            # else:
            #     print(
            #          f"Warning: Skipping complex value type {type(value)} "
            #          f"for key '{key}' when saving to .env"
            #     )

        # Verify what's actually in the file after modifications (optional but good practice)
        # final_env_values = dotenv_values(file_path)
        # print(f"Final .env content for {file_path}: {final_env_values}") # Debugging line
        return  # set_key handles file writing
    elif format == "ini":
        config = configparser.ConfigParser()
        # Iterate through the dictionary which should represent sections
        for section_name, section_data in data.items():
            if isinstance(section_data, dict):
                config[section_name] = {}
                for key, value in section_data.items():
                    # Ensure values are strings for configparser
                    config[section_name][key] = str(value)
            else:
                # Handle top-level keys - perhaps put them in a default section?
                # Or raise an error/warning as INI requires sections.
                # For now, let's put non-dict items in DEFAULT section if the key is 'DEFAULT'
                # or skip otherwise with a warning.
                if section_name == "DEFAULT" and not isinstance(value, (dict, list)):
                    # configparser handles DEFAULT section specially via defaults()
                    # It might be better to handle default section assignment explicitly if needed.
                    # Let's try adding non-dict/list items directly to the config object
                    # This might assign them to the DEFAULT section implicitly by some parsers
                    # but it's not standard. Let's stick to sections.
                    print(
                        f"Warning: Skipping non-dictionary top-level item "
                        f"'{section_name}' for INI output."
                    )
                elif not isinstance(section_data, dict):
                    print(
                        f"Warning: Skipping non-dictionary top-level item "
                        f"'{section_name}' for INI output."
                    )

        with open(file_path, "w") as f:
            config.write(f)
        return
    elif format == "xml":
        # xmltodict requires a single root element.
        # If data is a dict with one key, use that as root.
        # Otherwise, wrap the data in a default 'root' element.
        if isinstance(data, dict) and len(data) == 1:
            root_key = list(data.keys())[0]
            # Ensure the value is also suitable for unparse
            xml_data = {root_key: data[root_key]}
        else:
            xml_data = {"root": data}
        # Write with encoding='utf-8'
        with open(file_path, "w", encoding="utf-8") as f:
            # pretty=True for readable output
            # indent='  ' for standard indentation
            f.write(xmltodict.unparse(xml_data, pretty=True, indent="  "))
        return
    elif format == "yaml":  # Add yaml handling here
        yaml_dumper = YAML(typ="rt")
        yaml_dumper.indent(mapping=2, sequence=4, offset=2)
        with open(file_path, "w", encoding="utf-8") as f:
            yaml_dumper.dump(data, f)
        return
    elif format == "toml":  # Use tomlkit for saving
        with open(file_path, "w", encoding="utf-8") as f:
            tomlkit.dump(data, f)
        return

    with open(file_path, "w", encoding="utf-8") as f:
        if format == "json":
            json.dump(
                data, f, indent=4, ensure_ascii=False
            )  # ensure_ascii=False for broader char support
        # elif format == "yaml": # Remove old yaml handling
        #     yaml.dump(
        #         data, f, default_flow_style=False, allow_unicode=True
        #     )  # allow_unicode=True
        else:
            raise ValueError(f"Unsupported target format: {format}")


def validate_data(data, schema_path):
    """Validates data against a JSON schema file."""
    if not schema_path:
        return  # No schema provided, skip validation

    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        raise ValueError(f"Error loading schema file '{schema_path}': {e}")

    try:
        # Convert ruamel types to standard Python dict/list for validation
        if isinstance(data, (CommentedMap, CommentedSeq)):
            # Convert ruamel types to standard Python dict/list using a helper
            data_for_validation = _convert_ruamel_to_standard(data)
        else:
            data_for_validation = data

        validate(instance=data_for_validation, schema=schema)
        print(f"Data validated successfully against schema '{schema_path}'.")
    except ValidationError as e:
        raise ValueError(f"Schema validation failed: {e.message}")
    except Exception as e:
        # Catch other potential errors during validation
        raise ValueError(f"An error occurred during schema validation: {e}")


# Helper function to recursively convert ruamel types
def _convert_ruamel_to_standard(item):
    if isinstance(item, CommentedMap):
        return {k: _convert_ruamel_to_standard(v) for k, v in item.items()}
    elif isinstance(item, CommentedSeq):
        return [_convert_ruamel_to_standard(elem) for elem in item]
    else:
        return item


# Helper function to recursively convert tomlkit types
def _convert_tomlkit_to_standard(item):
    if isinstance(item, Table):
        # Use item.value for Tables obtained from parsing
        # Use item.items() if constructing manually?
        # Let's try .value first for loaded data
        try:
            # Use .unwrap() to get the underlying dict/list
            return {
                k: _convert_tomlkit_to_standard(v) for k, v in item.unwrap().items()
            }
        except AttributeError:
            # Fallback or different handling if .unwrap() not available
            return {k: _convert_tomlkit_to_standard(v) for k, v in item.items()}
    elif isinstance(item, Array):
        return [_convert_tomlkit_to_standard(elem) for elem in item.unwrap()]
    elif hasattr(
        item, "value"
    ):  # Handle AoT, etc. by getting primitive value if possible
        return item.value
    else:
        return item


def convert(
    input_file,
    source_format,
    target_format,
    output_file,
    input_schema=None,
    output_schema=None,
):
    """Converts a configuration file from source_format to target_format,
    optionally validating against JSON schemas.
    """
    # Normalize formats to lower case
    source_format = source_format.lower()
    target_format = target_format.lower()

    if source_format == target_format:
        raise ValueError("Source and target formats cannot be the same.")

    # Load data from the source file
    data = load_config(input_file, source_format)

    # Validate input data if schema provided
    if input_schema:
        print(f"Validating input data from '{input_file}'...")
        validate_data(data, input_schema)

    # Validate output data if schema provided
    # Note: Validation happens *before* saving, using the in-memory data.
    if output_schema:
        print(f"Validating output data for '{output_file}'...")
        validate_data(data, output_schema)

    # Save data to the target file
    save_config(data, output_file, target_format)
