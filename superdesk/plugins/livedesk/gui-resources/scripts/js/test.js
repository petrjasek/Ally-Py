define(['gizmo', 'gui/superdesk/livedesk/scripts/js/models/collaborator'], 
function(giz, Collaborator)
{
    return {init: function(){
        
    console.clear();
    //giz.Model.options.x = 'y';
    //console.dir('-----', giz.Model.options);
    var c = new Collaborator('http://localhost:8080/resources/Superdesk/Collaborator/1');
    //c.options.ceva = 'altceva';
    //console.dir('-----', c.options);
    //console.dir('-----', giz.Model.options);
    
    c.xfilter('Id', 'Name').sync().done(function()
    {
        console.log('a');
    });
    setTimeout(function(){ c.sync(); }, 10000);
    
    $(c).triggerHandler('relationHash');
    
    
        /*var Source = Model.extend(),
    Collaborator = Model.extend({ defaults:{ Post: CollaboratorPost }}),
    Post = Model.extend({ defaults:{ Author: Collaborator }}),
    CollaboratorPost = new Collection({ model: Post }),
    Collaborator = Model.extend
    ({ 
        defaults: { Post: CollaboratorPost, Source: Source } 
    });
    
var p = new Post('http://localhost:8080/resources/Superdesk/Post/1'); 
    console.log(p.sync().done(function(){console.log(p)}))
    */
    
    }};
});