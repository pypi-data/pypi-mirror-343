import click
import sys
import os
import requests

from primeway.constants import BASE_BACKEND_URL


def get_api_token():
    # Retrieve API token from environment variable or config file
    return os.getenv('PRIMEWAY_API_TOKEN')


@click.command('job')
@click.option('--job-id', help='The ID of the job.')
@click.option('--job-execution-id', help='The ID of the job execution.')
def stop_job_command(job_id, job_execution_id):
    """Retrieve and display logs for a job or job execution."""
    if not job_id and not job_execution_id:
        click.echo("Please provide either --job-id or --job-execution-id.")
        sys.exit(1)

    api_token = get_api_token()
    headers = {'Authorization': f'Bearer {api_token}'}

    # Prepare query parameters
    params = {}
    if job_id:
        params['job_id'] = job_id
    elif job_execution_id:
        params['job_execution_id'] = job_execution_id

    # Fetch logs from the API
    response = requests.post(f'{BASE_BACKEND_URL}/job-stop', headers=headers, params=params)
    if response.status_code == 200:
        data =  response.json()
        click.echo(data)
    else:
        click.echo(f"Error occur while stopping job: {response.text}")
        sys.exit(1)