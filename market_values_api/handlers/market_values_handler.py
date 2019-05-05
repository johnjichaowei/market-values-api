from aiohttp import web
import logging
import simplejson
import market_values_api.services as services

class MarketValuesHandler(object):
    async def get(self, request):
        logging.info(f"Handling get market values request: {request.query_string}")
        companies = self._parse_companies_param(request.query)
        service = services.MarketValuesService(request.app['client_session'])
        market_values = await service.get(companies)
        logging.info(f"Finishing get market values request")
        return self._json_response(market_values)

    def _parse_companies_param(self, query):
        if 'companies' not in query:
            raise web.HTTPBadRequest(reason='The companies param is required')

        param = query['companies']
        return param.split(',')

    def _json_response(self, data):
        response = web.Response()
        response.headers.add('Content-Type', 'application/json')
        response.text = simplejson.dumps(data)
        return response
