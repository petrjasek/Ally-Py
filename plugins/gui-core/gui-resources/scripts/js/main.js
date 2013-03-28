requirejs.config
({
	baseUrl: config.content_url,
	//urlArgs: "v=4",
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
		'concat': config.cjs('concat'),		
		'newgizmo': config.cjs('newgizmo')		
	}
});
require(['concat'], function(){
	require
	([
	  config.cjs('views/menu.js'), 
	  config.cjs('views/auth.js'), 
	  'jquery', 'jquery/superdesk', 'gizmo/superdesk/action', 'jquery/i18n', 'jqueryui/ext',

      config.cjs('underscore.js'),
      config.cjs('backbone.js'),
	], 
	function(MenuView, authView, $, superdesk, Action)
	{
	    $(authView).on('logout login', function(){ Action.clearCache(); });

        // initialize menu before auth because we have some events bound to auth there
        var menu = new MenuView({ el: $('#navbar-top') });

        var router = new Backbone.Router;
        router.route('', 'home', function() {
	        $.superdesk.applyLayout('layouts/dashboard', {}, function(){
                Action.initApps('modules.dashboard.*', $($.superdesk.layoutPlaceholder));
            });
	    });

	    // render auth view
        $(superdesk.layoutPlaceholder).html(authView.render().el);
	});
});
