import os
import yaml
from pathlib import Path

def process_yaml(var_path):
    """Process a YAML file to extract variable data.

    Args:
        var_path (str): Path to the YAML file.

    Returns:
        dict: A dictionary containing variable names as keys and tuples
        of values and descriptions as values.
    """
    var_dict = {}
    description = ""
    with open(var_path, 'r') as file:
        lines = file.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#'):
            description = line.lstrip('# ').strip()
        elif ':' in line:
            var_name, var_value = line.split(':', 1)
            var_value = var_value.strip()
            while (i + 1 < len(lines) and
                   not (lines[i + 1].strip().startswith('#') or ':' in lines[i + 1])):
                i += 1
                var_value += '\n' + lines[i].strip()
            var_value = yaml.safe_load(var_value) if not (var_value.startswith('{{') and var_value.endswith('}}')) else var_value
            var_dict[var_name.strip()] = (var_value, description)
            description = ""
        i += 1
    return var_dict

def generate_row(var, value_desc_tuple):
    """Generate a markdown table row from variable data.

    Args:
        var (str): The variable name.
        value_desc_tuple (tuple): A tuple containing the variable value and description.

    Returns:
        str: A formatted markdown table row.
    """
    value, description = value_desc_tuple
    if isinstance(value, bool):
        value_str = f'`{str(value)}`'  # Convert Python boolean to string
    elif isinstance(value, list):
        value_str = f'`{", ".join(value)}`'  # Convert list to comma-separated string
    else:
        value_str = f'`{str(value).replace("|", "\\|")}`'  # Escape the pipe character
    description = description.replace("|", "\\|")
    return f"| `{var}` | {value_str} | {description} |"


def process_directory(directory_path, target_dict):
    """Process a directory of YAML files and update a dictionary with extracted variable data.

    Args:
        directory_path (str): Path to the directory containing YAML files.
        target_dict (dict): Dictionary to update with extracted variable data.

    Returns:
        None
    """
    for var_file in os.listdir(directory_path):
        os_family = os.path.splitext(var_file)[0]
        var_path = os.path.join(directory_path, var_file)
        if os.path.exists(var_path):
            vars_dict = process_yaml(var_path)
            os_family_cap = os_family.capitalize()
            target_dict.setdefault(os_family_cap, {}).update(vars_dict) if os_family != 'main' else target_dict.update(vars_dict)

def generate_table(role_path):
    """Generate markdown tables of variables from a role directory.

    Args:
        role_path (str): Path to the Ansible role directory.

    Returns:
        str: Markdown tables of variables.
    """
    os_vars, general_vars = {}, {}
    vars_directory_path, defaults_directory_path = Path(role_path, 'vars'), Path(role_path, 'defaults')

    if os.path.exists(vars_directory_path):
        process_directory(vars_directory_path, os_vars)
    if os.path.exists(defaults_directory_path):
        process_directory(defaults_directory_path, general_vars)

    general_table_header = "| Variable | Default Value | Description |\n| --- | --- | --- |\n"
    general_table_rows = "\n".join([generate_row(var, value_desc_tuple) for var, value_desc_tuple in general_vars.items()])
    general_table = general_table_header + general_table_rows

    os_tables = [f"| Variable | Default Value ({os_family}) | Description |\n| --- | --- | --- |\n" +
                 "\n".join([generate_row(var, value_desc_tuple) for var, value_desc_tuple in var_dict.items()])
                 for os_family, var_dict in sorted(os_vars.items(), key=lambda item: item[0])]

    return general_table + "\n" + "\n".join(os_tables)

def main():
    """Main function to process all roles and update README files with variable tables.

    Returns:
        None
    """
    roles_path = Path("roles")
    for role_name in roles_path.iterdir():
        if role_name.is_dir():
            table = generate_table(role_name)
            readme_path = role_name / "README.md"
            if readme_path.exists():
                with open(readme_path, 'r') as file:
                    readme_content = file.read()
                markers = ("<!--- vars table -->", "<!--- end vars table -->")
                if all(marker in readme_content for marker in markers):
                    pre, _, post = readme_content.partition(markers[0])
                    post = post.partition(markers[1])[2]
                    new_readme_content = f"{pre}{markers[0]}\n{table}\n{markers[1]}{post}"
                    with open(readme_path, 'w') as file:
                        file.write(new_readme_content)
                else:
                    print(f"Marker not found in {readme_path}")
            else:
                print(f"{readme_path} does not exist")

if __name__ == "__main__":
    main()
