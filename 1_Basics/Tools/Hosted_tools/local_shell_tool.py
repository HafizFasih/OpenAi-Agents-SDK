# type: ignore
import subprocess
from agents import Agent, Runner
from agents.tool import LocalShellTool, LocalShellCommandRequest
from rich import print

# 1. Define an executor that matches LocalShellExecutor
def shell_executor(request: LocalShellCommandRequest) -> str:
    command = request.data.command  # LocalShellCall contains a `command` field
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

# 2. Instantiate the tool with your executor
shell_tool = LocalShellTool(executor=shell_executor)

# 3. Create the agent with the tool
agent = Agent(
    name="ShellBot",
    instructions="You are a helpful assistant that executes shell commands and returns the output. Only use the shell tool.",
    tools=[shell_tool]
)

# 4. Run the agent
result = Runner.run_sync(
    starting_agent=agent,
    input="List all files in the current directory"
)

# 5. Output results
print(result.final_output)
print(result.new_items)
