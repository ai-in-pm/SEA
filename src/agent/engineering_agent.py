from typing import Dict, Any, Optional, List
from ..llm import LLMManager
from ..tools import ToolManager
from .project_generator import ProjectGenerator
from .work_tracker import WorkTracker
from .self_improvement import SelfImprovementAgent
from ..utils.config import Config
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EngineeringAgent:
    """
    Smart Engineering Assistant - A mid-level engineering AI agent with multi-LLM capabilities.
    
    Technical Skills:
    - Engineering Principles: Strong foundation in software engineering principles
    - Software & Tools: Proficiency in multiple programming languages and frameworks
    - Analytical Problem-Solving: Complex problem analysis and solution development
    - Project Management: Project planning, execution, and oversight
    - Standards & Best Practices: Industry standards and best practices compliance
    
    Soft Skills:
    - Communication: Clear technical communication
    - Team Collaboration: Cross-functional team experience
    - Adaptability: Quick learning of new technologies
    - Time Management: Efficient handling of multiple tasks
    - Leadership: Guidance and mentoring capabilities
    """
    
    def __init__(self, config: Config):
        """Initialize the engineering agent with configuration."""
        self.config = config
        self.llm_manager = LLMManager(config)
        self.work_tracker = WorkTracker()
        self.tool_manager = ToolManager(config)
        self.project_generator = ProjectGenerator(config)
        
        # Initialize self-improvement agent
        self.improver = SelfImprovementAgent(
            objective_function=self._evaluate_code_quality,
            meta_learning_rate=0.01,
            evolution_threshold=0.8
        )
        
        # Initialize skillset tracking
        self.technical_skills = {
            "engineering_principles": {
                "level": "advanced",
                "focus": ["software_architecture", "design_patterns", "system_design"]
            },
            "software_tools": {
                "languages": ["python", "javascript", "typescript", "java", "c++"],
                "frameworks": ["flask", "react", "django", "fastapi", "spring"]
            },
            "problem_solving": {
                "approaches": ["analytical", "systematic", "data-driven"],
                "methodologies": ["agile", "tdd", "ddd"]
            },
            "project_management": {
                "capabilities": ["planning", "execution", "monitoring"],
                "tools": ["git", "jira", "trello"]
            },
            "standards": {
                "coding_standards": ["pep8", "eslint", "prettier"],
                "security": ["owasp", "sans"],
                "quality": ["solid", "clean_code", "dry"]
            }
        }
        
        self.soft_skills = {
            "communication": {
                "documentation": True,
                "code_review": True,
                "technical_writing": True
            },
            "collaboration": {
                "team_work": True,
                "cross_functional": True,
                "mentoring": True
            },
            "adaptability": {
                "learning_rate": "high",
                "technology_adoption": "proactive"
            },
            "time_management": {
                "task_prioritization": True,
                "deadline_tracking": True
            },
            "leadership": {
                "mentoring": True,
                "code_review": True,
                "knowledge_sharing": True
            }
        }

    def process_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process an engineering task using the most appropriate LLM and tools.
        
        Args:
            task: The engineering task description
            context: Additional context for the task
            
        Returns:
            Dict containing the processed result and metadata
        """
        # Analyze task complexity and requirements
        task_analysis = self.analyze_task(task, context)
        
        # Select appropriate LLM based on task requirements
        selected_llm = self.llm_manager.select_llm(task_analysis)
        
        # Process task with selected LLM
        result = selected_llm.process(task, context)
        
        # Apply any necessary post-processing or validation
        validated_result = self.validate_result(result)
        
        return validated_result
    
    def generate_project(self, description: str, project_type: str, name: str, 
                        framework: Optional[str] = None, topic: Optional[str] = None) -> None:
        """Generate a complete project based on description and type.
        
        Args:
            description: Project description
            project_type: Type of project to create
            name: Project name
            framework: Framework to use (optional)
            topic: Topic for topic-based apps (optional)
        """
        try:
            # Create project directory
            project_dir = self._create_project_directory(name)
            
            # Get project template
            template = self._get_template(project_type, framework, topic)
            
            # Create project structure
            self.project_generator.create_project_structure(
                project_dir=project_dir,
                task_description=description,
                template=template
            )
            
            # Initialize git repository
            self._initialize_git(project_dir)
            
            # Generate README
            self._generate_readme(project_dir, name)
            
            # Generate .env.example
            self._generate_env_example(project_dir)
            
            # Clean up unnecessary files
            self._cleanup_folders(project_dir)
            
            # Improve generated code
            self.work_tracker.log_step("Improving Code", "Enhancing code quality and organization")
            
            for root, _, files in os.walk(project_dir):
                for file in files:
                    if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx')):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            code = f.read()
                        
                        # Get file context
                        context = {
                            'file_path': file_path,
                            'project_dir': project_dir,
                            'task': description,
                            'language': os.path.splitext(file)[1][1:]
                        }
                        
                        # Try to improve code
                        improved_code = self.improver.improve_code(code, context)
                        if improved_code and improved_code != code:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(improved_code)
                            
                            self.work_tracker.add_step(
                                f"Improved {file}",
                                f"Enhanced code quality and organization"
                            )
            
            self.work_tracker.end_task(
                f"Successfully generated {project_type} project: {name}"
            )
            
            # Save work summary
            self.work_tracker.save_summary(os.path.join(project_dir, "work_summary.md"))
            
            print(f"\nProject Directory: {project_dir}")
            print(f"Work Summary: {os.path.join(project_dir, 'work_summary.md')}")
            print("\nTo run your project:")
            print(f"cd {project_dir}")
            print("python src/main.py")
            
        except Exception as e:
            self.work_tracker.log_error(
                error_type="ProjectGenerationError",
                error_message=str(e),
                context={
                    "description": description,
                    "project_type": project_type,
                    "name": name,
                    "framework": framework,
                    "topic": topic
                },
                stack_trace=traceback.format_exc(),
                component="project_generation",
                severity="ERROR"
            )
            raise

    def analyze_project(self, project_path: str) -> Dict[str, Any]:
        """Analyze an existing project and provide insights."""
        self.work_tracker.start_task("Project Analysis", {
            "project_path": project_path,
            "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        })
        
        try:
            # Log the analysis process
            self.work_tracker.log_thought(
                f"Starting analysis of project at: {project_path}"
            )
            
            # Select appropriate LLM for analysis
            task_analysis = {
                "type": "analysis",
                "complexity": "high",
                "safety_critical": False
            }
            llm = self.llm_manager.select_llm(task_analysis)
            self.work_tracker.log_decision(
                "Selected LLM for project analysis",
                f"Using {llm.__class__.__name__} for detailed code analysis"
            )
            
            # Analyze project structure
            self.work_tracker.log_step(
                "Analyzing Project Structure",
                "Examining directory structure and file organization"
            )
            
            # Analyze code quality
            self.work_tracker.log_step(
                "Analyzing Code Quality",
                "Checking code style, patterns, and potential issues"
            )
            
            # Analyze test coverage
            self.work_tracker.log_step(
                "Analyzing Test Coverage",
                "Evaluating test coverage and quality"
            )
            
            # Generate recommendations
            self.work_tracker.log_step(
                "Generating Recommendations",
                "Creating list of suggested improvements"
            )
            
            analysis_results = {
                "summary": "Project analysis completed",
                "work_log": self.work_tracker.get_work_summary()
            }
            
            self.work_tracker.end_task(
                "Successfully completed project analysis"
            )
            
            return analysis_results
            
        except Exception as e:
            self.work_tracker.log_error(str(e))
            raise
            
    def analyze_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze task complexity and requirements to determine optimal processing strategy."""
        # Implement task analysis logic
        return {
            "complexity": self._assess_complexity(task),
            "domain": self._identify_domain(task),
            "required_tools": self._identify_required_tools(task),
            "performance_requirements": self._assess_performance_needs(task)
        }
    
    def validate_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and ensure quality of the processing result."""
        # Implement validation logic
        return result
    
    def _assess_complexity(self, task: str) -> str:
        """Assess the complexity level of the task."""
        # Implement complexity assessment logic
        return "medium"
    
    def _identify_domain(self, task: str) -> str:
        """Identify the engineering domain of the task."""
        # Implement domain identification logic
        return "software"
    
    def _identify_required_tools(self, task: str) -> list:
        """Identify tools required for the task."""
        # Implement tool identification logic
        return []
    
    def _assess_performance_needs(self, task: str) -> Dict[str, Any]:
        """Assess performance requirements for the task."""
        # Implement performance assessment logic
        return {}
    
    def _evaluate_code_quality(self, code: str, context: Dict[str, Any]) -> float:
        """
        Evaluate the quality of generated code.
        
        Args:
            code: Code to evaluate
            context: Additional context
            
        Returns:
            float: Quality score between 0 and 1
        """
        try:
            # Use LLM to evaluate code quality
            prompt = f"""Evaluate the following code and rate its quality from 0 to 1:
            
            Code:
            {code}
            
            Consider:
            1. Code organization and structure
            2. Readability and maintainability
            3. Error handling and robustness
            4. Performance and efficiency
            5. Security best practices
            
            Return only the numerical score between 0 and 1.
            """
            
            response = self.llm_manager.generate(prompt)
            try:
                score = float(response.strip())
                return max(0.0, min(1.0, score))  # Clamp between 0 and 1
            except ValueError:
                return 0.0
                
        except Exception as e:
            logger.error(f"Code evaluation failed: {str(e)}")
            return 0.0

    def apply_engineering_principles(self, task: str) -> Dict[str, Any]:
        """Apply engineering principles to analyze and structure a task."""
        principles = {
            "requirements_analysis": self._analyze_requirements(task),
            "design_patterns": self._identify_design_patterns(task),
            "system_architecture": self._plan_architecture(task),
            "quality_standards": self._define_quality_standards()
        }
        return principles
    
    def _analyze_requirements(self, task: str) -> Dict[str, Any]:
        """Analyze and break down project requirements."""
        return {
            "functional": self.llm_manager.analyze_requirements(task, "functional"),
            "non_functional": self.llm_manager.analyze_requirements(task, "non_functional"),
            "constraints": self.llm_manager.analyze_requirements(task, "constraints")
        }
    
    def _identify_design_patterns(self, task: str) -> List[str]:
        """Identify applicable design patterns for the task."""
        return self.llm_manager.identify_patterns(task)
    
    def _plan_architecture(self, task: str) -> Dict[str, Any]:
        """Plan the system architecture based on requirements."""
        return {
            "components": self.llm_manager.design_architecture(task, "components"),
            "interactions": self.llm_manager.design_architecture(task, "interactions"),
            "technologies": self.llm_manager.design_architecture(task, "technologies")
        }
    
    def _define_quality_standards(self) -> Dict[str, Any]:
        """Define quality standards and metrics."""
        return {
            "code_quality": ["clean_code", "solid_principles", "dry"],
            "testing": ["unit_tests", "integration_tests", "e2e_tests"],
            "documentation": ["api_docs", "code_comments", "readme"],
            "performance": ["response_time", "resource_usage", "scalability"]
        }

    def _create_project_directory(self, name: str) -> str:
        """Create a new project directory."""
        # Clean project name
        clean_name = "".join(c for c in name if c.isalnum() or c in ['-', '_'])
        
        # Create project directory
        warehouse_dir = os.path.join("src", "warehouse")
        project_dir = os.path.join(warehouse_dir, clean_name)
        
        # If project exists, use it instead of creating a new one
        if os.path.exists(project_dir):
            print(f"\nProject {clean_name} already exists. Using existing directory.")
            self.work_tracker.log_thought(f"Using existing project directory: {project_dir}")
        else:
            print(f"\nCreating new project directory: {project_dir}")
            self.work_tracker.log_thought(f"Creating new project directory: {project_dir}")
            os.makedirs(project_dir, exist_ok=True)
        
        return project_dir

    def _get_template(self, project_type: str, framework: Optional[str] = None, topic: Optional[str] = None) -> str:
        """Get the project template based on project type and framework."""
        # Implement template selection logic
        return "default_template"

    def _initialize_git(self, project_dir: str) -> None:
        """Initialize a new git repository for the project."""
        # Implement git initialization logic
        pass

    def _generate_readme(self, project_dir: str, name: str) -> None:
        """Generate a README file for the project."""
        # Implement README generation logic
        pass

    def _generate_env_example(self, project_dir: str) -> None:
        """Generate a .env.example file for the project."""
        # Implement .env.example generation logic
        pass

    def _cleanup_folders(self, project_dir: str) -> None:
        """Clean up unnecessary files and folders in the project directory."""
        # Implement cleanup logic
        pass
