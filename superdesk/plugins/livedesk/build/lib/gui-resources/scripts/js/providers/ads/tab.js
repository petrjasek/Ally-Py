define('providers/ads/tab', ['providers'], 
function(providers) 
{
    providers.ads = 
    {
        className: 'big-icon-ads',       
        init: function() 
        {
            var args = arguments;
            require(['providers','providers/ads'], 
                function(providers){ providers.ads.init.apply(providers.ads, args); });
        }
    };
    return providers;
});