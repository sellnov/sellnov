Ext.define('Sellnov.store.MainMenu', {
    extend: 'Ext.data.TreeStore',
    model: 'Sellnov.model.MainMenuEntry',
    autoLoad: true,
    proxy: {
        type: 'memory',
        reader: {
            type: 'json'
        }
    },
    root: {
        expanded: true,
        text: 'Menu',
        children: [{
            id: '1',
            expanded: true,
            text: 'Sprzedaż',
            leaf: false,
            children: [{
                id: 'Sellnov.view.SaleInvoices',
                text: 'Faktury VAT sprzedaż',
                leaf: true,
                type: 'tab'
            }]
        },{
            id: 3,
            text: 'Słowniki',
            expanded: true,
            children: [{
                id: 'Sellnov.view.CustomersMgmt',
                text: 'Klienci',
                leaf: true
            },{
                id: 'Sellnov.view.Stock',
                text: 'Towary i usługi',
                leaf: true
            }]
        }]
    }
});
