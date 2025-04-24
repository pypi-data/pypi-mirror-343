{
    "name": "Odoo customizations for Energetica Cooperator",
    "version": "16.0.3.0.0",
    "depends": [
        "base",
        "component_event",
        "cooperator",
        "cooperator_website",
        "l10n_es",
    ],
    "author": "Coopdevs Treball SCCL",
    "category": "Cooperator",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Odoo customizations for Energetica Cooperator.
    """,
    "data": [
        "views/res_company.xml",
        "views/res_partner.xml",
        "views/subscription_request.xml",
        "views/subscription_template.xml",
    ],
    "installable": True,
}
