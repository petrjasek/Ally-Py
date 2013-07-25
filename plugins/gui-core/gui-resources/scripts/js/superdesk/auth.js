define(['angular'], function(angular) {
    'use strict';
    
    var TOKEN_KEY = 'superdesk.login.session';
    
    angular.module('superdesk.auth', []).
        service('tokenService', function($rootScope) {
            window.tokenService = this; // publish service
            this.storage = localStorage;
            
            this.setToken = function(token) {
                this.storage.setItem(TOKEN_KEY, token);
            };
            
            this.getToken = function() {
                return this.storage.getItem(TOKEN_KEY);
            };
            
            this.removeToken = function() {
                this.setToken(null);
            };
        }).
        run(function($http, tokenService) {
            $http.defaults.headers.common['Authorization'] = tokenService.getToken();
        });
});