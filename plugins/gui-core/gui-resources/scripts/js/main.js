requirejs.config
({
	baseUrl: config.content_url,
	urlArgs: "bust=" +  (new Date).getTime(),
	templatePaths: 
	{
	    'default': 'lib/core/templates/',
		'plugin': 'gui/superdesk/{plugin}/templates/'
	},
	paths: 
	{
		'jquery': config.js_url + '/jquery',
		'jqueryui': config.js_url + '/jquery/ui/',
		'dust': config.js_url + '/dust',
		'history': config.js_url + '/history',
		'tmpl': config.js_url + '/require/tmpl'
	}
});
require(['jquery/superdesk', 'lib/core/scripts/js/views/menu'], 
function(superdesk, MenuView)
{
    superdesk.navigation.init(function(){ var menuView = new MenuView; });
}); 