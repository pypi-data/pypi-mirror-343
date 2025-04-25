from datetime import datetime
from datetime import timedelta

from pytz import utc
from deceit.api_client import ApiClient
from .exceptions import ChannelAdvisorException


class ChannelAdvisorApi(ApiClient):
    def __init__(self, access_token=None, refresh_token=None,
                 application_id=None, shared_secret=None,
                 base_url='https://api.channeladvisor.com',
                 default_timeout=10, **kwargs):
        super().__init__(base_url=base_url, default_timeout=default_timeout, **kwargs)
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.application_id = application_id
        self.shared_secret = shared_secret

    def headers(self, *args, **kwargs):
        return {
            'accept': 'application/json',
            'content-type': 'application/json',
            'authorization': f'Bearer {self.access_token}',
        }

    def refresh_access_token(self):
        if not self.refresh_token:
            raise ChannelAdvisorException('Refresh token is not set')
        route = 'oauth2/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }
        dt = datetime.now(utc)
        url = self.get_url(route)
        auth = (self.application_id, self.shared_secret)
        response = self.session.post(
            url, data=data, timeout=self.default_timeout,
            auth=auth,
        )
        result = self.handle_response(response)
        self.access_token = result['access_token']
        dt += timedelta(seconds=result['expires_in'])
        result['expires_at'] = dt
        return result

    def products_page(self, limit=100, raw=False, **kwargs):
        params = {
            '$top': limit,
        }
        route = 'v1/Products'
        return self.get(route, params=params, raw=raw, **kwargs)

    def orders_page(self, limit=100, raw=False, **kwargs):
        params = {
            '$top': limit,
            '$expand':
                'Items($expand = FulfillmentItems, Promotions, Adjustments, '
                'BundleComponents), Fulfillments($expand = Items), '
                'Adjustments, CustomFields'
        }
        route = 'v1/Orders'
        return self.get(route, params=params, raw=raw, **kwargs)
