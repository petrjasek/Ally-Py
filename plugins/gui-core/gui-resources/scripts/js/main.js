requirejs.config
({
	baseUrl: config.content_url,
	waitSeconds: 15,
    templatePaths:
	{
	    'default': config.core('')+'templates/',
		'plugin': config.gui('{plugin}/templates/')
	},
	paths: 
	{
		'jquery': config.cjs('jquery'),
		'jqueryui': config.cjs('jquery/ui'),
		'bootstrap': config.cjs('jquery/bootstrap'),
		'dust': config.cjs('dust'),
		'history': config.cjs('history'),
		'utils': config.cjs('utils'),
		'gettext': config.cjs('gettext'),
        'order': config.cjs('require/order'),
		'tmpl': config.cjs('require/tmpl'),
		'model': config.cjs('require/model'),
		'i18n': config.cjs('require/i18n'),
		'gizmo': config.cjs('gizmo'),
		'loadaloha': config.cjs('aloha-init'),
		'concat': config.cjs('concat'),		
		'newgizmo': config.cjs('newgizmo'),
        'backbone': config.cjs('backbone'),
        'codebird': config.cjs('codebird'),
        'moment': config.cjs('moment'),
        'router': config.cjs('router'),
        'vendor': config.cjs('vendor'),
        'superdesk': config.cjs('superdesk'),
        'angular': 'http://ajax.googleapis.com/ajax/libs/angularjs/1.1.5/angular',
        'angular-resource': 'http://code.angularjs.org/1.1.5/angular-resource'
	},
    shim: {
        'vendor/backbone': {
            deps: ['vendor/underscore', 'jquery'],
            exports: 'Backbone'
        },
		'vendor/codebird-js/codebird': {
			deps: ['vendor/codebird-js/sha1'],
			exports: 'Codebird'
		},
        'angular': {exports: 'angular'},
        'angular-resource': {deps: ['angular']}
    }
});

// backbone must be loaded asap because it requires underscore
// but '_' is taken later for localization
require(['concat', 'backbone'], function() {
	require([
        'angular',
        'jquery', 'jquery/superdesk', 'gizmo/superdesk/action',
        'jquery/i18n',
        'jqueryui/ext',
        'superdesk/auth',
        'superdesk/menu',
        'superdesk/dashboard'
        ],
        function(angular, $, superdesk, Action) {
            angular.module('superdesk', ['superdesk.auth', 'superdesk.menu', 'superdesk.dashboard']);
            angular.bootstrap(document, ['superdesk']);
	    }
    );
});
