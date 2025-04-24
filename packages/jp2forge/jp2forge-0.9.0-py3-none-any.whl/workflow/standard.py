"""
Standard sequential workflow for JPEG2000 processing.

This module provides a sequential implementation of the JPEG2000 workflow.
"""

import os
import gc
import time
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

from core.types import (
    WorkflowStatus, 
    DocumentType, 
    CompressionMode, 
    ProcessingResult,
    WorkflowConfig,
    BnFCompressionRatio
)
from core.metadata.base_handler import MetadataHandler
from core.metadata.bnf_handler import BnFMetadataHandler
from utils.image import validate_image, get_output_path, find_image_files
from utils.profiling import profile, profile_block, mark_event, save_report
from workflow.base import BaseWorkflow

logger = logging.getLogger(__name__)


class StandardWorkflow(BaseWorkflow):
    """Sequential implementation of the JPEG2000 workflow."""
    
    def __init__(self, config: WorkflowConfig):
        """Initialize the workflow with configuration.
        
        Args:
            config: Workflow configuration
        """
        super().__init__(config)
        
        # Initialize performance profiling for the workflow
        self.enable_profiling = config.enable_profiling if hasattr(config, 'enable_profiling') else False
        if self.enable_profiling:
            from utils.profiling import get_profiler
            get_profiler(output_dir=config.report_dir)
            logger.info("Performance profiling enabled for StandardWorkflow")
    
    @profile("process_file_implementation")
    def _process_file_implementation(
        self,
        input_file: str,
        doc_type: DocumentType,
        lossless_fallback: bool,
        bnf_compliant: bool,
        compression_ratio_tolerance: float,
        include_bnf_markers: bool,
        metadata: Dict[str, Any]
    ) -> ProcessingResult:
        """Implementation of file processing logic.
        
        Args:
            input_file: Path to input file
            doc_type: Document type for compression
            lossless_fallback: Whether to fall back to lossless compression
            bnf_compliant: Whether to use BnF compliant settings
            compression_ratio_tolerance: Tolerance for compression ratio
            include_bnf_markers: Whether to include BnF robustness markers
            metadata: Additional metadata to include in output file
            
        Returns:
            ProcessingResult: Result of processing
        """
        try:
            # Step 1: Convert to JPEG2000
            with profile_block("conversion_to_jp2"):
                logger.info("Step 1: Converting to JPEG2000")
                output_file = get_output_path(input_file, self.config.output_dir, ".jp2")
                
                processing_start = time.time()
                
                # Process according to compression mode
                compression_mode = self.config.compression_mode
                success = self.compressor.convert_to_jp2(
                    input_file,
                    output_file,
                    doc_type,
                    compression_mode,
                    lossless_fallback,
                    bnf_compliant,
                    compression_ratio_tolerance,
                    include_bnf_markers
                )
                
                processing_time = time.time() - processing_start
                logger.info(f"Conversion completed in {processing_time:.2f} seconds")
                
                if not success:
                    mark_event("conversion_failed", {"input_file": input_file})
                    return ProcessingResult(
                        status=WorkflowStatus.FAILURE,
                        input_file=input_file,
                        error="Conversion failed"
                    )
            
            # Step 2: Analyze pixel loss (only in supervised mode)
            report_file = None
            analysis_results = None
            
            if compression_mode == CompressionMode.SUPERVISED:
                with profile_block("pixel_loss_analysis"):
                    logger.info("Step 2: Analyzing pixel loss")
                    analysis_start = time.time()
                    
                    analysis_result = self.analyzer.analyze_pixel_loss(
                        input_file,
                        output_file,
                        save_report=False  # Changed from True to False to avoid generating individual analysis files
                    )
                    
                    analysis_time = time.time() - analysis_start
                    logger.info(f"Analysis completed in {analysis_time:.2f} seconds")
                    
                    # Check if quality checks failed but we're still returning success
                    if not analysis_result.quality_passed:
                        logger.warning(f"Quality checks failed for {input_file}")
                        mark_event("quality_check_failed", {
                            "input_file": input_file,
                            "psnr": analysis_result.psnr,
                            "ssim": analysis_result.ssim,
                            "mse": analysis_result.mse
                        })
                        # We still return success but with metrics for user review
                        status = WorkflowStatus.WARNING
                        metrics = {
                            "psnr": analysis_result.psnr,
                            "ssim": analysis_result.ssim,
                            "mse": analysis_result.mse,
                            "quality_passed": analysis_result.quality_passed
                        }
                    else:
                        status = WorkflowStatus.SUCCESS
                        metrics = {
                            "psnr": analysis_result.psnr,
                            "ssim": analysis_result.ssim,
                            "mse": analysis_result.mse,
                            "quality_passed": analysis_result.quality_passed
                        }
            else:
                # For non-supervised modes, we don't do analysis
                status = WorkflowStatus.SUCCESS
                metrics = None
            
            # Step 3: Add metadata
            with profile_block("add_metadata"):
                logger.info("Step 3: Adding metadata")
                # Pass compression parameters to metadata handler
                compression_mode_str = self.config.compression_mode.value
                
                # For BnF mode, use BnF compliant metadata
                if bnf_compliant or compression_mode == CompressionMode.BNF_COMPLIANT:
                    # Use the BnF metadata handler
                    # Initialize with base handler to ensure proper setup
                    if not isinstance(self.metadata_handler, BnFMetadataHandler):
                        base_handler = MetadataHandler()
                        bnf_handler = BnFMetadataHandler(base_handler=base_handler, debug=True)
                    else:
                        bnf_handler = self.metadata_handler
                        
                    # Generate document ID if not provided in metadata
                    metadata_dict = {}
                    if metadata:
                        metadata_dict.update(metadata)
                    
                    # If not provided, generate default BnF isPartOf ID (NUM_format)
                    if 'dcterms:isPartOf' not in metadata_dict:
                        base_name = os.path.splitext(os.path.basename(input_file))[0]
                        metadata_dict['dcterms:isPartOf'] = f"NUM_{base_name}"
                    
                    # Default BnF provenance if not specified
                    if 'dcterms:provenance' not in metadata_dict:
                        metadata_dict['dcterms:provenance'] = "Bibliothèque nationale de France"
                        
                    try:
                        self.metadata_handler.write_metadata(
                            output_file,
                            metadata_dict,
                            compression_mode_str,
                            self.config.num_resolutions,
                            self.config.progression_order,
                            True  # bnf_compliant=True
                        )
                    except Exception as e:
                        mark_event("metadata_error", {"error": str(e), "type": "bnf_metadata"})
                        logger.error(f"Error writing BnF metadata: {str(e)}")
                        return ProcessingResult(
                            status=WorkflowStatus.WARNING,  # Continue with warning
                            input_file=input_file,
                            output_file=output_file,
                            error=f"Converted successfully but metadata failed: {str(e)}"
                        )
                else:
                    # Standard metadata
                    try:
                        self.metadata_handler.write_metadata(
                            output_file,
                            metadata,
                            compression_mode_str,
                            self.config.num_resolutions,
                            self.config.progression_order
                        )
                    except Exception as e:
                        mark_event("metadata_error", {"error": str(e), "type": "standard_metadata"})
                        logger.error(f"Error writing metadata: {str(e)}")
                        return ProcessingResult(
                            status=WorkflowStatus.WARNING,  # Continue with warning
                            input_file=input_file,
                            output_file=output_file,
                            error=f"Converted successfully but metadata failed: {str(e)}"
                        )
            
            # Force garbage collection
            with profile_block("cleanup"):
                gc.collect()
            
            # Calculate file sizes
            file_sizes = None
            try:
                original_size = os.path.getsize(input_file)
                converted_size = os.path.getsize(output_file)
                compression_ratio = original_size / converted_size if converted_size > 0 else 0
                
                file_sizes = {
                    "original_size": original_size,
                    "original_size_human": self._format_file_size(original_size),
                    "converted_size": converted_size,
                    "converted_size_human": self._format_file_size(converted_size),
                    "compression_ratio": f"{compression_ratio:.2f}:1"
                }
                
                # Log compression stats for profiling
                if self.enable_profiling:
                    mark_event("compression_stats", {
                        "input_file": os.path.basename(input_file),
                        "original_size_mb": original_size / (1024 * 1024),
                        "converted_size_mb": converted_size / (1024 * 1024),
                        "compression_ratio": compression_ratio
                    })
            except Exception as e:
                logger.warning(f"Error calculating file sizes: {str(e)}")
            
            logger.info(f"Successfully processed {input_file}")
            self.processed_files_count += 1
            
            return ProcessingResult(
                status=status,
                input_file=input_file,
                output_file=output_file,
                report_file=report_file,
                metrics=metrics,
                file_sizes=file_sizes
            )
            
        except Exception as e:
            logger.error(f"Error processing {input_file}: {str(e)}")
            mark_event("processing_error", {"input_file": input_file, "error": str(e)})
            return ProcessingResult(
                status=WorkflowStatus.FAILURE,
                input_file=input_file,
                error=str(e)
            )
    
    @profile("process_directory")
    def process_directory(
        self,
        input_dir: str,
        doc_type: Optional[DocumentType] = None,
        metadata: Optional[Dict[str, Any]] = None,
        recursive: Optional[bool] = None,
        lossless_fallback: Optional[bool] = None,
        bnf_compliant: Optional[bool] = None,
        compression_ratio_tolerance: Optional[float] = None,
        include_bnf_markers: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Process all files in a directory sequentially.
        
        Args:
            input_dir: Directory containing input files
            doc_type: Document type for compression
            metadata: Metadata to add to files
            recursive: Whether to process subdirectories
            lossless_fallback: Whether to fall back to lossless compression
            bnf_compliant: Whether to use BnF compliant settings
            compression_ratio_tolerance: Tolerance for compression ratio
            include_bnf_markers: Whether to include BnF robustness markers
            
        Returns:
            Dictionary with processing results
        """
        # Validate output directory before processing (implementing BaseWorkflow validation)
        if not self.config.output_dir or not os.path.exists(self.config.output_dir):
            logger.error("Output directory not specified or does not exist")
            return {
                'status': WorkflowStatus.FAILURE,
                'error': 'Output directory not specified or does not exist',
                'processed_files': [],
                'success_count': 0,
                'warning_count': 0,
                'error_count': 1,
                'corrupted_count': 0
            }
            
        # Use configuration defaults if not specified
        doc_type = doc_type or self.config.document_type
        recursive = self.config.recursive if recursive is None else recursive
        lossless_fallback = (
            self.config.lossless_fallback 
            if lossless_fallback is None 
            else lossless_fallback
        )
        bnf_compliant = (
            self.config.bnf_compliant
            if bnf_compliant is None
            else bnf_compliant
        )
        compression_ratio_tolerance = (
            self.config.compression_ratio_tolerance
            if compression_ratio_tolerance is None
            else compression_ratio_tolerance
        )
        include_bnf_markers = (
            self.config.include_bnf_markers
            if include_bnf_markers is None
            else include_bnf_markers
        )
        
        # Initialize default metadata if not provided
        if metadata is None:
            metadata = {}
        
        if not os.path.exists(input_dir):
            logger.error(f"Input directory not found: {input_dir}")
            return {
                'status': WorkflowStatus.FAILURE,
                'error': 'Input directory not found'
            }
        
        # Initialize results and tracking
        results = {
            'status': WorkflowStatus.SUCCESS,  # Initial status
            'processed_files': [],
            'success_count': 0,
            'warning_count': 0,
            'error_count': 0,
            'corrupted_count': 0,
            'processing_time': 0
        }
        
        # Initialize tracking variables
        self.processed_files_count = 0
        self.start_time = time.time()
        
        # Find all image files to process
        with profile_block("find_image_files"):
            image_files = find_image_files(input_dir, recursive)
            
        self.total_files = len(image_files)
        logger.info(f"Found {self.total_files} image files to process")
        
        if self.enable_profiling:
            mark_event("batch_processing_start", {
                "total_files": self.total_files,
                "input_dir": input_dir,
                "recursive": recursive
            })
        
        # Process files sequentially
        for i, input_file in enumerate(image_files):
            result = self.process_file(
                input_file=input_file,
                doc_type=doc_type,
                lossless_fallback=lossless_fallback,
                bnf_compliant=bnf_compliant,
                compression_ratio_tolerance=compression_ratio_tolerance,
                include_bnf_markers=include_bnf_markers,
                metadata=metadata
            )
            
            # Convert ProcessingResult to dictionary for report
            file_result = {
                'input_file': result.input_file,
                'status': result.status.name,
                'output_file': result.output_file,
                'report_file': result.report_file,
                'error': result.error
            }
            
            # Add file sizes if available
            if result.file_sizes:
                file_result['file_sizes'] = result.file_sizes
            
            results['processed_files'].append(file_result)
            
            if result.status == WorkflowStatus.SUCCESS:
                results['success_count'] += 1
            elif result.status == WorkflowStatus.WARNING:
                results['warning_count'] += 1
                if results['status'] == WorkflowStatus.SUCCESS:
                    results['status'] = WorkflowStatus.WARNING
            elif result.status == WorkflowStatus.FAILURE:
                results['error_count'] += 1
                results['status'] = WorkflowStatus.FAILURE
            elif result.status == WorkflowStatus.SKIPPED:
                results['corrupted_count'] += 1
                
            # Update progress
            progress = (len(results['processed_files']) / self.total_files) * 100
            logger.info(f"Progress: {progress:.1f}% ({len(results['processed_files'])}/{self.total_files})")
            
            # If there are errors, we still continue processing other files
            
            # Log batch progress every 5% or 10 files, whichever comes first
            should_log_progress = (i % 10 == 9) or (i > 0 and int(progress / 5) > int(((i - 1) / self.total_files * 100) / 5))
            if should_log_progress and self.enable_profiling:
                current_time = time.time()
                elapsed_time = current_time - self.start_time
                files_per_second = (i + 1) / elapsed_time if elapsed_time > 0 else 0
                estimated_remaining = (self.total_files - (i + 1)) / files_per_second if files_per_second > 0 else 0
                
                mark_event("batch_progress", {
                    "processed": i + 1,
                    "total": self.total_files,
                    "percent_complete": progress,
                    "files_per_second": files_per_second,
                    "estimated_remaining_seconds": estimated_remaining
                })
        
        # Calculate total processing time
        results['processing_time'] = time.time() - self.start_time
        
        # Generate summary report
        with profile_block("generate_summary_report"):
            summary_report = self._generate_summary_report(results)
            summary_file = os.path.join(self.config.report_dir, 'summary_report.md')
            with open(summary_file, 'w') as f:
                f.write(summary_report)
            
            results['summary_report'] = summary_file
        
        # Log results
        logger.info(
            f"Processed {len(results['processed_files'])} files in {results['processing_time']:.2f} seconds: "
            f"{results['success_count']} success, "
            f"{results['warning_count']} warning, "
            f"{results['error_count']} error"
        )
        logger.info(f"Directory processing complete. Status: {results['status'].name}")
        logger.info(f"Summary report: {summary_file}")
        logger.info(f"Processing rate: {len(results['processed_files']) / results['processing_time']:.2f} files/second")
        
        if self.enable_profiling:
            mark_event("batch_processing_complete", {
                "total_files": self.total_files,
                "success_count": results['success_count'],
                "warning_count": results['warning_count'],
                "error_count": results['error_count'],
                "corrupted_count": results['corrupted_count'],
                "total_duration": results['processing_time'],
                "files_per_second": len(results['processed_files']) / results['processing_time'] 
                    if results['processing_time'] > 0 else 0
            })
            
            # Save performance profile report
            profile_report_path = save_report(f"profile_report_standard_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            logger.info(f"Saved performance profile report to {profile_report_path}")
        
        return results
