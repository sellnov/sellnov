Ext.define('Sellnov.view.Main', {
    extend: 'Ext.container.Container',
    requires:[
        'Ext.tab.Panel',
        'Sellnov.store.MainMenu',
        'Ext.layout.container.Border'
    ],
    
    xtype: 'app-main',

    layout: {
        type: 'border'
    },

    items: [{
        region: 'west',
        xtype: 'treepanel',
        title: 'Sellnov &copy; 2013 NTSmedia',
        rootVisible: false,
        width: '20%',
        store: 'MainMenu',
        listeners: {
            itemdblclick: function(tree,record) {
                Ext.require(record.get('id'));
                var el = Ext.create(record.get('id'));
                var type = record.get('type') || 'tab';

                if(type=='tab') {
                    var tabs = Ext.getCmp('maintabs');
                    var tabId = record.get('id');
                    var tabExists = false;
                    var tab = null;

                    for(var i=0;i<tabs.items.length;i++) {
                        if(tabs.items.getAt(i).id == tabId) {
                            tab = tabs.items.getAt(i);
                            break;
                        }
                    }
                    if(tab==null) {
                        tab = Ext.getCmp('maintabs').add({
                            closable: true,
                            layout: 'fit',
                            id: tabId,
                            title: record.get('text'),
                            items: el
                        });
                    }
                    tab.show();
                } else {
                    var win = Ext.create('Ext.window.Window', {
                        width: 800,
                        height: 500,
                        title: record.get('text'),
                        layout: 'fit',
                        modal: true,
                        items: el
                    });
                    win.show();
                }
            }
        }
    },{
        region: 'center',
        xtype: 'tabpanel',
        id: 'maintabs',
        items:[]
    }]
});
