Ext.define('Sellnov.view.CustomersGrid', {
    extend: 'Ext.grid.Panel',
    alias: 'widget.customersgrid',
    columns: [
        {text: 'Nazwa', dataIndex: 'name', width: '40%'},
        {text: 'Adres', dataIndex: 'address'},
        {text: 'Telefon', dataIndex: 'phone'},
        {text: 'E-mail', dataIndex: 'email', width: '20%'},
        {text: 'NIP', dataIndex: 'nip'}
    ],
    tbar: [
        {xtype: 'button', text: 'Nowy', cls: 'x-btn-add'},
    ]
        
});
