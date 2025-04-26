import pytest
import json

# import yaml # Removed unused import
import tomlkit
from config_converter.converter import (
    convert,
    load_config,
    save_config,
    _convert_tomlkit_to_standard,
)
from dotenv import dotenv_values
import configparser
import xmltodict
from ruamel.yaml import YAML, YAMLError
from xml.parsers.expat import ExpatError

# from tomlkit import TOMLDocument # Removed unused import
from tomlkit.exceptions import TOMLKitError

# Sample data for testing
SAMPLE_DATA = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "user": "test_user",
        "enabled": True,
    },
    "api_settings": {"key": "abcdef12345", "retries": 3},
    "feature_flags": ["new_ui", "beta_feature"],
}

# Sample data specifically for .env testing (flat structure)
FLAT_SAMPLE_DATA = {
    "API_KEY": "abcdef12345",
    "DATABASE_HOST": "db.example.com",
    "DATABASE_PORT": "5432",  # .env values are typically strings
    "DEBUG_MODE": "true",
    "TIMEOUT_SECONDS": "30",
}

# Sample data specifically for INI testing (sections)
INI_SAMPLE_DATA = {
    "database": {"host": "db.example.com", "port": "1521", "enabled": "true"},
    "user_settings": {"theme": "dark", "notifications": "false"},
}

# Sample data specifically for XML testing
# Note: xmltodict converts numbers and booleans back to strings often
# Need to be careful with type comparisons
XML_SAMPLE_STR = """<?xml version="1.0" encoding="utf-8"?>
<config>
  <database host="localhost">
    <port>5432</port>
    <user>xml_user</user>
    <enabled>true</enabled>
  </database>
  <api key="key-from-xml">
    <retries>5</retries>
  </api>
  <flags>
    <flag>xml_flag1</flag>
    <flag>xml_flag2</flag>
  </flags>
</config>"""

XML_SAMPLE_DATA_FROM_STR = {
    "config": {
        "database": {
            "@host": "localhost",
            "port": "5432",
            "user": "xml_user",
            "enabled": "true",
        },
        "api": {"@key": "key-from-xml", "retries": "5"},
        "flags": {"flag": ["xml_flag1", "xml_flag2"]},
    }
}

# YAML with comments
YAML_WITH_COMMENTS = """
# Database configuration section
database:
  host: localhost # The database server
  port: 5432
  user: test_user # Username
  enabled: true

# API details
api_settings:
  key: abcdef12345 # Secret key
  retries: 3

feature_flags: # List of features
  - new_ui
  - beta_feature
"""

# TOML with comments
TOML_WITH_COMMENTS = """
# TOML Configuration Example

[database] # Database settings
host = "localhost"
port = 5432 # Default port
user = "test_user"
enabled = true

[api_settings] # API keys and config
key = "abcdef12345" # The API key
retries = 3

# Feature flags list
feature_flags = ["new_ui", "beta_feature"]
"""

# Define schema paths relative to the test file
VALID_SCHEMA_PATH = "tests/schemas/valid_schema.json"
INVALID_SCHEMA_PATH = "tests/schemas/invalid_schema.json"


@pytest.fixture
def temp_files(tmp_path):
    """Fixture to create temporary files for testing."""
    paths = {
        "json_in": tmp_path / "input.json",
        "yaml_in": tmp_path / "input.yaml",
        "yaml_comments_in": tmp_path / "input_comments.yaml",
        "toml_in": tmp_path / "input.toml",
        "toml_comments_in": tmp_path / "input_comments.toml",
        "env_in": tmp_path / "input.env",
        "ini_in": tmp_path / "input.ini",
        "xml_in": tmp_path / "input.xml",
        "out": tmp_path / "output",
    }
    # Create initial files
    with open(paths["json_in"], "w") as f:
        json.dump(SAMPLE_DATA, f, indent=4)
    # Use ruamel.yaml to write initial YAML for consistency
    yaml_writer = YAML()
    yaml_writer.indent(mapping=2, sequence=4, offset=2)
    with open(paths["yaml_in"], "w", encoding="utf-8") as f:
        yaml_writer.dump(SAMPLE_DATA, f)
    # Create YAML with comments
    with open(paths["yaml_comments_in"], "w", encoding="utf-8") as f:
        f.write(YAML_WITH_COMMENTS)

    with open(paths["toml_in"], "w", encoding="utf-8") as f:
        tomlkit.dump(SAMPLE_DATA, f)
    # Create TOML with comments
    with open(paths["toml_comments_in"], "w", encoding="utf-8") as f:
        f.write(TOML_WITH_COMMENTS)
    # Create sample .env file
    with open(paths["env_in"], "w") as f:
        for key, value in FLAT_SAMPLE_DATA.items():
            f.write(f"{key}={value}\n")
    # Create sample .ini file
    config = configparser.ConfigParser()
    for section, data in INI_SAMPLE_DATA.items():
        config[section] = data
    with open(paths["ini_in"], "w") as f:
        config.write(f)
    # Create sample .xml file
    with open(paths["xml_in"], "w", encoding="utf-8") as f:
        f.write(XML_SAMPLE_STR)
    return paths


