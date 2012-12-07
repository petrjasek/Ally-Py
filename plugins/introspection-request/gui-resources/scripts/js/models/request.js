define(['gizmo/superdesk'], 
function(giz)
{
    return giz.Model.extend
    ({ 
        defaults:
        {
            Get: giz.Model.extend(),
            Insert: giz.Model.extend(),
            Update: giz.Model.extend(),
            Delete: giz.Model.extend()
        }
    });
});