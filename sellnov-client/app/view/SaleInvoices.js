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
    tbar: [{
        xtype: 'button', 
        text: 'Nowa faktura VAT', 
        cls: 'x-icon-add', 
        listeners: {
            click: function() {
                var win = Ext.create('Ext.window.Window', {
                    title: 'Nowa faktura VAT sprzedaż',
                    items: Ext.create('Sellnov.view.SaleInvoice'),
                    layout: 'fit',
                    width: 800,
                    height: 500,
                    maximized: true,
                    maximizable: true,
                    padding: '5 5 5 5',
                    modal: true
                });
                win.show();
            }
        }
    }]
});
