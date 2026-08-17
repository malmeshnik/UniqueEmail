from odoo import api, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Extension of res.partner model to enforce unique email address constraints."""

    _inherit = "res.partner"

    @api.constrains("email")
    def _check_unique_email(self):
        """Verify that the entered email address is unique across active partner records.

        Raises:
            ValidationError: If another partner record already exists with the same email.
        """
        for partner in self:
            if not partner.email:
                continue

            clean_email = partner.email.strip().lower()
            domain = [
                ("id", "!=", partner.id),
                ("email", "=ilike", clean_email),
            ]

            duplicate_partner = self.search(domain, limit=1)
            if duplicate_partner:
                raise ValidationError(
                    f"The email address '{partner.email}' is already used "
                    f"by contact '{duplicate_partner.name}' (ID: {duplicate_partner.id})."
                )