# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from types import ModuleType
from typing import (
    List,
    Tuple,
    Dict,
    Union,
    Optional
)

# =============== // LIBRARY IMPORT // ===============

from loguru import logger
from jinja2 import Template
import yagmail

# =============== // MODULE IMPORT // ===============

import backend.constants as c

# =============== // EMAIL CLASS // ===============


class PrimedMail:
    def __init__(
        self,
        yag: ModuleType,
        contents: str,
        to: str
    ) -> None:
        self.yag: ModuleType = yag
        self.contents: str = contents
        self.to: str = to

    def send(
        self,
        subject: str,
        attachments: Optional[Union[str, List[str]]] = None,
        **kwargs
    ) -> Union[Dict, Tuple[List[str], str]]:
        if self.contents is None:
            _e: str = "Email does not have contents rendered"
            logger.error(_e)
            raise ValueError(_e)

        logger.debug(
            f"Sending email to {self.to} with subject {subject!r} ({len(attachments or [])} attachment(s))"
        )

        try:
            response: Union[Dict, Tuple[List[str], str]] = self.yag.send(
                to=self.to,
                subject=subject,
                contents=self.contents,
                attachments=attachments,
                **kwargs
            )
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise e
        else:
            logger.debug(
                f"Email sent to {self.to} with subject {subject!r} ({len(attachments or [])} attachment(s))"
            )
            return response
        finally:
            self.yag.close()


class Mailer:
    from_email: str = "happybread.mail@gmail.com"

    def __init__(
        self,
        /,
        to: str
    ):
        self.to: str = to
        self.yag: ModuleType = yagmail.SMTP(
            self.from_email,
            oauth2_file=str(c.MAILER_DIR / "oauth2.json")
        )

    def render(
        self,
        template: str,
        /,
        **kwargs
    ) -> PrimedMail:
        contents: str = yagmail.raw(
            Template(
                (c.TEMPLATES_DIR / f"{template}.html").read_text(encoding="utf-8")
            ).render(
                **kwargs
            ).replace(
                "\n", ""
            )
        )
        return PrimedMail(
            yag=self.yag,
            to=self.to,
            contents=contents
        )
