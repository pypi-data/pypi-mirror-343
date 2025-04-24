import subprocess
import socket
import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

MCP_CONFIG = {
    "host": "localhost",
    "port": 8931,
    "start_mcp": "npx @playwright/mcp@latest --port {port}",
    
}

console = Console()

def is_port_in_use(port, host='localhost'):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def is_mcp_server_running(url='http://localhost:8931/sse'):
    try:
        response = requests.get(f"{url}")
        return response.status_code == 200
    except requests.RequestException:
        return False

def start_mcp_server(port=8931, headless=True):
    console.print(f"[yellow]MCP server not detected on port {port}. Starting it now with Playwright MCP...[/yellow]")
    command = MCP_CONFIG["start_mcp"].format(port=port)
    if headless:
        command += " --headless"
    shell = True
    
    try:
        process = subprocess.Popen(command, shell=shell)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[yellow]Starting Playwright MCP server... {task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("", total=None)
            
            progress.update(task, description="Server started successfully!")
            console.print(f"[green]Playwright MCP server started successfully on port {port}[/green]")                
            return True
            
    except Exception as e:
        console.print(f"[red]Failed to start Playwright MCP server: {str(e)}[/red]")
        return False

def start_mcp_server_app(port=None, config=None):
    cfg = config or MCP_CONFIG
    port = port or cfg["port"]
    host = cfg["host"]
    
    mcp_url = f"http://{host}:{port}/sse"
    
    if not is_port_in_use(port, host):
        server_started = start_mcp_server(port)
        if not server_started:
            console.print("[red]Could not start Playwright MCP server. Please start it manually with:[/red]")
            console.print(f"[yellow]npx @playwright/mcp@latest --port {port}[/yellow]")
            return False
        return True
    else:      
        console.print(f"[green]MCP server already running on {mcp_url}[/green]")
        return True
      