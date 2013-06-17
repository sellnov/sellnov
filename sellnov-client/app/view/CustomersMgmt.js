Ext.define('Sellnov.view.CustomersMgmt', {
    extend: 'Ext.Panel',
    requires: [
        'Sellnov.view.CustomersGrid'
    ],
    border: false,
    layout: 'border',
    items: [{
        region: 'center',
        xtype: 'customersgrid',
        flex: 3
    },{
        region: 'south',
        xtype: 'panel',
        flex: 1
    }]

});

