from iiko_sdk import errors, services, http_utils


class OrganizationsGateway:
    version = 'api/1'

    def __init__(self, base_url: str, service: services.BaseService):
        self.base_url = base_url
        self.service = service

    async def get_organizations(self):
        """ Получение списка организаций """
        url = http_utils.join_str(self.base_url, self.version, '/organizations')
        request = {
            'method': 'POST',
            'url': url,
            'cfg': {
                'json': {}
            }
        }
        response = await self.service.send_request(**request)
        if response.status != 200:
            raise errors.InteractionError(response.status, response.response_data)

        return response.response_data