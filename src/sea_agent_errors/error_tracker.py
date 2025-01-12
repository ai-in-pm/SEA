from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import csv
import json
import logging
import os
import traceback

logger = logging.getLogger(__name__)

@dataclass
class AgentError:
    """Represents an error encountered by the SEA Agent."""
    timestamp: str
    error_type: str
    error_message: str
    context: Dict[str, Any]
    stack_trace: str
    component: str
    severity: str

class ErrorTracker:
    """Tracks and logs errors encountered by the SEA Agent."""
    
    def __init__(self, log_dir: str = None):
        """Initialize the error tracker."""
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        self.log_dir = log_dir
        self.errors = []
        self._ensure_log_directory()
    
    def _ensure_log_directory(self) -> None:
        """Ensure the log directory exists."""
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Create CSV file if it doesn't exist
        csv_path = os.path.join(self.log_dir, 'error_log.csv')
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp',
                    'Error Type',
                    'Error Message',
                    'Component',
                    'Severity',
                    'Context',
                    'Stack Trace'
                ])
    
    def log_error(self, error_type: str, error_message: str, context: Dict[str, Any],
                 stack_trace: Optional[str] = None, component: str = "unknown",
                 severity: str = "ERROR") -> None:
        """Log an error with detailed information."""
        timestamp = datetime.now().isoformat()
        
        error_data = {
            'timestamp': timestamp,
            'error_type': error_type,
            'error_message': error_message,
            'context': context,
            'stack_trace': stack_trace or traceback.format_exc(),
            'component': component,
            'severity': severity
        }
        
        self.errors.append(error_data)
        
        # Save to JSON file
        self._save_to_json()
        
        # Append to CSV file
        self._append_to_csv(error_data)
        
        # Generate error report if needed
        if severity in ['CRITICAL', 'ERROR']:
            self._generate_error_report(error_data)
    
    def _save_to_json(self) -> None:
        """Save all errors to a JSON file."""
        json_path = os.path.join(self.log_dir, 'error_log.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.errors, f, indent=2)
    
    def _append_to_csv(self, error_data: Dict[str, Any]) -> None:
        """Append an error to the CSV log file."""
        csv_path = os.path.join(self.log_dir, 'error_log.csv')
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                error_data['timestamp'],
                error_data['error_type'],
                error_data['error_message'],
                error_data['component'],
                error_data['severity'],
                json.dumps(error_data['context']),
                error_data['stack_trace']
            ])
    
    def _generate_error_report(self, error_data: Dict[str, Any]) -> None:
        """Generate a detailed error report in markdown format."""
        report_dir = os.path.join(self.log_dir, 'reports')
        os.makedirs(report_dir, exist_ok=True)
        
        timestamp = datetime.fromisoformat(error_data['timestamp'])
        filename = f"error_report_{timestamp.strftime('%Y%m%d_%H%M%S')}.md"
        report_path = os.path.join(report_dir, filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# SEA Agent Error Report\n\n")
            f.write(f"## Error Details\n")
            f.write(f"- **Timestamp:** {error_data['timestamp']}\n")
            f.write(f"- **Type:** {error_data['error_type']}\n")
            f.write(f"- **Component:** {error_data['component']}\n")
            f.write(f"- **Severity:** {error_data['severity']}\n\n")
            
            f.write(f"## Error Message\n")
            f.write(f"```\n{error_data['error_message']}\n```\n\n")
            
            f.write(f"## Context\n")
            f.write(f"```json\n{json.dumps(error_data['context'], indent=2)}\n```\n\n")
            
            if error_data['stack_trace']:
                f.write(f"## Stack Trace\n")
                f.write(f"```python\n{error_data['stack_trace']}\n```\n")
    
    def get_errors(self, severity: Optional[str] = None,
                  component: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get filtered errors based on severity and/or component."""
        filtered_errors = self.errors
        
        if severity:
            filtered_errors = [e for e in filtered_errors if e['severity'] == severity]
        
        if component:
            filtered_errors = [e for e in filtered_errors if e['component'] == component]
        
        return filtered_errors
    
    def get_error_summary(self) -> Dict[str, int]:
        """Get a summary of errors by type and severity."""
        summary = {
            'by_type': {},
            'by_severity': {},
            'by_component': {},
            'total': len(self.errors)
        }
        
        for error in self.errors:
            # Count by type
            error_type = error['error_type']
            summary['by_type'][error_type] = summary['by_type'].get(error_type, 0) + 1
            
            # Count by severity
            severity = error['severity']
            summary['by_severity'][severity] = summary['by_severity'].get(severity, 0) + 1
            
            # Count by component
            component = error['component']
            summary['by_component'][component] = summary['by_component'].get(component, 0) + 1
        
        return summary
    
    def clear(self) -> None:
        """Clear all stored errors."""
        self.errors = []
        self._save_to_json()
