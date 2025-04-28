import re
import toml
import networkx as nx


def __parse_requirements_with_versions(file_path):
    packages = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                # Match package and optional version
                match = re.match(r"([^=><!~]+)([=><!~]+.+)?", line)
                if match:
                    package_name = match.group(1).strip()
                    version = match.group(2).strip('=<>!~') if match.group(2) else None
                    packages.append((package_name, version))
    return packages

def parse_requirements(file_path):
    if file_path.endswith('requirements.txt'):
        return __parse_requirements_with_versions(file_path)
    elif file_path.endswith('Pipfile'):
        return _parse_pipfile(file_path)
    elif file_path.endswith('poetry.lock'):
        return _parse_poetry_lock(file_path)
    else:
        raise ValueError("Unsupported file type!")

def _parse_requirements_txt(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                package = re.split('==|>=|<=|>|<', line)[0].strip()
                graph.add_node(package)
    return graph

def _parse_pipfile(file_path):
    graph = nx.DiGraph()
    pipfile = toml.load(file_path)
    for package in pipfile.get('packages', {}).keys():
        graph.add_node(package)
    for package in pipfile.get('dev-packages', {}).keys():
        graph.add_node(package)
    return graph

def _parse_poetry_lock(file_path):
    graph = nx.DiGraph()
    with open(file_path, 'r') as f:
        in_package_block = False
        for line in f:
            if line.startswith('[[package]]'):
                in_package_block = True
            elif in_package_block and line.strip().startswith('name ='):
                package_name = line.split('=')[1].strip().strip('"')
                graph.add_node(package_name)
    return graph
