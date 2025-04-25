"""JSON reporter for panoptipy."""

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

if TYPE_CHECKING:
    from ..checks import CheckResult
    from ..rating import CodebaseRating

from rich import print_json

from .base_reporter import BaseReporter


class JSONReporter(BaseReporter):
    """Reporter that outputs check results in JSON format."""

    def __init__(self, show_details: bool = False, output_path: Optional[Path] = None):
        """Initialize the JSON reporter.

        Args:
            show_details: Whether to include detailed information in output
            output_path: Optional path to write JSON output to (stdout if None)
        """
        self.show_details = show_details
        self.output_path = output_path

    def report(
        self,
        results: Union[List["CheckResult"], Dict[Path, List["CheckResult"]]],
        rating: Optional["CodebaseRating"] = None,
        repo_path: Optional[Path] = None,
    ) -> None:
        """Generate a JSON report for check results.

        Args:
            results: Either a list of check results or a dictionary mapping paths to results
            rating: Overall rating for the codebase(s)
            repo_path: Path to the repository (only used for single repo reports)
        """
        if isinstance(results, dict):
            # Multiple repositories report
            report_data = {
                "repositories": {
                    str(path): {
                        "rating": self._get_rating_value(rating),
                        "summary": self._generate_summary(repo_results),
                        "results": self._serialize_results(repo_results),
                    }
                    for path, repo_results in results.items()
                }
            }
        else:
            # Single repository report
            report_data = {
                "repository": str(repo_path) if repo_path else None,
                "rating": self._get_rating_value(rating),
                "summary": self._generate_summary(results),
                "results": self._serialize_results(results),
            }

        json_output = json.dumps(report_data, indent=2)
        if self.output_path:
            # Write to file if output path is provided
            with open(self.output_path, "w") as f:
                f.write(json_output)
        else:
            # Default to stdout
            print_json(json_output)

    def _get_rating_value(self, rating: Optional["CodebaseRating"]) -> Optional[str]:
        """Safely get rating value, handling None case."""
        return rating.value if rating else None

    def _generate_summary(self, results: List["CheckResult"]) -> Dict[str, Any]:
        """Generate summary statistics.

        Args:
            results: List of check results

        Returns:
            Summary dictionary
        """
        # Import here to avoid circular imports
        from ..config import Config
        from ..rating import RatingCalculator

        # Create calculator with default config if needed
        calculator = RatingCalculator(Config.load())
        stats = calculator.calculate_summary_stats(results)

        return {
            "total_checks": stats["total_checks"],
            "status_counts": stats["status_counts"],
            "pass_rate": round(stats["pass_percentage"], 1),
        }

    def _serialize_results(self, results: List["CheckResult"]) -> List[Dict[str, Any]]:
        """Convert check results to JSON-serializable format."""
        return [
            {
                "check_id": result.check_id,
                "status": result.status.value,
                "message": result.message,
                "details": result.details
                if self.show_details and result.details
                else None,
            }
            for result in results
        ]


def create_reporter(
    show_details: bool = False, output_path: Optional[Path] = None
) -> JSONReporter:
    """Create a JSON reporter with the specified options.

    Args:
        show_details: Whether to include detailed information in output
        output_path: Optional path to write JSON output to (stdout if None)

    Returns:
        Configured JSON reporter
    """
    return JSONReporter(show_details=show_details, output_path=output_path)
