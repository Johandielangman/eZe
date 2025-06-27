# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // MODULE IMPORT // ===============

from backend.modules.mailer import Mailer


# =============== // TEST // ===============

def test_mailer() -> None:
    to_email: str = "jghanekom2@gmail.com"
    to_emails, contents = Mailer(
        to_email
    ).render(
        "default"
    ).send(
        subject="Good night!",
        preview_only=True
    )

    assert to_email in to_emails
