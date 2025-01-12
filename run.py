import argparse
import os
import sys
import time
from datetime import datetime
from src.agent.engineering_agent import EngineeringAgent
from src.utils.config import Config

def determine_project_type(task_description: str) -> str:
    """Determine project type from task description."""
    task_lower = task_description.lower()
    
    if any(term in task_lower for term in ["web", "api", "flask", "django", "fastapi"]):
        return "web_app"
    elif any(term in task_lower for term in ["cli", "command", "terminal"]):
        return "cli_tool"
    elif any(term in task_lower for term in ["game", "pygame"]):
        return "game"
    elif any(term in task_lower for term in ["desktop", "gui", "qt", "tkinter"]):
        return "desktop_app"
    elif any(term in task_lower for term in ["ai", "assistant", "gpt", "claude"]):
        return "ai_assistant"
    elif any(term in task_lower for term in ["data", "analysis", "machine learning", "ml"]):
        return "data_science"
    else:
        return "general"

def create_project_structure(project_name: str, project_type: str) -> str:
    """Create project directory structure and return the path."""
    # Base warehouse directory
    warehouse_dir = os.path.join("src", "warehouse")
    
    # Clean project name (remove special characters and spaces)
    clean_name = "".join(c for c in project_name if c.isalnum() or c in ['-', '_'])
    
    # Get current timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create the project directory path
    project_dir = os.path.join(warehouse_dir, project_type, f"{clean_name}")
    
    # If the exact project name exists, add timestamp to make it unique
    if os.path.exists(project_dir):
        project_dir = os.path.join(warehouse_dir, project_type, f"{clean_name}_{timestamp}")
    
    # Create the directory
    os.makedirs(project_dir, exist_ok=True)
    
    # Create standard project structure
    directories = [
        os.path.join(project_dir, "src"),
        os.path.join(project_dir, "tests"),
        os.path.join(project_dir, "docs"),
        os.path.join(project_dir, "config"),
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return project_dir

def save_work_summary(project_dir: str, agent: EngineeringAgent):
    """Save the agent's work summary to the project directory."""
    summary = agent.work_tracker.format_summary()
    summary_path = os.path.join(project_dir, "work_summary.md")
    
    with open(summary_path, "w") as f:
        f.write(summary)
    
    return summary_path

def main():
    parser = argparse.ArgumentParser(description="Smart Engineering Assistant (SEA) - Project Generator")
    parser.add_argument("--task", required=True, help="Description of the project to generate")
    parser.add_argument("--name", required=True, help="Name of the project")
    args = parser.parse_args()

    try:
        print(f"Initializing Smart Engineering Assistant for project: {args.name}")
        
        # Initialize the AI agent with configuration
        config = Config()
        agent = EngineeringAgent(config)
        
        # Determine project type from task description
        project_type = determine_project_type(args.task)
        print(f"Detected project type: {project_type}")
        
        # Create project directory in appropriate warehouse
        project_dir = create_project_structure(args.name, project_type)
        print(f"Created project directory: {project_dir}")
        
        # Generate project with work tracking
        print("\nGenerating project...")
        agent.generate_project(
            description=args.task,
            project_type=project_type,
            name=args.name
        )
        
        # Save work summary
        summary_path = save_work_summary(project_dir, agent)
        
        print("\nProject generation complete!")
        print("\nProject Details:")
        print(f"- Directory: {project_dir}")
        print(f"- Work Summary: {summary_path}")
        print(f"- Type: {project_type}")
        
        print("\nTo run your project:")
        print(f"cd {project_dir}")
        print("python src/main.py")
        
        print("\nCheck work_summary.md for detailed generation process")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