def test_json_to_yaml(temp_files):
    """Test converting JSON to YAML."""
    output_path = temp_files["out"].with_suffix(".yaml")
    convert(temp_files["json_in"], "json", "yaml", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "yaml")
    # ruamel.yaml preserves types better, direct comparison might work
    # Convert both to basic dicts for robust comparison if needed
    # assert json.loads(json.dumps(loaded_data)) == SAMPLE_DATA
    # Direct comparison (might be sensitive to types like CommentedMap)
    assert loaded_data == SAMPLE_DATA


def test_yaml_to_toml(temp_files):
    """Test converting YAML to TOML."""
    output_path = temp_files["out"].with_suffix(".toml")
    convert(temp_files["yaml_in"], "yaml", "toml", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "toml")
    # Convert tomlkit data to standard dict for comparison
    assert _convert_tomlkit_to_standard(loaded_data) == SAMPLE_DATA


def test_toml_to_json(temp_files):
    """Test converting TOML to JSON."""
    output_path = temp_files["out"].with_suffix(".json")
    convert(temp_files["toml_in"], "toml", "json", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "json")
    assert loaded_data == SAMPLE_DATA


def test_same_format_error(temp_files):
    """Test that converting to the same format raises an error."""
    output_path = temp_files["out"].with_suffix(".json")
    with pytest.raises(
        ValueError, match="Source and target formats cannot be the same."
    ):
        convert(temp_files["json_in"], "json", "json", output_path)


def test_unsupported_source_format_error(temp_files):
    """Test loading an unsupported format raises an error."""
    with pytest.raises(ValueError, match="Unsupported source format: unknown"):
        load_config(
            temp_files["json_in"], "unknown"
        )  # File content doesn't matter here


def test_unsupported_target_format_error(temp_files):
    """Test saving to an unsupported format raises an error."""
    output_path = temp_files["out"].with_suffix(".unknown")
    with pytest.raises(ValueError, match="Unsupported target format: unknown"):
        save_config(SAMPLE_DATA, output_path, "unknown")


def test_env_to_json(temp_files):
    """Test converting .env to JSON."""
    output_path = temp_files["out"].with_suffix(".json")
    convert(temp_files["env_in"], "env", "json", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "json")
    # .env values are loaded as strings by dotenv_values
    assert loaded_data == FLAT_SAMPLE_DATA


def test_json_to_env(temp_files):
    """Test converting JSON to .env (only top-level simple values)."""
    # Create a simplified JSON input for this test
    simple_json_path = temp_files["json_in"].parent / "simple.json"
    simple_data = {
        "SERVICE_URL": "https://api.example.com",
        "RETRIES": 5,
        "ENABLED": False,
        "FLOAT_VAL": 1.23,
        "NESTED": {"a": 1},  # This should be ignored
        "LIST_VAL": [1, 2],  # This should be ignored
    }
    expected_env_data = {
        "SERVICE_URL": "https://api.example.com",
        "RETRIES": "5",
        "ENABLED": "false",
        "FLOAT_VAL": "1.23",
        # Nested and List are excluded
    }
    with open(simple_json_path, "w") as f:
        json.dump(simple_data, f, indent=4)

    output_path = temp_files["out"].with_suffix(".env")
    convert(simple_json_path, "json", "env", output_path)
    assert output_path.exists()

    # Load the created .env file
    loaded_data = dotenv_values(output_path)

    assert loaded_data == expected_env_data


def test_ini_to_json(temp_files):
    """Test converting INI to JSON."""
    output_path = temp_files["out"].with_suffix(".json")
    convert(temp_files["ini_in"], "ini", "json", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "json")
    # configparser reads all values as strings
    assert loaded_data == INI_SAMPLE_DATA


