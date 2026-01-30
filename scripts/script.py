import asyncio

from python_template.api.main import services
from python_template.api.services.email_service import EmailService


async def main() -> None:
    async with services:
        email_service = await services.get(EmailService)
        await email_service.send_email()


if __name__ == "__main__":
    asyncio.run(main())
