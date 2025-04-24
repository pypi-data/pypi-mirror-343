from iiko_sdk import errors, services, http_utils


class MenuGateway:
    version = 'api/2'

    def __init__(self, base_url: str, service: services.BaseService):
        self.base_url = base_url
        self.service = service

    async def get_external_menus(self):
        """ Получить Ids внешних меню из Web """
        url = http_utils.join_str(self.base_url, self.version, '/menu')
        request = {
            'method': 'POST',
            'url': url
        }
        response = await self.service.send_request(**request)
        if response.status != 200:
            raise errors.InteractionError(response.status, response.response_data)

        return response.response_data

    async def get_menu_by_id(self, menu_id: str, restaurants: list[str]):
        """ Получение Web меню по id """
        url = http_utils.join_str(self.base_url, self.version, '/menu/by_id')
        request = {
            'method': 'POST',
            'url': url,
            'cfg': {
                'json': {
                    'externalMenuId': menu_id,
                    'organizationIds': restaurants
                }
            }
        }
        response = await self.service.send_request(**request)
        if response.status != 200:
            raise errors.InteractionError(response.status, response.response_data)

        return response.response_data
