import unittest
import subprocess as sp
import urllib2
import time


class DockerSingleImage(unittest.TestCase):

    def test_run_simple_web_app(self):

        def run_dockerator(host, path_to_image):
            cmd = ['python', 'dockerator.py', '-s', path_to_image,
                   '-b', host]
            sp.Popen(cmd, stdout=sp.PIPE).communicate()

        def http_get(url, timeout):
            start_time = time.time()
            while time.time() - start_time < timeout:
                try:
                    return urllib2.urlopen(url).read()
                except:
                    continue

        run_dockerator('tcp://192.168.59.103:2375',
                       'resources/simple-web-app/build.yaml')
        assert http_get('http://192.168.59.103:1111/', 600) == 'Hello world'


if __name__ == '__main__':
    unittest.main()
