{
    "name": "Contract Default Commission",
    "summary": "Set default commission for contract lines",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "Techsystech",
    "depends": ["contract", "account", "commission_oca", "account_commission_oca"],
    "data": [
        "security/ir.model.access.csv",
        "views/contract_views.xml",
    ],
    "installable": True,
    "application": False,
}
