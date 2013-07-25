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
        'angular': 'http://ajax.googleapis.com/ajax/libs/angularjs/1.0.7/angular',
        'angular-resource': 'http://code.angularjs.org/1.0.7/angular-resource'
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
        config.cjs('views/menu.js'), 
        config.cjs('views/auth.js'), 
        'jquery', 'jquery/superdesk', 'gizmo/superdesk/action',
        'router',
        'jquery/i18n',
        'jqueryui/ext',
        'superdesk/auth'
        ],
        function(angular, MenuView, authView, $, superdesk, Action, router) {

            angular.module('superdesk', ['superdesk.auth']);
            angular.bootstrap(document, ['superdesk']);

	        $(authView).on('logout login', function() { Action.clearCache(); });

            // initialize menu before auth because we have some events bound to auth there
            var menu = new MenuView({ el: $('#navbar-top') });

	        // render auth view
            $(superdesk.layoutPlaceholder).html(authView.render().el);

            router.route('', 'home', function() {
	            $.superdesk.applyLayout('layouts/dashboard', {}, function() {
                    Action.initApps('modules.dashboard.*', $($.superdesk.layoutPlaceholder));
                });
            });
	    }
    );
});