def test_json_to_ini(temp_files):
    """Test converting JSON (with structure similar to INI) to INI."""
    # Use SAMPLE_DATA which has nested dicts suitable for INI sections
    input_path = temp_files["json_in"]
    output_path = temp_files["out"].with_suffix(".ini")
    convert(input_path, "json", "ini", output_path)
    assert output_path.exists()

    # Load the created INI file
    config = configparser.ConfigParser()
    config.read(output_path)
    loaded_data = {
        section: dict(config.items(section)) for section in config.sections()
    }

    # Prepare expected data: Convert all values from SAMPLE_DATA to strings
    expected_ini_data = {}
    for section, data in SAMPLE_DATA.items():
        if isinstance(data, dict):
            expected_ini_data[section] = {k: str(v) for k, v in data.items()}
        # Skip non-dict top-level items like 'feature_flags' in SAMPLE_DATA for INI

    assert loaded_data == expected_ini_data


def test_xml_to_json(temp_files):
    """Test converting XML to JSON."""
    output_path = temp_files["out"].with_suffix(".json")
    convert(temp_files["xml_in"], "xml", "json", output_path)
    assert output_path.exists()
    # Load the JSON and compare with the expected dictionary structure from XML
    with open(output_path, "r", encoding="utf-8") as f:
        loaded_data = json.load(f)
    assert loaded_data == XML_SAMPLE_DATA_FROM_STR


def test_json_to_xml(temp_files):
    """Test converting JSON to XML."""
    # Use a dictionary structure that translates well to XML
    json_data_for_xml = {
        "app_config": {
            "server": {"@id": "main", "#text": "192.168.1.100"},
            "port": "8080",
            "features": {"feature": ["A", "B"]},
        }
    }
    json_input_path = temp_files["out"].parent / "input_for_xml.json"
    with open(json_input_path, "w", encoding="utf-8") as f:
        json.dump(json_data_for_xml, f, indent=4)

    output_path = temp_files["out"].with_suffix(".xml")
    convert(json_input_path, "json", "xml", output_path)
    assert output_path.exists()

    # Load the created XML and convert back to dict to compare
    # This verifies the structure is preserved reasonably well
    with open(output_path, "r", encoding="utf-8") as f:
        loaded_data = xmltodict.parse(f.read())

    # Comparing dicts is easier than comparing XML strings
    assert loaded_data == json_data_for_xml


def test_yaml_comment_preservation(temp_files):
    """Test that YAML comments are preserved during YAML load/save cycle."""
    input_path = temp_files["yaml_comments_in"]
    output_path = temp_files["out"].parent / "output_comments_preserved.yaml"

    # Load the data using ruamel.yaml (which load_config now does)
    loaded_data = load_config(input_path, "yaml")

    # Save the data back using ruamel.yaml (which save_config now does)
    save_config(loaded_data, output_path, "yaml")

    # Read the output file content
    with open(output_path, "r", encoding="utf-8") as f:
        output_content = f.read()

    # Read the input file content again for comparison
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Assert that the output content is identical to the input content
    # after stripping leading/trailing whitespace to handle potential
    # newline differences at the beginning/end of file.
    assert output_content.strip() == input_content.strip()


def test_validation_input_success(temp_files):
    """Test successful input validation."""
    output_path = temp_files["out"].with_suffix(".yaml")
    # Should run without errors
    convert(
        temp_files["json_in"],
        "json",
        "yaml",
        output_path,
        input_schema=VALID_SCHEMA_PATH,
    )
    assert output_path.exists()


def test_validation_output_success(temp_files):
    """Test successful output validation."""
    output_path = temp_files["out"].with_suffix(".yaml")
    # Should run without errors
    convert(
        temp_files["json_in"],
        "json",
        "yaml",
        output_path,
        output_schema=VALID_SCHEMA_PATH,
    )
    assert output_path.exists()


def test_validation_input_failure(temp_files):
    """Test failed input validation."""
    output_path = temp_files["out"].with_suffix(".yaml")
    with pytest.raises(ValueError, match="Schema validation failed"):
        convert(
            temp_files["json_in"],
            "json",
            "yaml",
            output_path,
            input_schema=INVALID_SCHEMA_PATH,
        )
    assert not output_path.exists()  # Should fail before writing output


