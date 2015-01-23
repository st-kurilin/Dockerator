import unittest
import subprocess as sp
import urllib2
import time


class DockerSingleImage(unittest.TestCase):

    def test_run_single_image(self):
        cmd = ['python', 'dockerator.py', '-s', 'single_app/build.yaml']
        sp.Popen(cmd, stdout=sp.PIPE).communicate()
        timeout = time.time() + 600  # 10 minutes timeout
        while time.time() < timeout:
            try:
                url = 'http://192.168.59.103:1111/'
                if urllib2.urlopen(url).read() == 'Hello world':
                    return "Great success"
            except:
                time.sleep(30)
        raise Exception

if __name__ == '__main__':
    unittest.main()
