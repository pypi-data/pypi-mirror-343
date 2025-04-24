import json
import os
import importlib.util
import subprocess
import sys
import time
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# FastMCP importları (eğer yüklüyse)
try:
    import fastmcp
    from fastmcp import FastMCP  # FastMCP v2 API
    FASTMCP_AVAILABLE = True
except ImportError:
    FASTMCP_AVAILABLE = False

class MCPTool:
    """
    Represents a loaded MCP tool that can be run as an isolated FastMCP server.
    """
    def __init__(self, tool_id: str, module_path: str, port: Optional[int] = None):
        self.tool_id = tool_id
        self.module_path = module_path
        self.port = port or self._find_available_port()
        self._server_process = None
        self._module = None
        self._fastmcp_server = None
        
    def _find_available_port(self) -> int:
        """Find an available port to run the FastMCP server on."""
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def _load_module(self):
        """Load the module from the module path."""
        if self._module is None:
            # Get the absolute path to the module
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            abs_path = os.path.join(base_dir, self.module_path)
            
            # Get the module name from the file path
            module_name = os.path.splitext(os.path.basename(abs_path))[0]
            
            # Load the module
            spec = importlib.util.spec_from_file_location(module_name, abs_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load module from {abs_path}")
            
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            self._module = module
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Start the tool and return the server info.
        
        Attempts to start the tool in the following order:
        1. Loading the module and using its FastMCP instance (if it has one)
        2. Using the direct 'fastmcp run' CLI command (if available)
        3. Fallback to direct module loading
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        abs_module_path = os.path.join(base_dir, self.module_path)
        
        # Method 1: Load module and find FastMCP instance inside
        if FASTMCP_AVAILABLE:
            try:
                print(f"Starting FastMCP server for '{self.tool_id}' by loading module...")
                
                # First load the module
                self._load_module()
                
                # Find the FastMCP instance (common names: mcp, server, app)
                mcp_instance = None
                for attr_name in ["mcp", "server", "app", "fastmcp"]:
                    if hasattr(self._module, attr_name):
                        potential_instance = getattr(self._module, attr_name)
                        if isinstance(potential_instance, FastMCP):
                            mcp_instance = potential_instance
                            break
                
                if mcp_instance:
                    # Rename server for clarity
                    if hasattr(mcp_instance, "name"):
                        original_name = mcp_instance.name
                        mcp_instance.name = f"LightMCP-{self.tool_id}"
                        print(f"Found FastMCP instance named '{original_name}', renamed to '{mcp_instance.name}'")
                    
                    # Save reference and start server
                    self._fastmcp_server = mcp_instance
                    self._fastmcp_server.run(
                        port=self.port,
                        blocking=False  # Non-blocking çalıştır
                    )
                    
                    # Server başlaması için kısa bir bekleme
                    time.sleep(0.5)
                    
                    return {
                        "tool_id": self.tool_id,
                        "server_url": f"http://localhost:{self.port}",
                        "port": self.port,
                        "server_type": "fastmcp_module_instance"
                    }
                else:
                    print(f"No FastMCP instance found in module '{self.tool_id}', will try other methods")
            except Exception as e:
                print(f"Warning: Failed to start FastMCP server from module: {str(e)}")
                self._fastmcp_server = None
        
        # Method 2: Try directly using fastmcp CLI command if available
        fastmcp_path = shutil.which("fastmcp")
        if fastmcp_path:
            try:
                print(f"Starting FastMCP server for '{self.tool_id}' using FastMCP CLI (found at {fastmcp_path})...")
                
                cmd = [
                    fastmcp_path, "run",  
                    abs_module_path,   
                    "--port", str(self.port)
                ]
                
                self._server_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Wait for server to start
                time.sleep(1)
                
                if self._server_process.poll() is None:
                    # Server is still running
                    return {
                        "tool_id": self.tool_id,
                        "server_url": f"http://localhost:{self.port}",
                        "port": self.port,
                        "server_type": "fastmcp_direct_cli"
                    }
                else:
                    # Server failed to start
                    stdout, stderr = self._server_process.communicate()
                    print(f"Failed to start FastMCP server using direct CLI: {stderr}")
                    self._server_process = None
            except Exception as e:
                print(f"Warning: Failed to start FastMCP server using direct CLI: {str(e)}")
                if self._server_process:
                    self._server_process.terminate()
                    self._server_process = None
        
        # Method 3: Fallback to direct module loading
        print(f"Falling back to direct module loading for '{self.tool_id}'")
        
        # Ensure module is loaded
        if self._module is None:
            self._load_module()
        
        # Check if the module has a run method that takes no parameters
        if hasattr(self._module, "main") and callable(getattr(self._module, "main")):
            print(f"Tool '{self.tool_id}' loaded directly (not as a server)")
            return {
                "tool_id": self.tool_id,
                "module_path": self.module_path,
                "direct_load": True,
                "server_type": "direct_module",
                "message": "Tool loaded directly (not as a server)"
            }
        elif hasattr(self._module, "run") and callable(getattr(self._module, "run")):
            print(f"Tool '{self.tool_id}' loaded directly (not as a server)")
            return {
                "tool_id": self.tool_id,
                "module_path": self.module_path,
                "direct_load": True,
                "server_type": "direct_module",
                "message": "Tool loaded directly (not as a server)"
            }
        else:
            raise ValueError(f"Module {self.module_path} does not have a 'run' or 'main' function")
    
    def call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call the tool with the given parameters.
        
        This is used when the tool is loaded directly or when calling a FastMCP server.
        """
        # If server is running, use FastMCP client to make calls
        if self._fastmcp_server is not None:
            try:
                # FastMCP v2 API ile doğrudan çağrı
                from fastmcp import Client
                
                async def async_call():
                    async with Client(self._fastmcp_server) as client:
                        # İlk erişilebilir tool'u al (genellikle tek tool olacak)
                        tools = await client.list_tools()
                        if not tools:
                            raise ValueError("No tools available on the server")
                        
                        # İlk tool'u çağır
                        tool_name = tools[0]
                        result = await client.call_tool(tool_name, params)
                        return result
                
                import asyncio
                try:
                    # asyncio.run() kullan (Python 3.7+)
                    return asyncio.run(async_call())
                except RuntimeError:
                    # Eğer zaten asyncio döngüsü varsa
                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(async_call())
            except Exception as e:
                print(f"Warning: Failed to call FastMCP server directly: {str(e)}")
        
        # Try HTTP call if we have a server process running
        if self._server_process is not None and self._server_process.poll() is None:
            try:
                import requests
                response = requests.post(
                    f"http://localhost:{self.port}/mcp/v1/tools",
                    json=params
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Warning: Failed to call FastMCP server via HTTP: {str(e)}")
        
        # Fallback to direct module call
        if self._module is None:
            self._load_module()
        
        if hasattr(self._module, "run"):
            return self._module.run(params)
        else:
            raise ValueError(f"Module {self.module_path} does not have a 'run' function")
    
    def stop(self):
        """Stop the FastMCP server if it's running."""
        if self._fastmcp_server is not None:
            try:
                # Direkt stop() metodu artık kullanılabilir
                self._fastmcp_server.stop()
                print("FastMCP server stopped (library)")
            except Exception as e:
                print(f"Warning: Failed to stop FastMCP server: {str(e)}")
            finally:
                self._fastmcp_server = None
                
        if self._server_process is not None:
            self._server_process.terminate()
            self._server_process = None
            print("FastMCP server stopped (CLI)")
    
    def __del__(self):
        """Ensure server is stopped when object is garbage collected."""
        self.stop()


class ToolRegistry:
    """
    Manages the registry of available MCP tools.
    """
    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or self._get_default_registry_path()
        self.registry = self._load_registry()
        
    def _get_default_registry_path(self) -> str:
        """Get the default path to the tool registry JSON file."""
        return os.path.join(os.path.dirname(__file__), "tool_registry.json")
    
    def _load_registry(self) -> Dict[str, str]:
        """Load the tool registry from the JSON file."""
        if not os.path.exists(self.registry_path):
            return {}
        
        with open(self.registry_path, 'r') as f:
            return json.load(f)
    
    def get_tool_path(self, tool_id: str) -> Optional[str]:
        """Get the path to the tool module for the given tool ID."""
        return self.registry.get(tool_id)
    
    def list_tools(self) -> List[str]:
        """List all available tool IDs."""
        return list(self.registry.keys())
        
    def add_tool(self, tool_id: str, module_path: str) -> None:
        """
        Add a new tool to the registry.
        
        Args:
            tool_id: The ID of the tool (e.g., "notion.query_tasks")
            module_path: The path to the tool module
        """
        self.registry[tool_id] = module_path
        self._save_registry()
        
    def remove_tool(self, tool_id: str) -> bool:
        """
        Remove a tool from the registry.
        
        Args:
            tool_id: The ID of the tool to remove
            
        Returns:
            True if the tool was removed, False if it wasn't in the registry
        """
        if tool_id in self.registry:
            del self.registry[tool_id]
            self._save_registry()
            return True
        return False
        
    def _save_registry(self) -> None:
        """Save the tool registry to the JSON file."""
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)


def load_tool(tool_id: str) -> MCPTool:
    """
    Load and return an MCPTool instance for the given tool ID.
    """
    registry = ToolRegistry()
    module_path = registry.get_tool_path(tool_id)
    
    if not module_path:
        raise ValueError(f"Tool '{tool_id}' not found in registry")
    
    # Check if the module exists
    full_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), module_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Tool module not found at {full_path}")
    
    return MCPTool(tool_id, module_path)
