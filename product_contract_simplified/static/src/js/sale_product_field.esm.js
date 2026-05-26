/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {SaleOrderLineProductField} from "@sale/js/sale_product_field";

patch(SaleOrderLineProductField.prototype, {
    async _openContractConfigurator(isNew = false) {
        if (isNew && this.props.record.data.skip_contract_configurator) {
            // Skip configurator popup when adding a product with skip flag
            return;
        }
        return super._openContractConfigurator(...arguments);
    },
});
