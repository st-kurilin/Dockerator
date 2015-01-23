"""Very first prototype of Dockerator.
"""

import argparse
import yaml

from docker.client import Client


def process(base_url, commands):

    def get_image_name():
        # image_info is dict.
        # RepoTags key has ['image_name:tag', ...] value.
        image_info = max(cli.images(), key=lambda i: i['Created'])
        return image_info['RepoTags'][0].split(':')[0]

    cli = Client(base_url)
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
    parser.add_argument('-b', '--host',
                        help='Docker host server base url',
                        required=True)
    args = vars(parser.parse_args())
    with open(args['source']) as f:
        commands = yaml.load(f)
        process(args['host'], commands)


if __name__ == '__main__':
    run()
