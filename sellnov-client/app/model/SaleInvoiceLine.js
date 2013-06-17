Ext.define('Sellnov.model.SaleInvoiceLine', {
    extend: 'Ext.data.Model',
    fields: ['id', 'name','price_net','price_gross','unit_name', 'unit', 'total_net', 'total_gross', 'quantity']
});
