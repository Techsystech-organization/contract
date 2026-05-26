{
    "name": "Product Contract Simplified",
    "summary": "Mutually exclusive contract template vs product-driven contract config, optional configurator skip",
    "version": "18.0.1.0.0",
    "category": "Contract Management",
    "author": "Techsystech",
    "license": "AGPL-3",
    "depends": ["product_contract"],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "product_contract_simplified/static/src/js/sale_product_field.esm.js",
        ],
    },
    "installable": True,
    "auto_install": False,
}
