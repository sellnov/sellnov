Ext.define('Sellnov.view.SaleInvoice', {
    extend: 'Ext.Panel',
    layout: 'border',
    border: false,
    tbar: [
        {xtype: 'button', text: 'Zapisz'},
        {xtype: 'button', text: 'Drukuj'},
        {xtype: 'button', text: 'Zamknij', listeners: {click: function() { this.up('window').close(); }}}
    ],
    items: [{
        region: 'north',
        xtype: 'panel',
        layout: 'border',
        flex: 1,
        margin: '5 5 5 5',
        defaults: {
            border: false
        },
        items: [{
            xtype: 'panel',
            region: 'west',
            flex: 2,
            items: [{
                xtype: 'combo',
                margin: '10 5 5 5',
                fieldLabel: 'Klient',
            }]
        },{
            xtype: 'panel',
            region: 'center',
            flex: 1,
            style: {
                'text-align': 'center'
            },
            html: '<h2>Faktura VAT'
        },{
            xtype: 'panel',
            region: 'east',
            flex: 2,
            align: 'right',
            layout: 'vbox',
            pack: 'end',
            defaults: {
                pack: 'end',
            },
            items: [{
                margin: '10 0 5 0',
                xtype: 'datefield',
                fieldLabel: 'Data wystawienia'
            },{
                xtype: 'datefield',
                fieldLabel: 'Data sprzedaży'
            }]
        }]
    },{
        region: 'center',
        xtype: 'grid',
        title: 'Towary i usługi',
        margin: '5 5 5 5',
        flex: 3,
        columns: [
            {text: 'Nazwa towaru lub usługi', dataIndex: 'name', width: '40%', field: {type: 'combo'}},
            {text: 'J.m.', dataIndex: 'unit_name', field: {type: 'combo'}},
            {text: 'Cena netto', dataIndex: 'price_net', field: {type: 'numberfield'}},
            {text: 'VAT', dataIndex: 'tax_rate'},
            {text: 'Cena brutto', dataIndex: 'price_gross'},
            {text: 'Ilość', dataIndex: 'quantity', field: {type: 'numberfield'}},
            {text: 'Wartość netto', dataIndex: 'total_net', summaryType: 'sum'},
            {text: 'Wartość brutto', dataIndex: 'total_gross', summaryType: 'sum'},
        ],
        tbar: [{
            xtype: 'button', 
            text: 'Dodaj wiersz',
            listeners: {
                click: function() {
                    var rec = Ext.create('Sellnov.model.SaleInvoiceLine');
                    var grid = this.up('grid');
                    var editing = grid.plugins[0];
                    grid.store.insert(0,rec);
                    editing.startEditByPosition({row: 0, column: 0});
                }
            }
        }],
        plugins: [Ext.create('Ext.grid.plugin.CellEditing')],
        features: [{
            ftype: 'summary'
        }],
        listeners: {
            edit: function(editor, e) {
                var record = e.record;
                record.set('tax_rate', record.get('tax_rate') || 23);
                record.set('price_gross', record.get('price_net') * (1+record.get('tax_rate')/100.0));
                record.set('total_net', record.get('price_net') * record.get('quantity'));
                record.set('total_gross', record.get('total_net') * (1+record.get('tax_rate')/100.0));
                record.commit();
            }
        }
   }]
});

