"""
Command-line interface for running complete analysis pipelines.

This module provides commands that chain together multiple analysis steps.
"""

import os
import sys
import logging
import argparse
import time
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments for pipeline commands."""
    parser = argparse.ArgumentParser(
        description="Run complete analysis pipelines on a codebase",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "path",
        type=str,
        help="Path to the codebase to analyze"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="output",
        help="Output directory for results"
    )
    
    parser.add_argument(
        "--exclude-dirs",
        type=str,
        nargs="+",
        default=["venv", ".git", "__pycache__", "node_modules", "dist"],
        help="Directories to exclude from analysis"
    )
    
    parser.add_argument(
        "--convert-deps",
        action="store_true",
        help="Generate enhanced dependency visualizations"
    )
    
    parser.add_argument(
        "--no-complexity",
        action="store_true",
        help="Skip complexity analysis"
    )
    
    return parser.parse_args(args)


def run_all_pipeline(path: str, output_dir: str, exclude_dirs: List[str], 
                     convert_deps: bool, no_complexity: bool) -> int:
    """
    Run a complete analysis pipeline on a codebase.
    
    This will:
    1. Extract dependencies
    2. Convert dependencies to visualization format (if requested)
    3. Generate architecture graph visualization
    4. Collect metrics (if complexity analysis is enabled)
    
    Args:
        path: Path to the codebase to analyze
        output_dir: Output directory for results
        exclude_dirs: Directories to exclude from analysis
        convert_deps: Whether to generate enhanced visualizations
        no_complexity: Whether to skip complexity analysis
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    start_time = time.time()
    try:
        print(f"Starting comprehensive analysis of: {path}")
        print("Running full analysis...")
        
        # Create output directory if needed
        os.makedirs(output_dir, exist_ok=True)
        
        # First, run the main analysis
        from codex_arch.analyzer import run_analysis
        analysis_results = run_analysis(
            paths=path,
            output_dir=output_dir,
            exclude_dirs=exclude_dirs,
            analyze_complexity=not no_complexity,
            analyze_dependencies=True,
            analyze_metrics=True,
        )
        
        # Step 1: Extract dependencies - explicitly call dependency command
        print("Extracting Python dependencies...")
        from codex_arch.cli import dependency_cmd
        dependency_args = [path, "--output", output_dir]
        
        # Add exclude patterns
        for exclude_dir in exclude_dirs:
            dependency_args.extend(["--exclude-patterns", f"**/{exclude_dir}/**"])
            
        dep_result = dependency_cmd.main(dependency_args)
        if dep_result != 0:
            logger.error("Dependency extraction failed")
            return dep_result
            
        deps_file = os.path.join(output_dir, "python_dependencies.json")
        
        # Step 2 & 3: Handle dependency conversion and visualization
        if convert_deps:
            # Step 2: Convert dependencies
            print("\nConverting dependencies to visualization format...")
            complete_deps_file = os.path.join(output_dir, "complete_dependencies.json")
            
            from codex_arch.cli import convert_deps_cmd
            convert_result = convert_deps_cmd.main([deps_file, complete_deps_file])
            if convert_result != 0:
                logger.error("Dependency conversion failed")
                return convert_result
            
            # Step 3a: Generate complete architecture visualization
            print("\nGenerating enhanced architecture visualization...")
            from codex_arch.cli import graph_cmd
            complete_graph_path = os.path.join(output_dir, "complete_arch_graph")
            graph_result = graph_cmd.main([complete_deps_file, complete_graph_path])
            if graph_result != 0:
                logger.error("Enhanced graph generation failed")
                return graph_result
                
        # Step 3b: Generate standard architecture visualization
        print("\nGenerating architecture graph from: {}".format(deps_file))
        from codex_arch.cli import graph_cmd
        graph_path = os.path.join(output_dir, "architecture_graph")
        
        try:
            graph_result = graph_cmd.main([deps_file, graph_path])
            if graph_result != 0:
                logger.error("Graph generation failed")
        except Exception as e:
            logger.error(f"Error generating architecture graph: {str(e)}")
        
        # Generate a file tree to help with navigation
        print("\nGenerating file tree for navigation...")
        from codex_arch.cli import file_tree_cmd
        file_tree_args = [path, "--output", os.path.join(output_dir, "file_tree.json")]
        for exclude_dir in exclude_dirs:
            file_tree_args.extend(["--exclude", exclude_dir])
        file_tree_cmd.main(file_tree_args)
        
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        
        print(f"\nAnalysis completed in {minutes} minutes and {seconds} seconds")
        print(f"Results saved to: {output_dir}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Error in pipeline execution: {str(e)}", exc_info=True)
        print(f"Error: {str(e)}")
        return 1


def main(args: Optional[List[str]] = None) -> int:
    """Run the pipeline command CLI."""
    parsed_args = parse_args(args)
    
    return run_all_pipeline(
        path=parsed_args.path,
        output_dir=parsed_args.output,
        exclude_dirs=parsed_args.exclude_dirs,
        convert_deps=parsed_args.convert_deps,
        no_complexity=parsed_args.no_complexity
    )


if __name__ == "__main__":
    sys.exit(main())