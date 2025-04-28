import click
import logging
from requests import RequestException
from .api import SonarQube
from .community import Project
from . import parser

# logging
logger = logging.getLogger()

pass_config = click.make_pass_decorator(Project, ensure=True)

@click.group()
@click.option('-c', 'config', help='Configuration file')
@click.option('-s', 'suffix', help='Suffix to use when managing SonarQube projects')
@click.option('-r', 'repository_id', help='Version control repository ID')
@click.option('-u', 'url', help='SonarQube url')
@click.option('-h', 'host', help='SonarQube host')
@click.option('-p', 'port', help='SonarQube port')
@click.option('-t', 'token', help='SonarQube personal access token')
@click.option('-l', 'log_level', help='Logging level')
@click.pass_context
def cli(ctx, config=None, suffix=None, repository_id=None, url=None, host=None, port=None, token=None, log_level=None):
    logging.basicConfig(level=log_level or logging.INFO)
    sq = SonarQube(url=url, host=host, port=port, token=token)
    ctx.obj = parser.read_project(file=config, repository_id=repository_id, suffix=suffix, sq = sq)

@cli.command()
@pass_config
def create(project):
    try:
        project.create_or_update()
    except RequestException as e:
        handleRequestException('create', e)

@cli.command()
@pass_config
def delete(project):
    try:
        project.delete()
    except RequestException as e:
        handleRequestException('delete', e)

def handleRequestException(command, e):
    err_code = 1
    if (e.response is not None):
        status_code = e.response.status_code
        logger.info(f"Error on '{ command }' with response: { vars(e.response) }")
        err_code = int(str(status_code)[:1])
    logger.error(f"Error on 'create' returning error code [{ err_code }]")
    raise click.exceptions.Exit(err_code)

if __name__ == "__main__":
    cli()