def test_validation_output_failure(temp_files):
    """Test failed output validation."""
    output_path = temp_files["out"].with_suffix(".yaml")
    with pytest.raises(ValueError, match="Schema validation failed"):
        convert(
            temp_files["json_in"],
            "json",
            "yaml",
            output_path,
            output_schema=INVALID_SCHEMA_PATH,
        )
    assert not output_path.exists()  # Should fail before writing output


def test_validation_schema_not_found(temp_files):
    """Test error when schema file does not exist."""
    output_path = temp_files["out"].with_suffix(".yaml")
    with pytest.raises(ValueError, match="Error loading schema file"):
        convert(
            temp_files["json_in"],
            "json",
            "yaml",
            output_path,
            input_schema="tests/schemas/nonexistent_schema.json",
        )


# --- Edge Case Tests --- #


def test_load_empty_json(tmp_path):
    """Test loading an empty JSON file."""
    p = tmp_path / "empty.json"
    p.write_text("{}")
    assert load_config(p, "json") == {}
    p.write_text("")  # Truly empty
    with pytest.raises((json.JSONDecodeError, ValueError)):
        load_config(p, "json")


def test_load_empty_yaml(tmp_path):
    """Test loading an empty YAML file."""
    p = tmp_path / "empty.yaml"
    p.write_text("")
    assert load_config(p, "yaml") is None  # ruamel.yaml loads empty as None
    p.write_text("--- \n...")  # Empty document
    assert load_config(p, "yaml") is None


def test_load_empty_toml(tmp_path):
    """Test loading an empty TOML file."""
    p = tmp_path / "empty.toml"
    p.write_text("")
    assert load_config(p, "toml") == {}


def test_load_invalid_json(tmp_path):
    """Test loading a JSON file with invalid syntax."""
    p = tmp_path / "invalid.json"
    p.write_text("{key: value}")  # Invalid JSON syntax
    with pytest.raises(json.JSONDecodeError):
        load_config(p, "json")


def test_load_invalid_yaml(tmp_path):
    """Test loading a YAML file with invalid syntax."""
    p = tmp_path / "invalid.yaml"
    p.write_text("key: value: another:")  # Invalid YAML
    with pytest.raises(YAMLError):
        load_config(p, "yaml")


def test_load_invalid_toml(tmp_path):
    """Test loading a TOML file with invalid syntax."""
    p = tmp_path / "invalid.toml"
    p.write_text("key = value = invalid")  # Invalid TOML
    with pytest.raises(TOMLKitError):
        load_config(p, "toml")


def test_load_invalid_xml(tmp_path):
    """Test loading an XML file with invalid syntax."""
    p = tmp_path / "invalid.xml"
    p.write_text("<root><unclosed></root>")
    with pytest.raises(ExpatError):
        load_config(p, "xml")


# --- More Conversion Tests --- #


def test_ini_to_yaml(temp_files):
    """Test converting INI to YAML."""
    output_path = temp_files["out"].with_suffix(".yaml")
    convert(temp_files["ini_in"], "ini", "yaml", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "yaml")
    # configparser reads all values as strings
    assert loaded_data == INI_SAMPLE_DATA


def test_xml_to_toml(temp_files):
    """Test converting XML to TOML."""
    output_path = temp_files["out"].with_suffix(".toml")
    input_xml_path = temp_files["xml_in"]
    convert(input_xml_path, "xml", "toml", output_path)
    assert output_path.exists()
    loaded_data = load_config(output_path, "toml")
    # Convert tomlkit data to standard dict for comparison
    assert _convert_tomlkit_to_standard(loaded_data) == XML_SAMPLE_DATA_FROM_STR


def test_toml_comment_preservation(temp_files):
    """Test that TOML comments are preserved during TOML load/save cycle."""
    input_path = temp_files["toml_comments_in"]
    output_path = temp_files["out"].parent / "output_comments_preserved.toml"

    # Load the data using tomlkit (which load_config now does)
    loaded_data = load_config(input_path, "toml")

    # Save the data back using tomlkit (which save_config now does)
    save_config(loaded_data, output_path, "toml")

    # Read the output file content
    with open(output_path, "r", encoding="utf-8") as f:
        output_content = f.read()

    # Read the input file content again for comparison
    with open(input_path, "r", encoding="utf-8") as f:
        input_content = f.read()

    # Assert that the output content is identical to the input content
    # after stripping leading/trailing whitespace.
    assert output_content.strip() == input_content.strip()
