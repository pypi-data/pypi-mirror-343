import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class UserKeycloakListener(Component):
    _name = "user.keycloak.listener"
    _inherit = "base.event.listener"
    _apply_on = ["res.users"]

    def on_record_create(self, record, fields=None):
        _logger.debug("Check if is needed create a user in Keycloak...")
        if self.env.company.keycloak_connector_enabled:
            _logger.debug(f"Creating user in Keycloak...{record.partner_id}")
            record.partner_id.with_delay().create_keycloak_user()
