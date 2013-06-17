Ext.define('Sellnov.view.Stock', {
    extend: 'Ext.grid.Panel',
    columns: [
        {text: 'Symbol', dataIndex: 'symbol' },
        {text: 'Nazwa towaru lub usługi', dataIndex: 'name', width: '40%'},
        {text: 'Rodzaj', dataIndex: 'type'},
        {text: 'J.m.', dataIndex: 'unit_name'},
        {text: 'Cena netto', dataIndex: 'price_net'},
        {text: 'Cena brutto', dataIndex: 'price__gross'}
    ],
    tbar: [
        {xtype: 'button', text: 'Nowy towar', cls: 'x-btn-add'},
    ]
        
});
