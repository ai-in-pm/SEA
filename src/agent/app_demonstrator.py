import os
import sys
import subprocess
import time
import requests
import psutil
import webbrowser
from typing import Dict, List, Optional, Tuple
import logging
import json
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class AppDemonstrator:
    """Demonstrates and verifies the functionality of generated web applications."""
    
    def __init__(self, project_dir: str):
        """Initialize the demonstrator with project directory."""
        self.project_dir = project_dir
        self.backend_process = None
        self.frontend_process = None
        self.backend_port = 5000
        self.frontend_port = 3000
        self.backend_url = f"http://localhost:{self.backend_port}"
        self.frontend_url = f"http://localhost:{self.frontend_port}"
        
    def _install_dependencies(self) -> Tuple[bool, str]:
        """Install backend and frontend dependencies."""
        try:
            # Install backend dependencies
            backend_dir = os.path.join(self.project_dir, 'backend')
            if os.path.exists(os.path.join(backend_dir, 'requirements.txt')):
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                             cwd=backend_dir, check=True)
            
            # Install frontend dependencies
            frontend_dir = os.path.join(self.project_dir, 'frontend')
            if os.path.exists(os.path.join(frontend_dir, 'package.json')):
                subprocess.run(['npm', 'install'], cwd=frontend_dir, check=True)
            
            return True, "Dependencies installed successfully"
        except subprocess.CalledProcessError as e:
            return False, f"Failed to install dependencies: {str(e)}"
        
    def _start_backend(self) -> Tuple[bool, str]:
        """Start the Flask backend server."""
        try:
            backend_dir = os.path.join(self.project_dir, 'backend')
            env = os.environ.copy()
            env['FLASK_APP'] = 'app'
            env['FLASK_ENV'] = 'development'
            
            self.backend_process = subprocess.Popen(
                [sys.executable, '-m', 'flask', 'run'],
                cwd=backend_dir,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for backend to start
            for _ in range(30):  # 30 seconds timeout
                try:
                    response = requests.get(f"{self.backend_url}/health")
                    if response.status_code == 200:
                        return True, "Backend started successfully"
                except requests.RequestException:
                    time.sleep(1)
            
            return False, "Backend failed to start within timeout"
        except Exception as e:
            return False, f"Failed to start backend: {str(e)}"
    
    def _start_frontend(self) -> Tuple[bool, str]:
        """Start the React frontend development server."""
        try:
            frontend_dir = os.path.join(self.project_dir, 'frontend')
            
            self.frontend_process = subprocess.Popen(
                ['npm', 'start'],
                cwd=frontend_dir,
                env={'PORT': str(self.frontend_port), **os.environ},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for frontend to start
            for _ in range(60):  # 60 seconds timeout
                try:
                    response = requests.get(self.frontend_url)
                    if response.status_code == 200:
                        return True, "Frontend started successfully"
                except requests.RequestException:
                    time.sleep(1)
            
            return False, "Frontend failed to start within timeout"
        except Exception as e:
            return False, f"Failed to start frontend: {str(e)}"
    
    def _verify_api_endpoints(self) -> List[Dict[str, str]]:
        """Verify that key API endpoints are working."""
        endpoints = [
            ('/api/health', 'GET'),
            ('/api/auth/register', 'POST'),
            ('/api/auth/login', 'POST'),
            ('/api/users/profile', 'GET'),
        ]
        
        results = []
        for endpoint, method in endpoints:
            try:
                if method == 'GET':
                    response = requests.get(f"{self.backend_url}{endpoint}")
                else:
                    response = requests.post(f"{self.backend_url}{endpoint}", json={})
                
                results.append({
                    'endpoint': endpoint,
                    'method': method,
                    'status': 'Success' if response.status_code < 500 else 'Failed',
                    'status_code': str(response.status_code)
                })
            except requests.RequestException as e:
                results.append({
                    'endpoint': endpoint,
                    'method': method,
                    'status': 'Failed',
                    'error': str(e)
                })
        
        return results
    
    def _generate_demo_report(self, api_results: List[Dict[str, str]]) -> str:
        """Generate a markdown report of the demonstration results."""
        report = [
            "# Web Application Demonstration Report\n",
            "## API Endpoint Status\n",
            "| Endpoint | Method | Status | Status Code |",
            "|----------|---------|---------|-------------|"
        ]
        
        for result in api_results:
            status_code = result.get('status_code', 'N/A')
            report.append(
                f"| {result['endpoint']} | {result['method']} | "
                f"{result['status']} | {status_code} |"
            )
        
        report.append("\n## Application URLs")
        report.append(f"- Frontend: {self.frontend_url}")
        report.append(f"- Backend API: {self.backend_url}")
        report.append("\n## Next Steps")
        report.append("1. Open the frontend URL in your browser")
        report.append("2. Try registering a new user")
        report.append("3. Test the login functionality")
        report.append("4. Explore the application features")
        
        return "\n".join(report)
    
    def _cleanup(self):
        """Clean up processes when demonstration is complete."""
        try:
            if self.backend_process:
                for child in psutil.Process(self.backend_process.pid).children(recursive=True):
                    child.terminate()
                self.backend_process.terminate()
            
            if self.frontend_process:
                for child in psutil.Process(self.frontend_process.pid).children(recursive=True):
                    child.terminate()
                self.frontend_process.terminate()
                
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
    
    def _analyze_and_fix_error(self, error: str, component: str) -> Tuple[bool, str]:
        """Analyze and attempt to fix common errors."""
        try:
            if component == 'backend':
                return self._fix_backend_error(error)
            elif component == 'frontend':
                return self._fix_frontend_error(error)
            elif component == 'dependencies':
                return self._fix_dependency_error(error)
            else:
                return False, f"Unknown component: {component}"
        except Exception as e:
            return False, f"Error fixing failed: {str(e)}"

    def _retry_with_fixes(self, operation: str, error_msg: str, component: str, 
                         func: callable, max_attempts: int = 5) -> Tuple[bool, str]:
        """
        Retry an operation with automatic error fixing.
        
        Args:
            operation: Name of the operation being performed
            error_msg: Initial error message
            component: Component type ('backend', 'frontend', or 'dependencies')
            func: Function to retry
            max_attempts: Maximum number of fix attempts
            
        Returns:
            Tuple of (success status, message)
        """
        attempt = 1
        last_error = error_msg
        errors_seen = set()  # Track unique errors to avoid fixing the same thing repeatedly
        
        while attempt <= max_attempts:
            print(f"\nAttempt {attempt}/{max_attempts} to fix {component} error:")
            print(f"Error: {last_error}")
            
            # Don't try to fix the same error twice
            if last_error in errors_seen:
                print("This error was seen before, trying different fix strategy...")
                attempt += 1
                continue
                
            errors_seen.add(last_error)
            
            # Attempt to fix the error
            fixed, fix_message = self._analyze_and_fix_error(last_error, component)
            
            if fixed:
                print(f"Fix applied: {fix_message}")
                # Retry the operation
                success, new_message = func()
                
                if success:
                    print(f"\n{operation} successful after fixes!")
                    return True, new_message
                else:
                    last_error = new_message
            else:
                print(f"Unable to fix error: {fix_message}")
                attempt += 1
        
        return False, f"Failed to fix {component} after {max_attempts} attempts. Last error: {last_error}"

    def demonstrate(self) -> Tuple[bool, str, Optional[str]]:
        """
        Demonstrate the web application by starting servers and verifying functionality.
        
        Returns:
            Tuple containing:
            - Success status (bool)
            - Status message (str)
            - Demo report content (str or None)
        """
        try:
            print("\nStarting Web Application Demonstration...")
            
            # Install dependencies
            print("\n[1/4] Installing dependencies...")
            success, message = self._install_dependencies()
            if not success:
                success, message = self._retry_with_fixes(
                    "Dependency installation",
                    message,
                    'dependencies',
                    self._install_dependencies
                )
                if not success:
                    return False, message, None
            
            # Start backend
            print("\n[2/4] Starting backend server...")
            success, message = self._start_backend()
            if not success:
                success, message = self._retry_with_fixes(
                    "Backend startup",
                    message,
                    'backend',
                    self._start_backend
                )
                if not success:
                    return False, message, None
            
            # Start frontend
            print("\n[3/4] Starting frontend server...")
            success, message = self._start_frontend()
            if not success:
                success, message = self._retry_with_fixes(
                    "Frontend startup",
                    message,
                    'frontend',
                    self._start_frontend
                )
                if not success:
                    return False, message, None
            
            # Verify API endpoints
            print("\n[4/4] Verifying API endpoints...")
            api_results = self._verify_api_endpoints()
            
            # Generate and save report
            report = self._generate_demo_report(api_results)
            report_path = os.path.join(self.project_dir, 'demo_report.md')
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
                
                # Add fix attempts information to the report
                f.write("\n\n## Fix Attempts Summary\n")
                if hasattr(self, '_fix_attempts'):
                    for component, attempts in self._fix_attempts.items():
                        f.write(f"\n### {component.title()} Fixes\n")
                        for attempt in attempts:
                            f.write(f"- {attempt}\n")
                else:
                    f.write("No fixes were needed during demonstration.\n")
            
            # Open application in browser
            webbrowser.open(self.frontend_url)
            
            return True, "Demonstration completed successfully", report
            
        except Exception as e:
            return False, f"Demonstration failed: {str(e)}", None
        
        finally:
            self._cleanup()

    def _fix_backend_error(self, error: str) -> Tuple[bool, str]:
        """Fix common backend errors."""
        backend_dir = os.path.join(self.project_dir, 'backend')
        
        # Initialize fix attempts tracking if not exists
        if not hasattr(self, '_fix_attempts'):
            self._fix_attempts = {'backend': [], 'frontend': [], 'dependencies': []}
        
        try:
            fix_applied = None
            
            if "ModuleNotFoundError" in error:
                # Fix missing imports
                module_name = error.split("'")[1]
                subprocess.run([sys.executable, '-m', 'pip', 'install', module_name],
                             cwd=backend_dir, check=True)
                fix_applied = f"Installed missing module: {module_name}"
                
            elif "Address already in use" in error:
                # Fix port conflict
                self.backend_port += 1
                self.backend_url = f"http://localhost:{self.backend_port}"
                fix_applied = f"Changed backend port to {self.backend_port}"
                
            elif "No module named 'flask'" in error:
                # Fix missing Flask
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'flask'],
                             cwd=backend_dir, check=True)
                fix_applied = "Installed Flask"
                
            elif "SQLAlchemy" in error:
                # Fix database issues
                fixes = [
                    "pip install sqlalchemy",
                    "pip install psycopg2-binary",
                    "pip install flask-sqlalchemy"
                ]
                for fix in fixes:
                    subprocess.run(fix.split(), cwd=backend_dir, check=True)
                fix_applied = "Installed database dependencies"
            
            if fix_applied:
                self._fix_attempts['backend'].append(fix_applied)
                return True, fix_applied
                
            return False, "Unable to automatically fix this backend error"
            
        except Exception as e:
            return False, f"Backend fix failed: {str(e)}"

    def _fix_frontend_error(self, error: str) -> Tuple[bool, str]:
        """Fix common frontend errors."""
        frontend_dir = os.path.join(self.project_dir, 'frontend')
        
        # Initialize fix attempts tracking if not exists
        if not hasattr(self, '_fix_attempts'):
            self._fix_attempts = {'backend': [], 'frontend': [], 'dependencies': []}
        
        try:
            fix_applied = None
            
            if "ENOENT" in error and "package.json" in error:
                # Fix missing package.json
                self._create_basic_package_json(frontend_dir)
                fix_applied = "Created basic package.json"
                
            elif "react-scripts" in error:
                # Fix missing react-scripts
                subprocess.run(['npm', 'install', 'react-scripts', '--save-dev'],
                             cwd=frontend_dir, check=True)
                fix_applied = "Installed react-scripts"
                
            elif "EADDRINUSE" in error:
                # Fix port conflict
                self.frontend_port += 1
                os.environ['PORT'] = str(self.frontend_port)
                self.frontend_url = f"http://localhost:{self.frontend_port}"
                fix_applied = f"Changed frontend port to {self.frontend_port}"
            
            if fix_applied:
                self._fix_attempts['frontend'].append(fix_applied)
                return True, fix_applied
                
            return False, "Unable to automatically fix this frontend error"
            
        except Exception as e:
            return False, f"Frontend fix failed: {str(e)}"

    def _fix_dependency_error(self, error: str) -> Tuple[bool, str]:
        """Fix common dependency errors."""
        # Initialize fix attempts tracking if not exists
        if not hasattr(self, '_fix_attempts'):
            self._fix_attempts = {'backend': [], 'frontend': [], 'dependencies': []}
        
        try:
            fix_applied = None
            
            if "npm" in error.lower():
                # Fix npm installation
                if sys.platform == 'win32':
                    subprocess.run(['npm', 'install', '-g', 'npm'], check=True)
                else:
                    subprocess.run(['sudo', 'npm', 'install', '-g', 'npm'], check=True)
                fix_applied = "Updated npm installation"
                
            elif "python" in error.lower() or "pip" in error.lower():
                # Fix pip installation
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'],
                             check=True)
                fix_applied = "Updated pip installation"
            
            if fix_applied:
                self._fix_attempts['dependencies'].append(fix_applied)
                return True, fix_applied
                
            return False, "Unable to automatically fix this dependency error"
            
        except Exception as e:
            return False, f"Dependency fix failed: {str(e)}"

    def _create_basic_package_json(self, frontend_dir: str):
        """Create a basic package.json file if missing."""
        package_json = {
            "name": "frontend",
            "version": "0.1.0",
            "private": True,
            "dependencies": {
                "react": "^17.0.2",
                "react-dom": "^17.0.2",
                "react-router-dom": "^6.0.0",
                "axios": "^0.24.0"
            },
            "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "eject": "react-scripts eject"
            },
            "eslintConfig": {
                "extends": ["react-app"]
            },
            "browserslist": {
                "production": [">0.2%", "not dead", "not op_mini all"],
                "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
            }
        }
        
        os.makedirs(frontend_dir, exist_ok=True)
        with open(os.path.join(frontend_dir, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
