import unittest
import subprocess as sp
import urllib2
import time


class DockerSingleImage(unittest.TestCase):

    def setUp(self):
        self.docker_host = 'tcp://192.168.59.103:2375'
        self.timeout = 600

    def test_build_container(self):
        self.run_dockerator(self.docker_host,
                            'resources/simple-web-app/build_container.yaml')
        assert self.http_get('http://192.168.59.103:1111/', self.timeout) \
            == 'Hello world'

    def test_set_env_var(self):
        self.run_dockerator(self.docker_host,
                            'resources/simple-web-app/set_env_var.yaml')
        assert self.http_get('http://192.168.59.103:3333/', self.timeout) \
            == 'This is a test'

    def run_dockerator(self, host, path_to_image):
        cmd = ['python', 'dockerator.py', '-s', path_to_image,
               '-b', host]
        sp.Popen(cmd, stdout=sp.PIPE).communicate()

    def http_get(self, url, timeout):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                return urllib2.urlopen(url).read()
            except:
                continue


if __name__ == '__main__':
    unittest.main()
