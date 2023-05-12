from apps.core.tests import generate_list_schema_validator

chef_list_schema = generate_list_schema_validator({
    'user_info': {'type': 'string', "required": True},
    'city': {'type': 'string', "required": True},
    'rating': {'type': 'float', "required": True},
    'tasties': {'type': 'integer', "required": True},
})
