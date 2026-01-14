
import import_declare_test

from splunktaucclib.rest_handler.endpoint import (
    field,
    validator,
    RestModel,
    DataInputModel,
)
from splunktaucclib.rest_handler import admin_external, util
from splunktaucclib.rest_handler.admin_external import AdminExternalHandler
import logging

util.remove_http_proxy_env_vars()


special_fields = [
    field.RestField(
        'name',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.AllOf(
            validator.Pattern(
                regex=r"""^[a-zA-Z\w-]*$""", 
            ), 
            validator.String(
                max_len=100, 
                min_len=1, 
            )
        )
    )
]

fields = [
    field.RestField(
        'index',
        required=True,
        encrypted=False,
        default='default',
        validator=validator.String(
            max_len=80, 
            min_len=1, 
        )
    ), 
    field.RestField(
        'sourcetype',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.AllOf(
            validator.Pattern(
                regex=r"""^[a-zA-Z\w-]*$""", 
            ), 
            validator.String(
                max_len=100, 
                min_len=1, 
            )
        )
    ), 
    field.RestField(
        'Server_IP',
        required=True,
        encrypted=False,
        default='0.0.0.0',
        validator=validator.String(
            max_len=15, 
            min_len=7, 
        )
    ), 
    field.RestField(
        'Server_Port',
        required=True,
        encrypted=False,
        default='1337',
        validator=validator.String(
            max_len=5, 
            min_len=2, 
        )
    ), 
    field.RestField(
        'Policy_Name',
        required=True,
        encrypted=False,
        default=None,
        validator=validator.AllOf(
            validator.Pattern(
                regex=r"""^[a-zA-Z\w-]*$""", 
            ), 
            validator.String(
                max_len=30, 
                min_len=1, 
            )
        )
    ), 
    field.RestField(
        'use_ssl',
        required=False,
        encrypted=False,
        default=False,
        validator=None
    ), 
    field.RestField(
        'sa_cert',
        required=False,
        encrypted=False,
        default='empty',
        validator=None
    ), 
    field.RestField(
        'sa_key',
        required=False,
        encrypted=False,
        default='empty',
        validator=None
    ), 

    field.RestField(
        'disabled',
        required=False,
        validator=None
    )

]
model = RestModel(fields, name=None, special_fields=special_fields)



endpoint = DataInputModel(
    'server_input',
    model,
)


if __name__ == '__main__':
    logging.getLogger().addHandler(logging.NullHandler())
    admin_external.handle(
        endpoint,
        handler=AdminExternalHandler,
    )
