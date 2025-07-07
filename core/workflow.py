"""
Main workflow orchestrator for incident response.
"""

import json
import requests
from typing import Dict, Any, Optional
from kubiya_workflow_sdk.dsl import Workflow
from .config import IncidentConfig
from ..workflows.incident_response import IncidentResponseWorkflow
from ..agents.service_validator import ServiceValidationAgent


class IncidentWorkflow:
    """Main orchestrator for incident response workflows."""
    
    def __init__(self, config: Optional[IncidentConfig] = None):
        """Initialize the incident workflow orchestrator.
        
        Args:
            config: Optional incident configuration. If not provided, will be loaded from environment.
        """
        self.config = config or IncidentConfig.from_env()
        self.workflow_impl = IncidentResponseWorkflow(self.config)
        self.service_agent = ServiceValidationAgent(self.config)
    
    def create_incident_response(self, **overrides) -> Workflow:
        """Create an incident response workflow with optional parameter overrides.
        
        Args:
            **overrides: Parameters to override in the configuration
            
        Returns:
            Configured Workflow object ready for execution
            
        Example:
            workflow = incident.create_incident_response(
                incident_id="INC-123",
                incident_title="Database Issues",
                incident_severity="high"
            )
        """
        if overrides:
            # Create new config with overrides
            config_dict = self.config.dict()
            config_dict.update(overrides)
            updated_config = IncidentConfig(**config_dict)
            
            # Create new workflow with updated config
            workflow_impl = IncidentResponseWorkflow(updated_config)
            return workflow_impl.create_workflow()
        
        return self.workflow_impl.create_workflow()
    
    def create_service_validation_agent(self) -> Dict[str, Any]:
        """Create service validation agent configuration.
        
        Returns:
            Complete agent configuration dictionary
        """
        return self.service_agent.get_agent_config()
    
    def execute_workflow(self, workflow: Workflow, **execution_params) -> Dict[str, Any]:
        """Execute the workflow using the Kubiya API.
        
        Args:
            workflow: The workflow to execute
            **execution_params: Additional execution parameters
            
        Returns:
            Execution result from the API
        """
        if not self.config.kubiya_api_key:
            raise ValueError("KUBIYA_API_KEY is required for workflow execution")
        
        workflow_dict = workflow.to_dict()
        
        # Merge execution parameters
        if execution_params:
            workflow_dict["params"].update(execution_params)
        
        # Prepare API request
        url = f"https://api.kubiya.ai/api/v1/workflow?runner={self.config.runner}&operation=execute_workflow"
        headers = {
            "Authorization": f"UserKey {self.config.kubiya_api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        api_payload = {
            "command": "execute_workflow",
            "name": workflow_dict["name"],
            "description": workflow_dict["description"],
            "env": workflow_dict.get("env", {}),
            "params": workflow_dict.get("params", {}),
            "steps": workflow_dict["steps"]
        }
        
        # Execute workflow
        response = requests.post(url, headers=headers, json=api_payload, timeout=60)
        
        if response.status_code == 200:
            return {"success": True, "response": response.text}
        else:
            return {"success": False, "error": response.text, "status_code": response.status_code}
    
    def execute_workflow_stream(self, workflow: Workflow, **execution_params):
        """Execute workflow and stream results.
        
        Args:
            workflow: The workflow to execute
            **execution_params: Additional execution parameters
            
        Yields:
            Streaming response lines
        """
        if not self.config.kubiya_api_key:
            raise ValueError("KUBIYA_API_KEY is required for workflow execution")
        
        workflow_dict = workflow.to_dict()
        
        # Merge execution parameters
        if execution_params:
            workflow_dict["params"].update(execution_params)
        
        # Prepare API request
        url = f"https://api.kubiya.ai/api/v1/workflow?runner={self.config.runner}&operation=execute_workflow"
        headers = {
            "Authorization": f"UserKey {self.config.kubiya_api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        
        api_payload = {
            "command": "execute_workflow",
            "name": workflow_dict["name"],
            "description": workflow_dict["description"],
            "env": workflow_dict.get("env", {}),
            "params": workflow_dict.get("params", {}),
            "steps": workflow_dict["steps"]
        }
        
        # Execute workflow with streaming
        response = requests.post(url, headers=headers, json=api_payload, stream=True, timeout=60)
        
        if response.status_code == 200:
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    yield line
        else:
            raise Exception(f"API Error {response.status_code}: {response.text}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Export workflow to dictionary format.
        
        Returns:
            Complete workflow dictionary
        """
        workflow = self.create_incident_response()
        return workflow.to_dict()
    
    def to_json(self, indent: int = 2) -> str:
        """Export workflow to JSON format.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            JSON-formatted workflow string
        """
        workflow = self.create_incident_response()
        return workflow.to_json(indent=indent)
    
    def to_yaml(self) -> str:
        """Export workflow to YAML format.
        
        Returns:
            YAML-formatted workflow string
        """
        workflow = self.create_incident_response()
        return workflow.to_yaml()
    
    @classmethod
    def from_config_file(cls, config_path: str) -> "IncidentWorkflow":
        """Create incident workflow from configuration file.
        
        Args:
            config_path: Path to configuration file (JSON or YAML)
            
        Returns:
            Configured IncidentWorkflow instance
        """
        import yaml
        
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                config_data = yaml.safe_load(f)
            else:
                config_data = json.load(f)
        
        config = IncidentConfig(**config_data)
        return cls(config)
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> "IncidentWorkflow":
        """Create incident workflow from configuration dictionary.
        
        Args:
            config_dict: Configuration dictionary
            
        Returns:
            Configured IncidentWorkflow instance
        """
        config = IncidentConfig(**config_dict)
        return cls(config)