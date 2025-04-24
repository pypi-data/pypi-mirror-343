"""
Benchmark suite for JP2Forge performance testing.

This module provides tools for benchmarking various configurations
and optimizations in the JP2Forge workflow.
"""

import os
import time
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple, Union
import concurrent.futures
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from core.types import WorkflowConfig, DocumentType, CompressionMode
from utils.profiling import get_profiler, mark_event, save_report, reset as reset_profiling
from workflow.standard import StandardWorkflow
from workflow.parallel import ParallelWorkflow
from utils.imaging.streaming_processor import StreamingImageProcessor

logger = logging.getLogger(__name__)

class BenchmarkSuite:
    """
    Benchmark suite for testing JP2Forge performance.
    
    This class provides functionality for running systematic
    benchmarks to identify optimal configurations.
    """
    
    def __init__(
        self, 
        output_dir: str,
        report_dir: str,
        results_dir: Optional[str] = None,
        enable_profiling: bool = True
    ):
        """
        Initialize the benchmark suite.
        
        Args:
            output_dir: Directory for output files
            report_dir: Directory for reports
            results_dir: Directory for benchmark results
            enable_profiling: Whether to enable detailed profiling
        """
        self.output_dir = output_dir
        self.report_dir = report_dir
        self.enable_profiling = enable_profiling
        
        # Create results directory if not specified
        if results_dir is None:
            results_dir = os.path.join(report_dir, "benchmarks")
        self.results_dir = results_dir
        
        # Ensure directories exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(results_dir, exist_ok=True)
        
        # Initialize profiling if enabled
        if enable_profiling:
            get_profiler(output_dir=report_dir, enabled=True)
        
        logger.info(
            f"Benchmark suite initialized: "
            f"output_dir={output_dir}, "
            f"report_dir={report_dir}, "
            f"results_dir={results_dir}, "
            f"enable_profiling={enable_profiling}"
        )
    
    def run_memory_pool_benchmark(
        self,
        input_files: List[str],
        memory_pool_sizes: List[int] = [50, 100, 200, 400],
        max_blocks: List[int] = [5, 10, 20],
        repetitions: int = 3
    ) -> Dict[str, Any]:
        """
        Benchmark different memory pool configurations.
        
        Args:
            input_files: List of input files to process
            memory_pool_sizes: List of memory pool sizes in MB to test
            max_blocks: List of maximum block counts to test
            repetitions: Number of repetitions for each configuration
            
        Returns:
            Dictionary with benchmark results
        """
        logger.info(f"Starting memory pool benchmark with {len(input_files)} files")
        mark_event("memory_pool_benchmark_start", {
            "input_files_count": len(input_files),
            "memory_pool_sizes": memory_pool_sizes,
            "max_blocks": max_blocks,
            "repetitions": repetitions
        })
        
        results = []
        
        for input_file in input_files:
            file_size = os.path.getsize(input_file) / (1024 * 1024)  # Size in MB
            file_name = os.path.basename(input_file)
            logger.info(f"Benchmarking file: {file_name} ({file_size:.2f} MB)")
            
            # Get standard processing time (no memory pool)
            std_times = []
            for _ in range(repetitions):
                processor = StreamingImageProcessor(
                    use_memory_pool=False,
                    temp_dir=self.output_dir
                )
                output_file = os.path.join(self.output_dir, f"std_{file_name}_out.jpg")
                
                start_time = time.time()
                processor.process_in_chunks(  # Changed from process_whole_image to process_in_chunks
                    input_file,
                    output_file,
                    lambda img: img  # Identity function
                )
                end_time = time.time()
                std_times.append(end_time - start_time)
            
            avg_std_time = sum(std_times) / len(std_times)
            
            # Test different memory pool configurations
            for pool_size in memory_pool_sizes:
                for blocks in max_blocks:
                    config_times = []
                    memory_usages = []
                    
                    for rep in range(repetitions):
                        # Reset profiling between runs
                        if self.enable_profiling:
                            reset_profiling()
                        
                        processor = StreamingImageProcessor(
                            use_memory_pool=True,
                            memory_pool_size_mb=pool_size,
                            temp_dir=self.output_dir
                        )
                        processor.initialize_memory_pool(pool_size, blocks)
                        
                        output_file = os.path.join(
                            self.output_dir,
                            f"pool_{pool_size}mb_{blocks}blocks_{file_name}_out.jpg"
                        )
                        
                        start_time = time.time()
                        try:
                            processor.process_in_chunks(  # Changed from process_whole_image to process_in_chunks
                                input_file,
                                output_file,
                                lambda img: img  # Identity function
                            )
                            status = "success"
                        except Exception as e:
                            logger.error(f"Error processing with memory pool: {e}")
                            status = "error"
                        
                        end_time = time.time()
                        duration = end_time - start_time
                        config_times.append(duration)
                        
                        # Clean up
                        processor.cleanup()
                        if os.path.exists(output_file):
                            try:
                                os.remove(output_file)
                            except:
                                pass
                    
                    # Calculate average and improvement
                    avg_time = sum(config_times) / len(config_times)
                    improvement = (avg_std_time - avg_time) / avg_std_time * 100
                    
                    result = {
                        "file_name": file_name,
                        "file_size_mb": file_size,
                        "memory_pool_size_mb": pool_size,
                        "max_blocks": blocks,
                        "avg_time": avg_time,
                        "std_time": avg_std_time,
                        "improvement_percent": improvement,
                        "all_times": config_times
                    }
                    
                    results.append(result)
                    logger.info(
                        f"Memory pool {pool_size}MB x {blocks} blocks: "
                        f"avg_time={avg_time:.4f}s, "
                        f"improvement={improvement:.2f}%"
                    )
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(
            self.results_dir,
            f"memory_pool_benchmark_{timestamp}.json"
        )
        
        with open(result_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "input_files": [os.path.basename(f) for f in input_files],
                "memory_pool_sizes": memory_pool_sizes,
                "max_blocks": max_blocks,
                "repetitions": repetitions,
                "results": results
            }, f, indent=2)
        
        # Generate summary visualizations if pandas is available
        try:
            df = pd.DataFrame(results)
            
            # Plot improvement by memory pool size and blocks
            plt.figure(figsize=(12, 8))
            
            for file_name in df['file_name'].unique():
                file_df = df[df['file_name'] == file_name]
                
                for blocks in file_df['max_blocks'].unique():
                    blocks_df = file_df[file_df['max_blocks'] == blocks]
                    plt.plot(
                        blocks_df['memory_pool_size_mb'],
                        blocks_df['improvement_percent'],
                        marker='o',
                        label=f"{file_name} ({blocks} blocks)"
                    )
            
            plt.xlabel('Memory Pool Size (MB)')
            plt.ylabel('Performance Improvement (%)')
            plt.title('Memory Pool Performance Improvement')
            plt.legend()
            plt.grid(True)
            
            # Save plot
            plot_file = os.path.join(
                self.results_dir,
                f"memory_pool_benchmark_{timestamp}.png"
            )
            plt.savefig(plot_file)
            
        except Exception as e:
            logger.warning(f"Error generating visualization: {e}")
        
        logger.info(f"Memory pool benchmark results saved to {result_file}")
        mark_event("memory_pool_benchmark_complete")
        
        return {
            "result_file": result_file,
            "results": results
        }
    
    def run_workflow_benchmark(
        self,
        input_dir: str,
        configurations: List[Dict[str, Any]],
        repetitions: int = 2
    ) -> Dict[str, Any]:
        """
        Benchmark different workflow configurations.
        
        Args:
            input_dir: Directory containing input files
            configurations: List of configuration dictionaries
            repetitions: Number of repetitions for each configuration
            
        Returns:
            Dictionary with benchmark results
        """
        # Import datetime in the method scope to ensure it's available
        from datetime import datetime
        
        logger.info(f"Starting workflow benchmark with {len(configurations)} configurations")
        mark_event("workflow_benchmark_start", {
            "input_dir": input_dir,
            "config_count": len(configurations),
            "repetitions": repetitions
        })
        
        # Get list of files
        input_files = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                    input_files.append(os.path.join(root, file))
        
        if not input_files:
            logger.error(f"No input files found in {input_dir}")
            return {"error": "No input files found"}
        
        results = []
        
        # Run benchmarks for each configuration
        for config_index, config_dict in enumerate(configurations):
            logger.info(f"Testing configuration {config_index + 1}/{len(configurations)}")
            
            for rep in range(repetitions):
                # Reset profiling between runs
                if self.enable_profiling:
                    reset_profiling()
                
                # Create a unique output directory for this run
                run_output_dir = os.path.join(
                    self.output_dir,
                    f"config_{config_index + 1}_rep_{rep + 1}"
                )
                os.makedirs(run_output_dir, exist_ok=True)
                
                # Create workflow configuration
                workflow_config = WorkflowConfig(
                    output_dir=run_output_dir,
                    report_dir=self.report_dir,
                    **config_dict
                )
                
                # Determine workflow type based on processing_mode
                if isinstance(workflow_config.processing_mode, str):
                    # Handle case where processing_mode is passed as a string
                    processing_mode = workflow_config.processing_mode.upper()
                    is_parallel = processing_mode == "PARALLEL"
                else:
                    # Handle case where processing_mode is passed as an enum
                    is_parallel = workflow_config.processing_mode.name == "PARALLEL"
                
                if is_parallel:
                    workflow = ParallelWorkflow(workflow_config)
                else:
                    workflow = StandardWorkflow(workflow_config)
                
                # Process files
                start_time = time.time()
                try:
                    result = workflow.process_directory(input_dir)
                    status = "success"
                except Exception as e:
                    logger.error(f"Error in workflow benchmark: {e}")
                    status = "error"
                    result = {"error": str(e)}
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Save results
                config_result = {
                    "config_index": config_index,
                    "repetition": rep,
                    "configuration": config_dict,
                    "duration": duration,
                    "status": status,
                    "file_count": len(input_files),
                    "files_per_second": len(input_files) / duration if duration > 0 else 0
                }
                
                if status == "success":
                    config_result.update({
                        "success_count": result.get("success_count", 0),
                        "warning_count": result.get("warning_count", 0),
                        "error_count": result.get("error_count", 0)
                    })
                
                results.append(config_result)
                logger.info(
                    f"Configuration {config_index + 1}, rep {rep + 1}: "
                    f"duration={duration:.2f}s, "
                    f"files_per_second={config_result['files_per_second']:.2f}"
                )
        
        # Save benchmark results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(
            self.results_dir,
            f"workflow_benchmark_{timestamp}.json"
        )
        
        with open(result_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "input_dir": input_dir,
                "file_count": len(input_files),
                "configurations": configurations,
                "repetitions": repetitions,
                "results": results
            }, f, indent=2)
        
        # Generate summary visualization
        try:
            df = pd.DataFrame(results)
            
            # Group by configuration and calculate average performance
            avg_performance = df.groupby('config_index').agg({
                'duration': 'mean',
                'files_per_second': 'mean'
            }).reset_index()
            
            # Create configuration labels
            config_labels = []
            for i, config in enumerate(configurations):
                mode = config.get('mode', 'standard')
                workers = config.get('max_workers', 1)
                use_memory_pool = config.get('use_memory_pool', False)
                label = f"{mode}-w{workers}"
                if use_memory_pool:
                    label += "-mem"
                config_labels.append(label)
            
            # Plot performance comparison
            plt.figure(figsize=(12, 8))
            plt.bar(range(len(avg_performance)), avg_performance['files_per_second'])
            plt.xlabel('Configuration')
            plt.ylabel('Files Processed Per Second')
            plt.title('Workflow Configuration Performance Comparison')
            plt.xticks(range(len(avg_performance)), config_labels)
            plt.grid(True, axis='y')
            
            # Save plot
            plot_file = os.path.join(
                self.results_dir,
                f"workflow_benchmark_{timestamp}.png"
            )
            plt.savefig(plot_file)
            
        except Exception as e:
            logger.warning(f"Error generating visualization: {e}")
        
        logger.info(f"Workflow benchmark results saved to {result_file}")
        mark_event("workflow_benchmark_complete")
        
        return {
            "result_file": result_file,
            "results": results
        }

    def run_image_size_benchmark(
        self,
        image_dirs: Dict[str, str],
        configurations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Benchmark performance across different image sizes.
        
        Args:
            image_dirs: Dictionary mapping size categories to directories
            configurations: List of configuration dictionaries to test
            
        Returns:
            Dictionary with benchmark results
        """
        logger.info(
            f"Starting image size benchmark with {len(image_dirs)} size categories "
            f"and {len(configurations)} configurations"
        )
        mark_event("image_size_benchmark_start", {
            "size_categories": list(image_dirs.keys()),
            "config_count": len(configurations)
        })
        
        results = []
        
        # Process each size category
        for size_category, directory in image_dirs.items():
            if not os.path.exists(directory):
                logger.warning(f"Directory not found: {directory}")
                continue
                
            logger.info(f"Benchmarking size category: {size_category}")
            
            # Count image files in directory
            image_files = []
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                        image_files.append(os.path.join(root, file))
            
            if not image_files:
                logger.warning(f"No image files found in {directory}")
                continue
            
            # Test each configuration
            for config_index, config_dict in enumerate(configurations):
                # Create a unique output directory for this run
                run_output_dir = os.path.join(
                    self.output_dir,
                    f"{size_category}_config_{config_index + 1}"
                )
                os.makedirs(run_output_dir, exist_ok=True)
                
                # Create workflow configuration
                workflow_config = WorkflowConfig(
                    output_dir=run_output_dir,
                    report_dir=self.report_dir,
                    **config_dict
                )
                
                # Determine workflow type
                if config_dict.get('mode') == 'parallel':
                    workflow = ParallelWorkflow(workflow_config)
                else:
                    workflow = StandardWorkflow(workflow_config)
                
                # Reset profiling
                if self.enable_profiling:
                    reset_profiling()
                
                # Process files
                start_time = time.time()
                try:
                    result = workflow.process_directory(directory)
                    status = "success"
                except Exception as e:
                    logger.error(f"Error in image size benchmark: {e}")
                    status = "error"
                    result = {"error": str(e)}
                
                end_time = time.time()
                duration = end_time - start_time
                
                # Calculate file sizes
                total_input_size = sum(os.path.getsize(f) for f in image_files) / (1024 * 1024)  # MB
                
                # Save result
                size_result = {
                    "size_category": size_category,
                    "config_index": config_index,
                    "configuration": config_dict,
                    "file_count": len(image_files),
                    "total_input_size_mb": total_input_size,
                    "duration": duration,
                    "files_per_second": len(image_files) / duration if duration > 0 else 0,
                    "mb_per_second": total_input_size / duration if duration > 0 else 0,
                    "status": status
                }
                
                if status == "success":
                    size_result.update({
                        "success_count": result.get("success_count", 0),
                        "warning_count": result.get("warning_count", 0),
                        "error_count": result.get("error_count", 0)
                    })
                
                results.append(size_result)
                logger.info(
                    f"{size_category}, Config {config_index + 1}: "
                    f"duration={duration:.2f}s, "
                    f"files/s={size_result['files_per_second']:.2f}, "
                    f"MB/s={size_result['mb_per_second']:.2f}"
                )
        
        # Save benchmark results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(
            self.results_dir,
            f"image_size_benchmark_{timestamp}.json"
        )
        
        with open(result_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "image_dirs": image_dirs,
                "configurations": configurations,
                "results": results
            }, f, indent=2)
        
        # Generate visualization
        try:
            df = pd.DataFrame(results)
            
            # Create configuration labels
            config_labels = []
            for i, config in enumerate(configurations):
                mode = config.get('mode', 'standard')
                workers = config.get('max_workers', 1)
                use_memory_pool = config.get('use_memory_pool', False)
                label = f"{mode}-w{workers}"
                if use_memory_pool:
                    label += "-mem"
                config_labels.append(label)
            
            # Plot performance by size category
            plt.figure(figsize=(12, 8))
            
            # Get unique size categories and configs
            size_categories = sorted(df['size_category'].unique())
            config_indices = df['config_index'].unique()
            
            # Prepare data for grouped bar chart
            x = np.arange(len(size_categories))
            width = 0.8 / len(config_indices)
            
            for i, config_idx in enumerate(config_indices):
                config_df = df[df['config_index'] == config_idx]
                # Sort by size category
                config_df = config_df.set_index('size_category').reindex(size_categories).reset_index()
                
                plt.bar(
                    x + i * width - width * (len(config_indices) - 1) / 2,
                    config_df['mb_per_second'],
                    width,
                    label=config_labels[int(config_idx)]
                )
            
            plt.xlabel('Image Size Category')
            plt.ylabel('Processing Speed (MB/s)')
            plt.title('Processing Performance by Image Size')
            plt.xticks(x, size_categories)
            plt.legend()
            plt.grid(True, axis='y')
            
            # Save plot
            plot_file = os.path.join(
                self.results_dir,
                f"image_size_benchmark_{timestamp}.png"
            )
            plt.savefig(plot_file)
            
        except Exception as e:
            logger.warning(f"Error generating visualization: {e}")
        
        logger.info(f"Image size benchmark results saved to {result_file}")
        mark_event("image_size_benchmark_complete")
        
        return {
            "result_file": result_file,
            "results": results
        }

def main():
    """Command-line entry point for running benchmarks."""
    # Import datetime in the function scope to ensure it's available in all contexts
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description="JP2Forge benchmark suite")
    parser.add_argument(
        "--output-dir", 
        default="./benchmark_output",
        help="Directory for benchmark output files"
    )
    parser.add_argument(
        "--report-dir", 
        default="./benchmark_reports",
        help="Directory for benchmark reports"
    )
    parser.add_argument(
        "--results-dir", 
        default="./benchmark_results",
        help="Directory for benchmark results"
    )
    parser.add_argument(
        "--input-dir", 
        default="./images",
        help="Directory containing input images"
    )
    parser.add_argument(
        "--enable-profiling", 
        action="store_true",
        help="Enable detailed performance profiling"
    )
    parser.add_argument(
        "--benchmark-type",
        choices=["memory-pool", "workflow", "image-size", "all"],
        default="all",
        help="Type of benchmark to run"
    )
    parser.add_argument(
        "--small-images-dir",
        help="Directory containing small test images"
    )
    parser.add_argument(
        "--medium-images-dir",
        help="Directory containing medium test images"
    )
    parser.add_argument(
        "--large-images-dir",
        help="Directory containing large test images"
    )
    
    args = parser.parse_args()
    
    # Initialize benchmark suite
    benchmark = BenchmarkSuite(
        output_dir=args.output_dir,
        report_dir=args.report_dir,
        results_dir=args.results_dir,
        enable_profiling=args.enable_profiling
    )
    
    # Run requested benchmarks
    if args.benchmark_type in ["memory-pool", "all"]:
        # Find input files
        input_files = []
        for root, _, files in os.walk(args.input_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                    input_files.append(os.path.join(root, file))
        
        if input_files:
            # Limit to a few files for memory pool benchmarks
            test_files = input_files[:5]
            benchmark.run_memory_pool_benchmark(test_files)
        else:
            logger.error(f"No input files found in {args.input_dir}")
    
    if args.benchmark_type in ["workflow", "all"]:
        # Define workflow configurations to test
        configs = [
            # Standard workflow
            {"processing_mode": "SEQUENTIAL", "use_memory_pool": False, "enable_profiling": True},
            # Standard workflow with memory pool
            {"processing_mode": "SEQUENTIAL", "use_memory_pool": True, "enable_profiling": True},
            # Parallel workflow with 2 workers
            {"processing_mode": "PARALLEL", "max_workers": 2, "use_memory_pool": False, "enable_profiling": True},
            # Parallel workflow with 2 workers and memory pool
            {"processing_mode": "PARALLEL", "max_workers": 2, "use_memory_pool": True, "enable_profiling": True},
            # Parallel workflow with 4 workers
            {"processing_mode": "PARALLEL", "max_workers": 4, "use_memory_pool": False, "enable_profiling": True},
            # Parallel workflow with 4 workers and memory pool
            {"processing_mode": "PARALLEL", "max_workers": 4, "use_memory_pool": True, "enable_profiling": True}
        ]
        
        benchmark.run_workflow_benchmark(args.input_dir, configs)
    
    if args.benchmark_type in ["image-size", "all"]:
        # Define image directories by size
        image_dirs = {}
        
        if args.small_images_dir:
            image_dirs["small"] = args.small_images_dir
            
        if args.medium_images_dir:
            image_dirs["medium"] = args.medium_images_dir
            
        if args.large_images_dir:
            image_dirs["large"] = args.large_images_dir
            
        if not image_dirs:
            logger.error("No image directories specified for image-size benchmark")
        else:
            # Define configurations to test
            configs = [
                # Standard workflow with memory pool
                {"processing_mode": "SEQUENTIAL", "use_memory_pool": True, "enable_profiling": True},
                # Parallel workflow with 4 workers and memory pool
                {"processing_mode": "PARALLEL", "max_workers": 4, "use_memory_pool": True, "enable_profiling": True}
            ]
            
            benchmark.run_image_size_benchmark(image_dirs, configs)

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    main()