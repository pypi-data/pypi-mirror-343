import asyncio
import os
import datetime

from agents import Agent, Runner, gen_trace_id, set_default_openai_key, trace
from agents.mcp.server import MCPServerSse
from agents.model_settings import ModelSettings

from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console
from rich.panel import Panel

from .mcp_server_utils import start_mcp_server_app, MCP_CONFIG

console = Console()


async def run_test_suite(test_suites, openai_api_key, path_log_files, headless=True):
    """
    Run automated test suites using Playwright through MCP.
    
    Parameters:
        test_suites (dict): Dictionary of test suites to run. REQUIRED.
            Each entry should be in the format: 
            "test-key": ("Test Name", "Test Instructions")
            The tuple structure is intentional for immutability.
        openai_api_key (str): OpenAI API key to use for testing. REQUIRED.
    """
    artifacts_dir = path_log_files
    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)
        console.print(f"[green]Created artifacts directory: {artifacts_dir}[/green]")
    
    console.print(Panel("[bold blue]Playwright Automated Test Suite[/bold blue]", 
                        subtitle="Running predefined test tasks"))
    
    if not start_mcp_server_app(headless=headless):
        return
    
    console.print("[yellow]Waiting for MCP server to initialize...[/yellow]")
    
    if openai_api_key:
        set_default_openai_key(openai_api_key)
    else:        
        console.print("[red]OPENAI_API_KEY is required...[/red]")
        return
        
    if not test_suites:
        console.print("[red]No tests provided. test_suites parameter is required...[/red]")
        return
        
    console.print("\n[bold cyan]Available Test Suites:[/bold cyan]")
    for (name, _) in test_suites:
        console.print(f"  [yellow]{name}[/yellow]")  
  
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
    console.print(f"\n[bold yellow]Starting tests[/bold yellow]")
    
    async with MCPServerSse(
        name="playwright_mcp_server",
        params={"url": f"http://{MCP_CONFIG['host']}:{MCP_CONFIG['port']}"},
        cache_tools_list=True,
    ) as playwright_mcp_server:
        trace_id = gen_trace_id()
        with trace(workflow_name="mcp_playwright", trace_id=trace_id):
            console.print(f"[green]View trace:[/green] https://platform.openai.com/traces/{trace_id}")

        mcp_agent = Agent(
            name="mcp_play_agent",
            model="gpt-4.1",
            instructions=(           
                """You are an automated testing assistant utilizing MCP server tools for precise web testing operations. Clearly display each MCP tool used and
                   its corresponding output in the console after every step. 
                
                Follow these explicit guidelines:

                1. Execute each web test exactly as described.
                2. Always wait for the previous step to complete fully before starting the next one.
                3. Ensure all web pages are fully loaded before continuing to subsequent steps.
                4. If an issue or unexpected behavior occurs, document it clearly, then restart the entire test up to a maximum of 3 retries.
                5. Extract, summarize, and clearly log relevant information from each tested webpage.
                6. Clearly document any errors, inconsistencies, or unexpected behaviors encountered during the tests.
                7. After every step, explicitly display all MCP tools utilized and their outputs directly in the console.
                """
            ),
            mcp_servers=[playwright_mcp_server],
            model_settings=ModelSettings(tool_choice="auto"),
        )
        
        conversation_history = []
        
        console.print("\n[bold yellow]Starting automated test sequence...[/bold yellow]")
        
        for i, task in enumerate(test_suites, 1):
            console.print(f"\n[bold cyan]Task {i}/{len(test_suites)}:[/bold cyan] {task[0]}")
            console.print("[dim]Processing...[/dim]")
                        
            task_dir = os.path.join(artifacts_dir, f"{task[0]}_{current_date}")
            if not os.path.exists(task_dir):
                os.makedirs(task_dir)
                console.print(f"[green]Created task directory: {task_dir}[/green]")
            
            conversation_history.append(f"Test Task: {task[0]}")
            
            if len(conversation_history) > 1:
                context_prompt = "Previous test results:\n"
                for entry in conversation_history[-4:-1]:
                    if entry.startswith("Test Task:"):
                        continue
                    context_prompt += f"{entry}\n"
                context_prompt += f"\nCurrent test task {task[0]}: {task[1]}"
            else:
                context_prompt = f"Perform this test {task[0]}: {task[1]}"
            
            result = Runner.run_streamed(
                starting_agent=mcp_agent,
                input=context_prompt,
                max_turns=100
            )
            
            console.print("\n[bold green]Test Results:[/bold green]")
            response_text = ""
            
            async for event in result.stream_events():
                if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                    response_text += event.data.delta
                    console.print(event.data.delta, end="", highlight=False)                    
            
            conversation_history.append(f"Test Result: {response_text}")
            summary_path = os.path.join(artifacts_dir, f"test_{task[0]}_{current_date}.txt")   
            save_to_file(response_text, summary_path)
        
        console.print("\n[bold green]✓ Automated test sequence completed[/bold green]")
        
        console.print("\n[bold blue]Generating test summary...[/bold blue]")
        summary_prompt = "Create a summary report of all the tests that were performed and their results. Include any issues found and recommendations for fixing them."
        
        summary_result = Runner.run_streamed(
            starting_agent=mcp_agent,
            input=summary_prompt,
            max_turns=100
        )
        
        console.print("\n[bold green]Test Summary Report:[/bold green]")
        summary_text = ""
        
        async for event in summary_result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                summary_text += event.data.delta
                console.print(event.data.delta, end="", highlight=False)
                
     

        summary_path = os.path.join(artifacts_dir, f"test_summary_{current_date}.txt")
        save_to_file(summary_text, summary_path, "Test summary saved to")

    
def save_to_file(content, filepath, message="File saved"):
    """Save content to a file and print status message."""
    try:
        with open(filepath, "w") as f:
            f.write(content)
        console.print(f"\n[green]{message}: {filepath}[/green]")
        return True
    except Exception as e:
        console.print(f"\n[red]Failed to save file: {str(e)}[/red]")
        return False  


if __name__ == "__main__":
    try:
        asyncio.run(run_test_suite())
    except KeyboardInterrupt:
        console.print("\n[yellow]Test execution interrupted by user.[/yellow]")
    finally:
        # Cleanup code here if needed
        console.print("[green]Test execution completed.[/green]")
