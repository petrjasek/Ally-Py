define([
    'utils/sha512',
    'angular',
    'angular-resource'
], function(jsSHA, angular) {
    'use strict';

    var TOKEN_KEY = 'superdesk.login.session';

    angular.module('superdesk.auth.services', ['ngResource']).
        factory('Session', function($resource) {
            return $resource('/resources/Security/Authentication', {}, {
                save: {method: 'POST'}
            });
        }).
        factory('Login', function($resource) {
            return $resource('/resources/Security/Authentication/Login');
        }).
        service('authService', function($rootScope, $http, $route, $q, Session, Login) {
            window.authService = this; // publish service
            var self = this;

            var getHashedToken = function(username, password, loginToken) {
                var shaPassword = new jsSHA(password, "ASCII");
                var shaStep1 = new jsSHA(shaPassword.getHash("SHA-512", "HEX"), "ASCII");
                var shaStep2 = new jsSHA(loginToken, "ASCII");
                var HashedToken = shaStep1.getHMAC(username, "ASCII", "SHA-512", "HEX");
                return shaStep2.getHMAC(HashedToken, "ASCII", "SHA-512", "HEX");
            };

            this.auth = function(username, password, rememberMe) {
                var delay = $q.defer();

                if (!username || !password) {
                    delay.reject();
                    return delay.promise;
                }

                Session.save({userName: username}, function(session) {
                    Login.save({
                        UserName: username,
                        Token: session.Token,
                        HashedToken: getHashedToken(username, password, session.Token)
                    }, function(login) {
                        self.setToken(login.Session, rememberMe);
                        $http.defaults.headers.common['Authorization'] = login.Session;
                        $rootScope.$broadcast('auth.login', login);
                        $route.reload();
                        delay.resolve(login.Session);
                    }, function(response) {
                        delay.reject(response);
                    });
                });

                return delay.promise;
            };

            this.setToken = function(token, useLocalStorage) {
                sessionStorage.setItem(TOKEN_KEY, token);
                if (useLocalStorage) {
                    localStorage.setItem(TOKEN_KEY, token);
                } else {
                    localStorage.setItem(TOKEN_KEY, '');
                }
            };

            this.getToken = function() {
                return sessionStorage.getItem(TOKEN_KEY)
                    ? sessionStorage.getItem(TOKEN_KEY)
                    : localStorage.getItem(TOKEN_KEY);
            };

            this.hasToken = function() {
                return !!this.getToken();
            };

            this.removeToken = function() {
                this.setToken('');
            };
        });
});
