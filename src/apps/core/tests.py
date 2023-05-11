from cerberus import Validator
from rest_framework.test import APITestCase


class BaseAPITestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def check_response_schema(self, schema, response):
        validator = Validator(schema)
        is_valid = validator.validate(response)
        if not is_valid:
            print(f'Validator Error:{validator.errors}')
        self.assert_(validator.validate(response))

    def tearDown(self) -> None:
        super(BaseAPITestCase, self).tearDown()
