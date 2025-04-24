## Codex-Arch

A tool for analyzing and visualizing code architecture.

### Installation

```bash
# Install from source
git clone https://github.com/egouilliard/codex-arch.git
cd codex-arch
pip install -e .

# Or directly from PyPI
pip install codex-arch
```

### Quick Start

```bash
# Run a full analysis
codex-arch run-all path/to/your/code -o output --convert-deps
```

### Available Commands

- `analyze`: Run a complete analysis pipeline
- `bundle`: Package analysis artifacts
- `changes`: Detect changes between Git commits
- `convert-deps`: Convert dependency format for visualization
- `dependencies`: Extract dependency relationships
- `filetree`: Generate a directory structure representation
- `graph`: Generate architecture graphs
- `hooks`: Manage Git hooks integration
- `index`: Index a repository for faster searching
- `query`: Search for files, symbols, or dependencies
- `query-deps`: Query dependency information for specific files
- `report`: Generate a report about code architecture
- `run-all`: Run all analysis steps in sequence
- `summarize`: Summarize changes between Git commits
- `api`: Launch a REST API server

For detailed documentation on all commands, see [CLI Usage Guide](docs/cli_usage.md) or run:

```bash
codex-arch --help
codex-arch <command> --help
```

### Requirements

- Python 3.7+
- GraphViz (for visualization)

### Command Examples

#### Dependency Analysis

```bash
# Extract dependencies
codex-arch dependencies my_project -o output

# Generate visualization
codex-arch graph output/python_dependencies.json output/architecture_graph
```

#### Enhanced Visualization

```bash
codex-arch dependencies my_project -o output
codex-arch convert-deps output/python_dependencies.json output/complete_dependencies.json
codex-arch graph output/complete_dependencies.json output/complete_arch_graph
```

#### File Structure Analysis

```bash
codex-arch filetree my_project -o structure.json
```

#### Complete Analysis

```bash
codex-arch run-all my_project -o analysis_results --exclude-dirs venv,node_modules,.git
```