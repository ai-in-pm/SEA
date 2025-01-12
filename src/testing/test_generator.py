from typing import Dict, Any, List
import json
import os
from ..llm import LLMManager
from ..utils.config import Config

class TestGenerator:
    """Advanced test generation with multiple testing strategies."""
    
    def __init__(self, config: Config):
        self.config = config
        self.llm_manager = LLMManager(config)
    
    def generate_test_suite(self, code: Dict[str, str], framework: str) -> Dict[str, str]:
        """Generate comprehensive test suite."""
        test_suite = {}
        
        # Generate unit tests
        unit_tests = self.generate_unit_tests(code, framework)
        test_suite.update(unit_tests)
        
        # Generate integration tests
        integration_tests = self.generate_integration_tests(code, framework)
        test_suite.update(integration_tests)
        
        # Generate end-to-end tests
        e2e_tests = self.generate_e2e_tests(code, framework)
        test_suite.update(e2e_tests)
        
        return test_suite
    
    def generate_unit_tests(self, code: Dict[str, str], framework: str) -> Dict[str, str]:
        """Generate unit tests for all components."""
        unit_tests = {}
        test_llm = self.llm_manager.select_llm({"complexity": "medium", "domain": "testing"})
        
        for component, component_code in code.items():
            prompt = self._create_unit_test_prompt(component, component_code, framework)
            response = test_llm.process(prompt)
            unit_tests[f"test_{component}.py"] = response["response"]
        
        return unit_tests
    
    def generate_integration_tests(self, code: Dict[str, str], framework: str) -> Dict[str, str]:
        """Generate integration tests for component interactions."""
        integration_tests = {}
        test_llm = self.llm_manager.select_llm({"complexity": "high", "domain": "testing"})
        
        # Group related components
        component_groups = self._group_related_components(code)
        
        for group_name, components in component_groups.items():
            prompt = self._create_integration_test_prompt(components, framework)
            response = test_llm.process(prompt)
            integration_tests[f"test_integration_{group_name}.py"] = response["response"]
        
        return integration_tests
    
    def generate_e2e_tests(self, code: Dict[str, str], framework: str) -> Dict[str, str]:
        """Generate end-to-end tests for complete workflows."""
        e2e_tests = {}
        test_llm = self.llm_manager.select_llm({"complexity": "high", "domain": "testing"})
        
        # Identify main workflows
        workflows = self._identify_workflows(code)
        
        for workflow_name, workflow_specs in workflows.items():
            prompt = self._create_e2e_test_prompt(workflow_specs, framework)
            response = test_llm.process(prompt)
            e2e_tests[f"test_e2e_{workflow_name}.py"] = response["response"]
        
        return e2e_tests
    
    def _create_unit_test_prompt(self, component: str, code: str, framework: str) -> str:
        """Create prompt for unit test generation."""
        return json.dumps({
            "role": "system",
            "content": f"Generate unit tests for this component using {framework}.",
            "component": component,
            "code": code,
            "framework": framework,
            "requirements": [
                "Test each function/method independently",
                "Include edge cases",
                "Mock external dependencies",
                "Achieve high code coverage"
            ]
        })
    
    def _create_integration_test_prompt(self, components: Dict[str, str], framework: str) -> str:
        """Create prompt for integration test generation."""
        return json.dumps({
            "role": "system",
            "content": f"Generate integration tests using {framework}.",
            "components": components,
            "framework": framework,
            "requirements": [
                "Test component interactions",
                "Verify data flow between components",
                "Test error handling between components",
                "Include common integration scenarios"
            ]
        })
    
    def _create_e2e_test_prompt(self, workflow: Dict[str, Any], framework: str) -> str:
        """Create prompt for end-to-end test generation."""
        return json.dumps({
            "role": "system",
            "content": f"Generate end-to-end tests using {framework}.",
            "workflow": workflow,
            "framework": framework,
            "requirements": [
                "Test complete user workflows",
                "Verify system-wide functionality",
                "Include realistic user scenarios",
                "Test performance and reliability"
            ]
        })
    
    def _group_related_components(self, code: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """Group related components for integration testing."""
        groups = {}
        
        # Simple grouping based on naming conventions
        for component, component_code in code.items():
            if "model" in component.lower():
                groups.setdefault("data_layer", {})[component] = component_code
            elif "service" in component.lower() or "repository" in component.lower():
                groups.setdefault("service_layer", {})[component] = component_code
            elif "controller" in component.lower() or "view" in component.lower():
                groups.setdefault("presentation_layer", {})[component] = component_code
            else:
                groups.setdefault("misc", {})[component] = component_code
        
        return groups
    
    def _identify_workflows(self, code: Dict[str, str]) -> Dict[str, Dict[str, Any]]:
        """Identify main workflows for end-to-end testing."""
        workflows = {}
        
        # Analyze code to identify main workflows
        api_endpoints = self._extract_api_endpoints(code)
        user_interfaces = self._extract_user_interfaces(code)
        data_flows = self._extract_data_flows(code)
        
        # Combine into workflows
        if api_endpoints:
            workflows["api"] = {
                "type": "api",
                "endpoints": api_endpoints,
                "data_flows": data_flows
            }
        
        if user_interfaces:
            workflows["ui"] = {
                "type": "ui",
                "interfaces": user_interfaces,
                "data_flows": data_flows
            }
        
        return workflows
    
    def _extract_api_endpoints(self, code: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract API endpoints from code."""
        endpoints = []
        for component, component_code in code.items():
            if "api" in component.lower() or "controller" in component.lower():
                # Basic endpoint extraction (could be enhanced with proper parsing)
                for line in component_code.split("\n"):
                    if "@route" in line or "@app." in line:
                        endpoints.append({
                            "path": line,
                            "component": component
                        })
        return endpoints
    
    def _extract_user_interfaces(self, code: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract user interface components from code."""
        interfaces = []
        for component, component_code in code.items():
            if "view" in component.lower() or "component" in component.lower():
                interfaces.append({
                    "name": component,
                    "type": "view"
                })
        return interfaces
    
    def _extract_data_flows(self, code: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract data flows from code."""
        flows = []
        # Analyze code for data flow patterns
        # This is a simplified version and could be enhanced
        for component, component_code in code.items():
            if "repository" in component.lower() or "service" in component.lower():
                flows.append({
                    "source": component,
                    "type": "data_access"
                })
        return flows
    
    def _write_test_file(self, file_path: str, test_code: str) -> None:
        """Write test code to file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(test_code)
