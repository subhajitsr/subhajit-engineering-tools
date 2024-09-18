import re

def increment_version(version: str, part: str) -> str:
    major, minor, patch = map(int, version.split('.'))
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    else:
        raise ValueError("Invalid part specified. Must be 'major', 'minor', or 'patch'.")
    return f"{major}.{minor}.{patch}"

def update_version_in_file(file_path: str, new_version: str):
    with open(file_path, 'r') as file:
        content = file.read()

    # Update version in file
    new_content = re.sub(r"version='\d+\.\d+\.\d+'", f"version='{new_version}'", content)

    with open(file_path, 'w') as file:
        file.write(new_content)

if __name__ == "__main__":
    import sys

    version_file = 'version.py'
    version_part = 'minor'

    # Read the current version
    with open(version_file, 'r') as file:
        content = file.read()
    match = re.search(r"version='(\d+\.\d+\.\d+)'", content)
    if match:
        current_version = match.group(1)
        new_version = increment_version(current_version, version_part)
        update_version_in_file(version_file, new_version)
        print(f"Version updated to: {new_version}")
    else:
        print(f"Version not found in {version_file}")
        sys.exit(1)
