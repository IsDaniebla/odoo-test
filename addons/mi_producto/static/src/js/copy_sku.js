odoo.define('mi_producto.copy_sku', ['web.public.widget'], function (require) {
    "use strict";
    var publicWidget = require('web.public.widget');

    publicWidget.registry.CopySKU = publicWidget.Widget.extend({
        selector: '.btn-copy-sku',
        events: {
            'click': '_onCopyClick',
        },
        _onCopyClick: function (ev) {
            var sku = ev.currentTarget.getAttribute('data-sku');
            navigator.clipboard.writeText(sku);
            alert('SKU copiado: ' + sku);
        },
    });
});