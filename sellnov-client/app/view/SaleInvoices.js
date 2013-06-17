Ext.define('Sellnov.view.SaleInvoices', {
    extend: 'Ext.grid.Panel',
    columns: [
        {text: 'Numer', dataIndex: 'number_fmt' },
        {text: 'Data sprzedaży', dataIndex: 'sale_date'},
        {text: 'Data wystawienia', dataIndex: 'issue_date'},
        {text: 'Wartość netto', dataIndex: 'total_net'},
        {text: 'Wartość brutto', dataIndex: 'total_gross'},
        {text: 'Płatność', dataIndex: 'payment_name'},
    ],
    tbar: [
        {xtype: 'button', text: 'Nowa faktura VAT', cls: 'x-btn-add'},
    ]
        
});
