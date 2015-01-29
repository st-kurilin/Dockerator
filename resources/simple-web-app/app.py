import web
import os

urls = (
    '/', 'index'
)


class index:
    def GET(self):
        env_var = os.environ.get('TEST_FOO')
        return env_var or 'Hello world'


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
