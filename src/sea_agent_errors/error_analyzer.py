from typing import Dict, Any, List
import pandas as pd
import os
from datetime import datetime, timedelta
import json

class ErrorAnalyzer:
    """Analyzes errors logged by the SEA Agent."""
    
    def __init__(self, log_dir: str = None):
        """Initialize the error analyzer."""
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        self.log_dir = log_dir
    
    def analyze_errors(self, time_window: timedelta = None) -> Dict[str, Any]:
        """
        Analyze errors from the CSV log file.
        
        Args:
            time_window: Optional time window to analyze (e.g., last 24 hours)
            
        Returns:
            Dict containing error analysis results
        """
        csv_path = os.path.join(self.log_dir, 'error_log.csv')
        if not os.path.exists(csv_path):
            return self._empty_analysis()
        
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(csv_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        
        # Filter by time window if specified
        if time_window:
            cutoff_time = datetime.now() - time_window
            df = df[df['Timestamp'] > cutoff_time]
        
        if len(df) == 0:
            return self._empty_analysis()
        
        # Perform analysis
        analysis = {
            'total_errors': len(df),
            'by_type': df['Error Type'].value_counts().to_dict(),
            'by_severity': df['Severity'].value_counts().to_dict(),
            'by_component': df['Component'].value_counts().to_dict(),
            'time_series': self._analyze_time_series(df),
            'common_patterns': self._find_patterns(df),
            'improvement_suggestions': self._generate_suggestions(df)
        }
        
        return analysis
    
    def _analyze_time_series(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze error frequency over time."""
        # Resample by hour and count errors
        hourly_counts = df.set_index('Timestamp').resample('H').size()
        
        return {
            'hourly_counts': hourly_counts.to_dict(),
            'peak_hour': hourly_counts.idxmax().strftime('%Y-%m-%d %H:00:00'),
            'peak_count': int(hourly_counts.max())
        }
    
    def _find_patterns(self, df: pd.DataFrame) -> List[str]:
        """Find common patterns in errors."""
        patterns = []
        
        # Find most common error type
        most_common_error = df['Error Type'].mode().iloc[0]
        error_count = df['Error Type'].value_counts().iloc[0]
        patterns.append(f"Most common error: {most_common_error} ({error_count} occurrences)")
        
        # Find most problematic component
        most_common_component = df['Component'].mode().iloc[0]
        component_count = df['Component'].value_counts().iloc[0]
        patterns.append(f"Most affected component: {most_common_component} ({component_count} errors)")
        
        # Find error clusters
        if len(df) >= 3:
            df['TimeDiff'] = df['Timestamp'].diff()
            clusters = df[df['TimeDiff'] < pd.Timedelta(minutes=5)]
            if len(clusters) >= 3:
                patterns.append(f"Found {len(clusters)} errors occurring in quick succession")
        
        return patterns
    
    def _generate_suggestions(self, df: pd.DataFrame) -> List[str]:
        """Generate improvement suggestions based on error patterns."""
        suggestions = []
        
        # Analyze error types
        for error_type, count in df['Error Type'].value_counts().items():
            if count >= 3:  # Threshold for considering an error type significant
                if 'import' in str(error_type).lower():
                    suggestions.append("Review and update dependency management")
                elif 'type' in str(error_type).lower():
                    suggestions.append("Improve type checking and validation")
                elif 'permission' in str(error_type).lower():
                    suggestions.append("Review file system permissions and access patterns")
                elif 'timeout' in str(error_type).lower():
                    suggestions.append("Optimize performance and add timeout handling")
        
        # Analyze components
        for component, count in df['Component'].value_counts().items():
            if count >= 3:
                suggestions.append(f"Consider refactoring the {component} component")
        
        # Analyze severity
        critical_errors = df[df['Severity'] == 'CRITICAL']
        if len(critical_errors) > 0:
            suggestions.append("Address critical errors in the following components: " +
                            ", ".join(critical_errors['Component'].unique()))
        
        return suggestions
    
    def _empty_analysis(self) -> Dict[str, Any]:
        """Return empty analysis structure."""
        return {
            'total_errors': 0,
            'by_type': {},
            'by_severity': {},
            'by_component': {},
            'time_series': {'hourly_counts': {}, 'peak_hour': None, 'peak_count': 0},
            'common_patterns': [],
            'improvement_suggestions': []
        }
    
    def generate_report(self, time_window: timedelta = None) -> str:
        """Generate a markdown report of error analysis."""
        analysis = self.analyze_errors(time_window)
        
        report = [
            "# SEA Agent Error Analysis Report",
            f"\nGenerated at: {datetime.now().isoformat()}",
            
            "\n## Summary",
            f"- Total Errors: {analysis['total_errors']}",
            
            "\n## Error Distribution",
            "\n### By Type",
            *[f"- {t}: {c}" for t, c in analysis['by_type'].items()],
            
            "\n### By Severity",
            *[f"- {s}: {c}" for s, c in analysis['by_severity'].items()],
            
            "\n### By Component",
            *[f"- {comp}: {c}" for comp, c in analysis['by_component'].items()],
            
            "\n## Time Analysis",
            f"- Peak Hour: {analysis['time_series']['peak_hour']}",
            f"- Peak Count: {analysis['time_series']['peak_count']}",
            
            "\n## Common Patterns",
            *[f"- {p}" for p in analysis['common_patterns']],
            
            "\n## Improvement Suggestions",
            *[f"- {s}" for s in analysis['improvement_suggestions']]
        ]
        
        return "\n".join(report)
