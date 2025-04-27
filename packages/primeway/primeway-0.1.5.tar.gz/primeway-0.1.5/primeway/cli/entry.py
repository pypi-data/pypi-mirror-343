'''
The entry point for the primeway CLI.
'''
import click
import os
from dotenv import load_dotenv, find_dotenv

# First, explicitly find the .env file
env_path = find_dotenv(usecwd=True)
if env_path:
    print(f"Found .env at: {env_path}")  # Debugging line
    load_dotenv(env_path)
else:
    print("Warning: No .env file found")  # Debugging line

# Print the value to debug (remove in production)
print(f"PRIMEWAY_API_TOKEN exists: {'PRIMEWAY_API_TOKEN' in os.environ}")

from .commands.get_logs import get_logs
from .commands.manage_jobs import (
    list_jobs, 
    list_executions, 
    get_job_info,
    get_job_logs,
    get_job_artifacts,
    get_buildjob_logs
)
from .commands.create_job import create_job
from .commands.run_job import run_job
from .commands.stop_job import stop_job_command


@click.group()
def primeway_cli():
    '''A collection of CLI functions for primeway.'''


@primeway_cli.group(name='job')
def job_group():
    """Commands related to jobs."""
    pass

@primeway_cli.group(name='pipeline')
def pipeline_group():
    """Commands related to pipelines."""
    pass


@primeway_cli.group()
def create():
    """Commands related to creation."""
    pass

# Add commands to the 'create' group
create.add_command(create_job)


@primeway_cli.group()
def run():
    """Commands related to runs."""
    pass

# Add commands to the 'run' group
run.add_command(run_job)


@primeway_cli.group()
def stop():
    """Commands related to stops."""
    pass

# Add commands to the 'run' group
stop.add_command(stop_job_command)

# Add commands to the 'jobs' group
job_group.add_command(list_jobs)
job_group.add_command(list_executions)
job_group.add_command(get_job_info)
job_group.add_command(get_job_logs)
job_group.add_command(get_job_artifacts)
job_group.add_command(get_buildjob_logs)

# Add other commands directly to 'primeway_cli'
primeway_cli.add_command(run)
primeway_cli.add_command(get_logs)

if __name__ == '__main__':
    primeway_cli()