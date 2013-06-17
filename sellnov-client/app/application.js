Ext.define('Sellnov.Application', {
    name: 'Sellnov',

    extend: 'Ext.app.Application',

    views: [
        'CustomersMgmt'
    ],

    controllers: [
        // TODO: add controllers here
    ],
    models: [
        'MainMenuEntry'
    ],
    stores: [
        'MainMenu'
    ]
});
