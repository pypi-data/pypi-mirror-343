import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque

def get_package_dependencies(package_name):
    """Fetch dependencies of a package using 'pip show'."""
    try:
        result = subprocess.run(
            ["pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
        requires = []
        for line in result.stdout.splitlines():
            if line.startswith("Requires:"):
                deps = line.split(":", 1)[1].strip()
                if deps:
                    requires = [dep.strip().split(" ")[0] for dep in deps.split(",")]
                break
        return requires
    except subprocess.CalledProcessError:
        print(f"Warning: Failed to fetch dependencies for {package_name}")
        return []

def build_dependency_graph(packages):
    """Build a dependency graph for the given packages."""
    graph = defaultdict(set)
    all_packages = set(packages)
    visited = set()

    def dfs(pkg):
        if pkg in visited:
            return
        visited.add(pkg)
        deps = get_package_dependencies(pkg)
        for dep in deps:
            graph[pkg].add(dep)
            all_packages.add(dep)
            dfs(dep)

    for pkg in packages:
        dfs(pkg)

    return graph, all_packages

def topological_sort(graph, all_packages):
    """Return install layers based on dependency graph."""
    in_degree = {pkg: 0 for pkg in all_packages}
    for deps in graph.values():
        for dep in deps:
            in_degree[dep] += 1

    queue = deque([pkg for pkg in all_packages if in_degree[pkg] == 0])
    layers = []

    while queue:
        layer = list(queue)
        layers.append(layer)
        next_queue = deque()
        for pkg in layer:
            for neighbor in graph.get(pkg, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_queue.append(neighbor)
        queue = next_queue

    if sum(in_degree.values()) != 0:
        raise RuntimeError("Cycle detected in dependencies")

    return layers

def install_package(package_name):
    """Install a single package via pip."""
    print(f"Installing {package_name}...")
    result = subprocess.run(["pip", "install", package_name])
    if result.returncode != 0:
        print(f"Failed to install {package_name}")
    else:
        print(f"Installed {package_name}")

def concurrent_install(packages, max_workers=4):
    """Install packages concurrently with dependency analysis."""
    graph, all_packages = build_dependency_graph(packages)
    layers = topological_sort(graph, all_packages)

    for layer in layers:
        print(f"Installing layer: {layer}")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(install_package, pkg): pkg for pkg in layer}
            for future in as_completed(futures):
                pkg = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error installing {pkg}: {e}")

if __name__ == "__main__":
    import sys
    pkgs = sys.argv[1:]
    if not pkgs:
        print("Usage: python pip_concurrent.py package1 package2 ...")
    else:
        concurrent_install(pkgs)