"""
Command module for querying dependencies.
"""

import argparse
import json
import sys
from pathlib import Path

def query_dependencies(file_path, dependency_file, direction):
    """Query dependencies for a specific file."""
    try:
        with open(dependency_file) as f:
            data = json.load(f)
        
        # Check if the data uses the new format with graph
        if 'graph' in data and 'edges' in data['graph']:
            # Direct dependencies (what file_path depends on)
            if direction in ['out', 'both']:
                print(f"\nDependencies of {file_path}:")
                deps = [edge[1] for edge in data['graph']['edges'] if edge[0] == file_path]
                if deps:
                    for dep in deps:
                        print(f"  - {dep}")
                else:
                    print("  No dependencies found")
            
            # Reverse dependencies (what depends on file_path)
            if direction in ['in', 'both']:
                print(f"\nFiles that depend on {file_path}:")
                rev_deps = [edge[0] for edge in data['graph']['edges'] if edge[1] == file_path]
                if rev_deps:
                    for file in rev_deps:
                        print(f"  - {file}")
                else:
                    print("  No files depend on this")
        elif 'edges' in data:
            # Support for the old format
            # Direct dependencies (what file_path depends on)
            if direction in ['out', 'both']:
                print(f"\nDependencies of {file_path}:")
                if file_path in data['edges']:
                    for dep in data['edges'][file_path]:
                        print(f"  - {dep}")
                else:
                    print("  No dependencies found")
            
            # Reverse dependencies (what depends on file_path)
            if direction in ['in', 'both']:
                print(f"\nFiles that depend on {file_path}:")
                depends_on_target = []
                for file, deps in data['edges'].items():
                    if file_path in deps:
                        depends_on_target.append(file)
                
                if depends_on_target:
                    for file in depends_on_target:
                        print(f"  - {file}")
                else:
                    print("  No files depend on this")
        else:
            print(f"Error: Unsupported dependency file format")
            return 1
                
        return 0
    except FileNotFoundError:
        print(f"Error: Dependency file '{dependency_file}' not found.")
        return 1
    except KeyError as e:
        print(f"Error: Missing key in dependency file: {e}")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

def main(args=None):
    """Main entry point for the command."""
    parser = argparse.ArgumentParser(
        description="Query dependencies for a specific file"
    )
    
    parser.add_argument(
        "file_path",
        help="Path to the file to query dependencies for"
    )
    
    parser.add_argument(
        "-d", "--dependency-file",
        default="output/python_dependencies.json",
        help="Path to the dependency JSON file"
    )
    
    parser.add_argument(
        "--direction",
        choices=["in", "out", "both"],
        default="both",
        help="Direction of dependencies to show: in=reverse deps, out=direct deps, both=all"
    )
    
    if args is None:
        args = sys.argv[1:]
    
    parsed_args = parser.parse_args(args)
    
    return query_dependencies(
        parsed_args.file_path,
        parsed_args.dependency_file,
        parsed_args.direction
    )

if __name__ == "__main__":
    sys.exit(main()) 