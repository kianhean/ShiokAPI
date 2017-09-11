from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

from promos import api as promo_api
from draws import api as draw_api


def welcome():
    """ Welcome Message """
    return {'message': 'Welcome to ShiokAPI!'}


routes = [
    Route('/', 'GET', welcome),
    Route('/promo', 'GET', promo_api.get_promos),
    Route('/promolist', 'GET', promo_api.promo_loop),
    Route('/draw4d', 'GET', draw_api.FourD),
    Route('/drawtoto', 'GET', draw_api.TOTO),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
