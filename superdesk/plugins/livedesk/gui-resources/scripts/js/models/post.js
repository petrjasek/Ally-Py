define(['gizmo/superdesk', 
/*        'livedesk/models/collaborator',
        'livedesk/models/blog',
        'livedesk/models/user',
        'livedesk/models/posttype'
*/
], 
function(Gizmo)
{
	return Gizmo.AuthModel.extend({
		url: new Gizmo.Url('/Post')
	}, { register: 'Post' } );
	/*
    return Gizmo.AuthModel.extend
    ({ 
		url: new Gizmo.Url('/Post'),
		defaults:
        { 
            Author: Collaborator,
            Blog: Blog,
            Creator: User,
            PostType: PostType
        }
    }, { register: 'Post' } );*/
});