from api.application_settings import ApplicationSettings
from api.workflows.products.publish_product.publish_product_workflow import (
    PublishProductWorkflow,
)


class DependencyContainer:
    @classmethod
    def initialize(cls) -> None:
        cls.initialize_application_settings()

    @classmethod
    def initialize_application_settings(cls) -> None:
        cls.application_settings = ApplicationSettings()  # type: ignore[reportCallIssue]

    @classmethod
    def get_application_settings(cls) -> ApplicationSettings:
        return cls.application_settings

    @classmethod
    def get_publish_product_workflow(cls) -> PublishProductWorkflow:
        return PublishProductWorkflow()
