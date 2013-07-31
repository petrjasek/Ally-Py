define([
    'angular',
    'superdesk/auth/directives',
    'superdesk/auth/services'
], function(angular) {
    'use strict';

    angular.module('superdesk.auth', ['superdesk.auth.directives', 'superdesk.auth.services']).
        config(function($routeProvider) {
            $routeProvider.
                when('/desks', {
                    template: '<h1>desks</h1>',
                    controller: function($scope) {
                    }
                }).
                when('/:plugin', {
                    template: '<div ng-include="templateUrl">Loading..</div>',
                    controller: function($scope, $route, $routeParams) {
                        console.log('in', $route, $routeParams);
                    }
                });
        }).
        run(function($rootScope, $route, authService) {
            $rootScope.$on('$locationChangeStart', function(event) {
                if (!authService.hasIdentity()) {
                    event.preventDefault();
                    $rootScope.$broadcast('auth.doLogin');
                }
            });

            $rootScope.$on('auth.login', function() {
                $route.reload();
            });
        });
});
