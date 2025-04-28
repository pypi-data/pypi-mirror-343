import logging
from os import path
import yaml
import configparser
from .community import Project
from .exceptions import CliException

# logging
logger = logging.getLogger()

DEFAULT_ALM_PROFILE = 'NHSBSA_GITLAB'

def read_project(file = None, repository_id = None, suffix = None, sq = None):
    
    config_filename = None

    if file:
        config_filename = _find_file(file)
        if not config_filename:
            raise CliException(f"Specified Sonarqube config file does not exist: [{file}]")
    else:
        config_filename = _find_file('sonar-project.properties', '.sonarqube.yml')
        if not config_filename:
            raise CliException("No config file specified and default does not exist. " 
                            "Define .sonarqube.yml or sonar-project.properties")

    if(config_filename.endswith('.yml') or config_filename.endswith('.yaml')):
        return _read_yaml(config_filename, repository_id, suffix, sq)
    elif(config_filename.endswith('.properties')):
        return _read_properties(config_filename, repository_id, suffix, sq)
    else:
        raise CliException(f"Invalid config file extension [{config_filename}]")

def _find_file(*filenames):
    for filename in filenames:
        if filename and path.isfile(filename):
            return filename

    
def _read_yaml(config_filename, repository_id, suffix = None, sq = None):
    with open(config_filename, "r") as stream:
        try:
            # takes the last key defined in the event of duplicates
            config = yaml.safe_load(stream)
            config_project = config['project']
            return Project(
                key = config_project['key'],
                name = config_project['name'],
                project_id = repository_id,
                #wrapper around boolean to ensure it is read as a string (API expects this)
                monorepo = str(config_project['monorepo']).lower() if 'monorepo' in config_project.keys() else 'false',
                alm_profile= config_project['alm-profile'] if 'alm-profile' in config_project.keys() else  DEFAULT_ALM_PROFILE,
                suffix = suffix,
                quality_gate = config_project['quality-gate'],
                quality_profiles = config_project['quality-profiles'] or {},
                sq = sq
            )
        except (KeyError, TypeError, yaml.YAMLError) as exc:
            raise CliException(f"Failed to parse config file [{config_filename}] {exc}")

def _read_properties(config_filename, repository_id, suffix = None, sq = None):
    parser = configparser.ConfigParser()
    with open(config_filename, 'r') as stream:
        try:
            parser.read_string('[root]\n' + stream.read())
            profiles = _collect_prefixed_properties_to_dict(parser.items('root'), 'project.quality-profiles.')
            return Project(
            key = parser.get('root','sonar.projectKey'),
            name = parser.get('root','sonar.projectName'),
            project_id = repository_id,
            monorepo = parser.get('root', 'project.monorepo', fallback='false'),
            alm_profile = parser.get('root', 'project.alm-profile', fallback=DEFAULT_ALM_PROFILE),
            suffix = suffix,
            quality_gate = parser.get('root','project.quality-gate'),
            quality_profiles = profiles,
            sq = sq
            )
        except (configparser.DuplicateOptionError, configparser.NoOptionError, configparser.ParsingError) as exc:
            raise CliException(f"Failed to parse config file [{config_filename}] {exc}")
        
def _collect_prefixed_properties_to_dict(props, prefix):
    props_dict = {}
    for prop in props:
        if(prop[0].startswith(prefix)):
            key = prop[0].rsplit(prefix, 1)[1]
            value = prop[1]
            props_dict[key] = value
    return props_dict
            

if __name__ == "__main__":
    logger.error("Parser script intended for use as an import")
