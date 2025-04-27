# django_spellbook/management/commands/spellbook_md_p/reporter.py
from typing import List, Tuple, Optional, Any
from io import StringIO
from django.core.management.base import OutputWrapper
from django.core.management.color import color_style

class MarkdownReporter:
    """
    Reporter class for Django Spellbook markdown processing.
    
    This class handles all reporting and output functionality related to the spellbook_md command,
    providing consistent formatting and organization of command outputs.
    """
    
    def __init__(
        self, 
        stdout: Any, 
        style=None, 
        report_level: str = 'detailed', 
        report_format: str = 'text', 
        report_output: Optional[str] = None
    ):
        """
        Initialize the MarkdownReporter.
        
        Args:
            stdout: An output stream object (OutputWrapper from Django or another IO-like object)
            style: Django's style object from BaseCommand.style (if None, a default style will be created)
            report_level: Level of detail in the report ('minimal', 'detailed', or 'debug')
            report_format: Format of the report ('text', 'json', or 'none')
            report_output: File path to save the report (if None, print to stdout)
        """
        self.stdout = stdout
        self.style = style or color_style()
        self.report_level = report_level
        self.report_format = report_format
        self.report_output = report_output
        
        # If report_output is specified, prepare the output file
        self.output_file = None
        if self.report_output and self.report_format != 'none':
            try:
                self.output_file = open(self.report_output, 'w', encoding='utf-8')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error opening output file: {str(e)}"))
                self.report_output = None  # Fallback to stdout
        
    def generate_summary_report(self, pair_results: List[Tuple[str, str, str, bool, int]]):
        """
        Generate and display a summary report of the markdown processing results.
        
        Args:
            pair_results: List of tuples containing processing results for each source-destination pair.
        """
        if self.report_format == 'none':
            return
            
        success_count = sum(1 for _, _, _, success, _ in pair_results if success)
        total_processed = sum(count for _, _, _, success, count in pair_results if success)
        failed_pairs = [(str(src), dst, prefix) for src, dst, prefix, success, _ in pair_results if not success]
        
        if self.report_format == 'json':
            self._generate_json_report(pair_results, success_count, total_processed, failed_pairs)
        else:  # Default to text format
            self._generate_text_report(pair_results, success_count, total_processed, failed_pairs)

    def _generate_text_report(self, pair_results, success_count, total_processed, failed_pairs):
        """Generate a text report."""
        # First, decide where to output
        output = self.output_file if self.output_file else self.stdout
        
        output.write("\nProcessing Summary:\n")
        
        if success_count == len(pair_results):
            message = (
                f"All {len(pair_results)} source-destination pairs processed successfully. "
                f"Total files processed: {total_processed}."
            )
            output.write(self.style.SUCCESS(message) if hasattr(output, 'write') else message)
        else:
            message = (
                f"{success_count} of {len(pair_results)} pairs processed successfully. "
                f"Total files processed: {total_processed}. "
            )
            if failed_pairs:
                message += f"Failed pairs: {', '.join(f'{src} → {dst} (prefix: {prefix})' for src, dst, prefix in failed_pairs)}"
            
            output.write(self.style.WARNING(message) if hasattr(output, 'write') else message)

    def _generate_json_report(self, pair_results, success_count, total_processed, failed_pairs):
        """Generate a JSON report."""
        import json
        
        # Prepare the JSON data
        report_data = {
            "summary": {
                "total_pairs": len(pair_results),
                "successful_pairs": success_count,
                "total_processed_files": total_processed
            },
            "pairs": [
                {
                    "source": str(src),
                    "destination": dst,
                    "url_prefix": prefix,
                    "success": success,
                    "processed_files": count
                }
                for src, dst, prefix, success, count in pair_results
            ]
        }
        
        if failed_pairs:
            report_data["failed_pairs"] = [
                {"source": src, "destination": dst, "url_prefix": prefix}
                for src, dst, prefix in failed_pairs
            ]
        
        # Convert to JSON string
        json_str = json.dumps(report_data, indent=2)
        
        # Output to file or stdout
        output = self.output_file if self.output_file else self.stdout
        output.write(json_str)

    def __del__(self):
        """Clean up resources when the reporter is destroyed."""
        if hasattr(self, 'output_file') and self.output_file:
            self.output_file.close()

        
    def _should_output(self, level: str) -> bool:
        """Determine if a message should be output based on the report level."""
        if self.report_format == 'none':
            return False
        
        levels = {'minimal': 0, 'detailed': 1, 'debug': 2}
        return levels.get(level, 1) <= levels.get(self.report_level, 1)

    def error(self, message: str):
        """Always display error messages regardless of report level."""
        if self.report_format == 'none':
            return
        self.stdout.write(self.style.ERROR(message))
        
    def warning(self, message: str, level: str = 'detailed'):
        """Display a warning message if the report level allows."""
        if not self._should_output(level):
            return
        self.stdout.write(self.style.WARNING(message))
        
    def success(self, message: str, level: str = 'detailed'):
        """Display a success message if the report level allows."""
        if not self._should_output(level):
            return
        self.stdout.write(self.style.SUCCESS(message))
        
    def write(self, message: str, level: str = 'detailed'):
        """Display a plain message if the report level allows."""
        if not self._should_output(level):
            return
        self.stdout.write(message)