"""Very first prototype of Dockerator.
"""

import argparse
import yaml

from docker.client import Client
from docker.utils import kwargs_from_env


def process(commands):

    def get_image_name():
        image_info = max(cli.images(), key=lambda i: i['Created'])
        return image_info['RepoTags'][0].split(':')[0]

    cli = Client(**kwargs_from_env())
    cli.import_image(src=commands['path_to_image'],
                     repository=commands['path_to_image'])
    host_port, container_port = map(int, commands['ports'].split(':'))
    container = cli.create_container(image=get_image_name(),
                                     command=commands['commands'],
                                     ports=[container_port],
                                     detach=True)
    cli.start(container, port_bindings={container_port: host_port})


def run():
    parser = argparse.ArgumentParser(description='Dockerator')
    parser.add_argument('-s', '--source',
                        help='Path to source ymal file', required=True)
    source = vars(parser.parse_args())['source']
    with open(source) as f:
        commands = yaml.load(f)
        process(commands)


if __name__ == '__main__':
    run()
