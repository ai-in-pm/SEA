"""
WorkTracker module for SEA that provides "Show Your Work" functionality.
This allows the agent to document its thought process and steps while solving problems.
"""

from typing import List, Dict, Any
from datetime import datetime

class WorkTracker:
    """Tracks and logs the work done by the agent."""
    
    def __init__(self):
        """Initialize the work tracker."""
        self.current_task = None
        self.task_metadata = None
        self.thoughts = []
        self.steps = []
        self.decisions = []
        self.errors = []
        self.start_time = None
        self.end_time = None
    
    def start_task(self, task_name: str, metadata: Dict[str, Any] = None) -> None:
        """Start tracking a new task."""
        self.current_task = task_name
        self.task_metadata = metadata or {}
        self.thoughts = []
        self.steps = []
        self.decisions = []
        self.errors = []
        self.start_time = datetime.now()
    
    def end_task(self, summary: str) -> None:
        """End the current task."""
        self.end_time = datetime.now()
        self.task_metadata["summary"] = summary
    
    def log_thought(self, thought: str) -> None:
        """Log a thought or analysis."""
        self.thoughts.append({
            "timestamp": datetime.now(),
            "thought": thought
        })
    
    def log_step(self, title: str, description: str) -> None:
        """Log a step in the process."""
        self.steps.append({
            "timestamp": datetime.now(),
            "title": title,
            "description": description
        })
    
    def log_decision(self, decision: str, reason: str) -> None:
        """Log a decision and its reasoning."""
        self.decisions.append({
            "timestamp": datetime.now(),
            "decision": decision,
            "reason": reason
        })
    
    def log_error(self, error: str) -> None:
        """Log an error."""
        self.errors.append({
            "timestamp": datetime.now(),
            "error": error
        })
    
    def format_summary(self, format_type: str = "markdown") -> str:
        """Format the work summary in the specified format."""
        if format_type == "markdown":
            summary = f"# Work Summary: {self.current_task}\n\n"
            
            # Task Information
            summary += "## Task Details\n"
            for key, value in self.task_metadata.items():
                summary += f"- **{key}**: {value}\n"
            summary += f"- **Started**: {self.start_time}\n"
            if self.end_time:
                summary += f"- **Completed**: {self.end_time}\n"
            summary += "\n"
            
            # Thoughts
            if self.thoughts:
                summary += "## Thought Process\n"
                for thought in self.thoughts:
                    summary += f"- {thought['timestamp']}: {thought['thought']}\n"
                summary += "\n"
            
            # Steps
            if self.steps:
                summary += "## Steps Taken\n"
                for step in self.steps:
                    summary += f"### {step['title']}\n"
                    summary += f"{step['description']}\n"
                    summary += f"*Timestamp: {step['timestamp']}*\n\n"
            
            # Decisions
            if self.decisions:
                summary += "## Key Decisions\n"
                for decision in self.decisions:
                    summary += f"### {decision['decision']}\n"
                    summary += f"**Reason**: {decision['reason']}\n"
                    summary += f"*Timestamp: {decision['timestamp']}*\n\n"
            
            # Errors
            if self.errors:
                summary += "## Errors Encountered\n"
                for error in self.errors:
                    summary += f"- {error['timestamp']}: {error['error']}\n"
                summary += "\n"
            
            return summary
        else:
            raise ValueError(f"Unsupported format type: {format_type}")
    
    def save_summary(self, file_path: str) -> None:
        """Save work summary to a markdown file."""
        if not self.current_task:
            raise ValueError("No task is currently being tracked")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            # Write header
            f.write(f"# Work Summary: {self.current_task}\n\n")
            
            # Write metadata
            f.write("## Task Details\n")
            for key, value in self.task_metadata.items():
                f.write(f"- **{key}**: {value}\n")
            f.write(f"- **Started**: {self.start_time}\n")
            if self.end_time:
                f.write(f"- **Completed**: {self.end_time}\n")
            f.write("\n")
            
            # Write thoughts
            if self.thoughts:
                f.write("## Thought Process\n")
                for thought in self.thoughts:
                    f.write(f"- {thought['timestamp']}: {thought['thought']}\n")
                f.write("\n")
            
            # Write steps
            if self.steps:
                f.write("## Steps Taken\n")
                for step in self.steps:
                    f.write(f"### {step['title']}\n")
                    f.write(f"{step['description']}\n")
                    f.write(f"*Timestamp: {step['timestamp']}*\n\n")
            
            # Write decisions
            if self.decisions:
                f.write("## Key Decisions\n")
                for decision in self.decisions:
                    f.write(f"### {decision['decision']}\n")
                    f.write(f"**Reason**: {decision['reason']}\n")
                    f.write(f"*Timestamp: {decision['timestamp']}*\n\n")
            
            # Write errors
            if self.errors:
                f.write("## Errors Encountered\n")
                for error in self.errors:
                    f.write(f"- {error['timestamp']}: {error['error']}\n")
                f.write("\n")
