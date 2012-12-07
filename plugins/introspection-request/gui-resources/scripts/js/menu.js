define(['jquery','jquery/superdesk','jquery/rest'], function ($, superdesk)
{
    return { 
        init: function()
        { 
            superdesk.getActions('modules.request.*')
            .done(function(actions)
            {
                $(actions).each(function()
                {
                    if(this.Path == 'modules.request.list' && this.ScriptPath)
                        require([superdesk.apiUrl+this.ScriptPath], function(ListApp){ listApp = new ListApp(); });
                });
            });
        }
    };
});