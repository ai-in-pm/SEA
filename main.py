#!/usr/bin/env python3
import os
import click
import logging
from datetime import datetime
from typing import Optional
from src.agent.engineering_agent import EngineeringAgent
from src.templates.project_templates import ProjectType, Framework, get_template
from src.utils.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def initialize_agent() -> EngineeringAgent:
    """Initialize the SEA agent with configuration."""
    config_path = os.getenv('SEA_CONFIG', 'config/default.yaml')
    return EngineeringAgent(config_path)

def validate_project_name(name: str) -> str:
    """Validate and sanitize project name."""
    # Remove special characters and spaces
    sanitized = ''.join(c if c.isalnum() else '_' for c in name)
    if not sanitized:
        raise click.BadParameter("Project name must contain alphanumeric characters")
    return sanitized

def get_timestamp() -> str:
    """Get formatted timestamp for project directory."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

@click.group()
def cli():
    """Smart Engineering Assistant (SEA) - Your AI-powered development companion."""
    pass

@cli.command()
@click.option('--name', prompt='Project name', help='Name of the project to create')
@click.option('--type', 'project_type', type=click.Choice([t.value for t in ProjectType]),
              prompt='Project type', help='Type of project to create')
@click.option('--framework', type=click.Choice([f.value for f in Framework]),
              help='Framework to use (optional)')
@click.option('--topic', help='Topic for topic-based apps (required for topic_app type)')
@click.option('--description', prompt='Project description',
              help='Detailed description of the project')
@click.option('--output-dir', default='projects',
              help='Directory where the project should be created')
def create(name: str, project_type: str, framework: Optional[str],
           topic: Optional[str], description: str, output_dir: str):
    """Create a new software project."""
    try:
        # Initialize agent
        agent = initialize_agent()
        logger.info(f"Initialized SEA agent for project creation: {name}")

        # Validate and prepare project directory
        project_name = validate_project_name(name)
        timestamp = get_timestamp()
        project_dir = os.path.join(
            output_dir,
            f"{project_name}_{timestamp}"
        )
        os.makedirs(output_dir, exist_ok=True)

        # Convert string values to enums
        project_type_enum = ProjectType(project_type)
        framework_enum = Framework(framework) if framework else None

        # Validate topic for topic-based apps
        if project_type_enum == ProjectType.TOPIC_APP and not topic:
            raise click.BadParameter("Topic must be provided for topic-based apps")

        # Generate project
        logger.info(f"Generating project in {project_dir}")
        agent.generate_project(
            description=description,
            project_type=project_type_enum,
            name=project_name,
            framework=framework_enum,
            topic=topic
        )

        click.echo(f"\n✨ Project created successfully in {project_dir}")
        click.echo("\nNext steps:")
        click.echo(f"1. cd {project_dir}")
        click.echo("2. pip install -r requirements.txt")
        click.echo("3. python main.py")

    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        raise click.Abort()

@cli.command()
@click.option('--game', type=click.Choice([
    'snake', 'tictactoe', 'chess', 'checkers', 'poker', 'solitaire'
]), prompt='Select game', help='Game to run')
def play(game: str):
    """Run a game from the game warehouse."""
    try:
        game_module = f"src.warehouse.games.{game}.{game}_game"
        os.system(f"python -m {game_module}")
    except Exception as e:
        logger.error(f"Error running game: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        raise click.Abort()

@cli.command()
@click.option('--project-dir', type=click.Path(exists=True),
              prompt='Project directory', help='Directory of the project to analyze')
def analyze(project_dir: str):
    """Analyze an existing project and provide insights."""
    try:
        agent = initialize_agent()
        logger.info(f"Analyzing project in {project_dir}")
        
        # TODO: Implement project analysis
        click.echo("Project analysis feature coming soon!")
        
    except Exception as e:
        logger.error(f"Error analyzing project: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        raise click.Abort()

@cli.command()
@click.option('--project-dir', type=click.Path(exists=True),
              prompt='Project directory', help='Directory of the project to test')
def test(project_dir: str):
    """Generate and run tests for a project."""
    try:
        agent = initialize_agent()
        logger.info(f"Generating tests for project in {project_dir}")
        
        # TODO: Implement test generation and running
        click.echo("Test generation feature coming soon!")
        
    except Exception as e:
        logger.error(f"Error generating tests: {str(e)}")
        click.echo(f"❌ Error: {str(e)}")
        raise click.Abort()

@cli.command()
def version():
    """Show SEA version information."""
    click.echo("SEA (Smart Engineering Assistant) v1.0.0")
    click.echo("Created by the Codeium team")

def main():
    """Main entry point for the SEA CLI."""
    try:
        cli()
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        click.echo(f"❌ Unexpected error: {str(e)}")
        raise click.Abort()

if __name__ == '__main__':
    main()
