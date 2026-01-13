import asyncio

from python_template.api.main import services
from python_template.api.services.email_service import EmailService


async def main() -> None:
    async with services.build_service_provider() as service_provider:
        email_service = await service_provider.get_required_service(EmailService)
        await email_service.send_email()


if __name__ == "__main__":
    asyncio.run(main())
