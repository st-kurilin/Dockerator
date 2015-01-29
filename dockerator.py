"""Very first prototype of Dockerator.
"""

import argparse
import yaml

from docker.client import Client


def process(base_url, commands):

    def get_image_name(docker_client):
        # image_info is dict.
        # RepoTags key has ['image_name:tag', ...] value.
        image_info = max(docker_client.images(), key=lambda i: i['Created'])
        return image_info['RepoTags'][0].split(':')[0]

    def import_image(path_to_image):
        if path_to_image:
            docker_client.import_image(src=path_to_image,
                                       repository=path_to_image)

    docker_client = Client(base_url)

    import_image(commands.get('path_to_image'))

    if commands.get('ports'):
        host_port, container_port = map(int, commands.get('ports').split(':'))
        port_bindings = {container_port: host_port}
        ports = [container_port]

    container = docker_client.create_container(
        image=get_image_name(docker_client),
        command=commands.get('commands'),
        ports=ports,
        environment=commands.get('env'),
        detach=True)

    docker_client.start(container, port_bindings=port_bindings)


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
