# Smart Engineering Assistant (SEA)

A powerful AI-driven engineering assistant that helps generate, analyze, and improve software projects. SEA combines advanced language models with recursive self-improvement capabilities and mid-level engineering expertise to create high-quality, production-ready code.

*Last Updated: January 11, 2025*

## Requirements

- Python 3.8+
- Click
- PyYAML
- Logging

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a configuration file:
```bash
cp config/default.yaml.example config/default.yaml
# Edit config/default.yaml with your settings
```

3. Use the CLI to create and manage projects:

```bash
# Create a new project
python main.py create --name "PROJECT_NAME" --type "web_app" --description "Project description"

# Available project types:
# - web_app: Web applications and APIs
# - cli_tool: Command-line tools and utilities
# - desktop_app: GUI applications
# - game: Game development projects
# - ai_assistant: AI and LLM applications
# - data_science: Data analysis and ML projects
# - topic_app: Domain-specific applications for any topic

# Play a game from the warehouse
python main.py play --game [snake|tictactoe|chess|checkers|poker|solitaire]

# Analyze an existing project
python main.py analyze --project-dir "./my_project"

# Generate and run tests
python main.py test --project-dir "./my_project"

# Check version
python main.py version
```

### Example Usage

```bash
# Create a full-stack web application
python main.py create \
  --name "WebApp" \
  --type "web_app" \
  --description "Create a full-stack web application with Flask backend and React frontend"

# Play a game
python main.py play --game snake

# Analyze a project
python main.py analyze --project-dir "./my_project"
```

## Features

### Core Capabilities
- **Intelligent Project Generation**: Creates complete project structures based on descriptions
- **Multi-Framework Support**: Handles various frameworks (Flask, React, Django, FastAPI, Spring)
- **Game Development**: Built-in game warehouse with popular games
- **Project Analysis**: Code quality assessment and improvement suggestions
- **Test Generation**: Automated test case generation and execution
- **Documentation**: Comprehensive documentation and work summaries
- **Development Time Comparison**: Provides detailed comparison of development time and cost savings

### Technical Skills
- **Languages**: Python, JavaScript, TypeScript, Java, C++
- **Frameworks**: Flask, React, Django, FastAPI, Spring
- **Standards**: PEP8, ESLint, Prettier
- **Security**: OWASP, SANS
- **Quality**: SOLID, Clean Code, DRY

### Project Types

The SEA system supports various project types:
- `web_app`: Web applications and APIs
- `cli_tool`: Command-line tools and utilities
- `desktop_app`: GUI applications
- `game`: Game development
- `ai_assistant`: AI and LLM applications
- `data_science`: Data analysis and ML projects
- `topic_app`: Domain-specific applications for any topic

## Development Time Comparison

Each generated project includes a `comparison.md` file that provides:
- Detailed time comparison between SEA Agent and human engineers
- Cost analysis and ROI calculations
- Quality metrics comparison
- Additional benefits of using SEA Agent

Example time savings:
- Project setup: 1.9 hours saved
- Database design: 2.8 hours saved
- API development: 7.7 hours saved
- Frontend UI: 11.7 hours saved
- Total average savings: 36.5 hours per project

## Architecture

The SEA system consists of several key components:

- **Engineering Agent**: Core component that orchestrates project generation and improvement
  - Manages project lifecycle
  - Ensures code quality and standards
  - Provides technical expertise
- **Project Generator**: Creates project structures and initial code
- **Game Warehouse**: Collection of implemented games
- **Test Generator**: Automated test case generation
- **Work Tracker**: Monitors progress and maintains logs

## Development Status

Current development status as of January 11, 2025:
- CLI interface implemented
- Project generation framework
- Game warehouse with multiple games
- Project analysis (in progress)
- Test generation (in progress)
- Documentation system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sea.git
   cd sea
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your API keys and configuration

## Usage

### Command Line Interface (Recommended)

The easiest way to use SEA is through its command-line interface:

```bash
# Basic usage
python main.py create --name "PROJECT_NAME" --type "PROJECT_TYPE" --description "YOUR_PROJECT_DESCRIPTION"

# Examples
python main.py create --name "WebApp" --type "web_app" --description "Create a full-stack web application with Flask backend and React frontend"
python main.py play --game snake
python main.py analyze --project-dir "./my_project"
```

### Python API

For more advanced usage, you can use the Python API:

```python
from sea import EngineeringAgent
from sea.utils.config import Config

# Initialize the agent
config = Config()
agent = EngineeringAgent(config)

# Generate a project
project = agent.generate_project(
    description="Create a full-stack web application with Flask backend and React frontend",
    name="WebApp"
)

# Access engineering capabilities
principles = agent.apply_engineering_principles(description)
architecture = agent.plan_architecture(description)
patterns = agent.identify_design_patterns(description)
```

### Advanced Features

#### Engineering Analysis
```python
# Analyze project requirements
requirements = agent.analyze_requirements(task)

# Plan system architecture
architecture = agent.plan_architecture(task)

# Identify design patterns
patterns = agent.identify_design_patterns(task)

# Define quality standards
standards = agent.define_quality_standards()
```

#### Self-Improvement

The SEA agent includes recursive self-improvement capabilities that:
- Analyze code quality and structure
- Identify potential improvements
- Apply enhancements while maintaining functionality
- Track code evolution and changes

```python
# The agent automatically improves code during generation
# You can also trigger improvement manually:
agent.improver.improve_code(code, context)
```

#### Work Tracking

Monitor project generation progress and improvements:
```python
# Get work summary
summary = agent.work_tracker.format_summary()

# Save work summary to file
agent.work_tracker.save_summary("work_summary.md")
```

## Project Structure

Generated projects follow a standardized structure:

```
project_name/
├── src/              # Source code
│   ├── main.py      # Entry point
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   └── utils/       # Utilities
├── tests/           # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/            # Documentation
│   ├── README.md
│   └── API.md
├── work_summary.md  # SEA's thought process
├── comparison.md    # Development time analysis
├── requirements.txt # Dependencies
└── setup.py        # Package configuration
```

SEA's own codebase structure:

```
sea/
├── src/
│   ├── agent/
│   │   ├── engineering_agent.py   # Main agent implementation
│   │   ├── project_generator.py   # Project generation logic
│   │   ├── self_improvement.py    # Self-improvement capabilities
│   │   └── work_tracker.py        # Progress tracking
│   ├── llm/
│   │   └── llm_manager.py        # Language model integration
│   └── utils/
│       └── config.py             # Configuration management
├── tests/                        # Test suite
├── docs/                         # Documentation
└── examples/                     # Example projects
```

## Acknowledgments

- Built with advanced language models
- Inspired by recursive self-improvement principles
- Uses various open-source libraries and frameworks
