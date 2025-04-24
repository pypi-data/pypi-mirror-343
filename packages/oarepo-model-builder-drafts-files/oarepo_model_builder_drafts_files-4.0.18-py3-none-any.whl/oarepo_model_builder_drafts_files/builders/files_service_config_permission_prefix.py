from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class FilesServiceConfigPermissionPrefixBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "files_service_config_permission_prefix"
    section = "service-config"
    template = "draft-service-config-permission-prefix"
