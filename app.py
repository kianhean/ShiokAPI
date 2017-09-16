"""app.py: Entry point for apistar app"""

from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

from promos import api as promo_api
from draws import api as draw_api
from train_alert import api as train_api


routes = [
    Route('/promo', 'GET', promo_api.get_promos),
    Route('/promolist', 'GET', promo_api.promo_loop),

    Route('/draw4d', 'GET', draw_api.FourD),
    Route('/drawtoto', 'GET', draw_api.TOTO),

    Route('/trainall', 'GET', train_api.all_breakdowns),

    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
