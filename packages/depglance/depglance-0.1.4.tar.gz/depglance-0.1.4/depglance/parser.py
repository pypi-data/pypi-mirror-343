import re
import toml

def parse_requirements(file_path):
    if file_path.endswith('requirements.txt'):
        return _parse_requirements_txt(file_path)
    elif file_path.endswith('Pipfile'):
        return _parse_pipfile(file_path)
    elif file_path.endswith('poetry.lock'):
        return _parse_poetry_lock(file_path)
    else:
        raise ValueError("Unsupported file type!")

def _parse_requirements_txt(file_path):
    packages = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                package = re.split('==|>=|<=|>|<', line)[0].strip()
                packages.append(package)
    return packages

def _parse_pipfile(file_path):
    pipfile = toml.load(file_path)
    packages = list(pipfile.get('packages', {}).keys())
    packages += list(pipfile.get('dev-packages', {}).keys())
    return packages

def _parse_poetry_lock(file_path):
    packages = []
    with open(file_path, 'r') as f:
        in_package_block = False
        for line in f:
            if line.startswith('[[package]]'):
                in_package_block = True
            elif in_package_block and line.strip().startswith('name ='):
                package_name = line.split('=')[1].strip().strip('"')
                packages.append(package_name)
    return packages
