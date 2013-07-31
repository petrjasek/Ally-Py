define([
    'utils/sha512',
    'angular',
    'angular-resource'
], function(jsSHA, angular) {
    'use strict';

    var AUTH_NS = 'superdesk.auth';

    var SessionData = function(data) {
        this.token = data ? data.Token: null;
        this.user = data ? data.User : {
            Id: null,
            Name: 'Anonymous'
        };
    };

    angular.module('superdesk.auth.services', ['ngResource']).
        factory('Session', function($resource) {
            return $resource('/resources/Security/Authentication', {}, {
                save: {method: 'POST'}
            });
        }).
        factory('Login', function($resource) {
            return $resource('/resources/Security/Authentication/Login', {}, {
                'save': {method: 'POST', params: {'X-Filter': 'User.*'}}
            });
        }).
        service('authService', function($rootScope, $http, $q, Session, Login) {
            window.authService = this; // publish service

            // remember me func - if we have auth data in localStorage copy it to sessionStorage
            if (localStorage.getItem(AUTH_NS)) {
                sessionStorage.setItem(AUTH_NS, localStorage.getItem(AUTH_NS));
            }

            // init session
            this.sessionData = sessionStorage.getItem(AUTH_NS)
                ? angular.fromJson(sessionStorage.getItem(AUTH_NS))
                : new SessionData();
            $rootScope.currentUser = this.sessionData.user;

            var getHashedToken = function(username, password, loginToken) {
                var shaPassword = new jsSHA(password, "ASCII");
                var shaStep1 = new jsSHA(shaPassword.getHash("SHA-512", "HEX"), "ASCII");
                var shaStep2 = new jsSHA(loginToken, "ASCII");
                var HashedToken = shaStep1.getHMAC(username, "ASCII", "SHA-512", "HEX");
                return shaStep2.getHMAC(HashedToken, "ASCII", "SHA-512", "HEX");
            };

            /**
             * Login
             *
             * @param {string} username
             * @param {string} password
             * @param {boolean} rememberMe
             */
            this.login = function(username, password, rememberMe) {
                var delay = $q.defer();

                if (!username || !password) {
                    delay.reject();
                    return delay.promise;
                }

                var self = this;
                Session.save({userName: username}, function(session) {
                    Login.save({
                        UserName: username,
                        Token: session.Token,
                        HashedToken: getHashedToken(username, password, session.Token)
                    }, function(login) {
                        self.setSessionData(login, rememberMe);
                        $rootScope.$broadcast('auth.login', login);
                        delay.resolve(login.Session);
                    }, function(response) {
                        delay.reject(response);
                    });
                });

                return delay.promise;
            };

            /**
             * Logout
             */
            this.logout = function() {
                this.setSessionData();
                sessionStorage.removeItem(AUTH_NS);
                localStorage.removeItem(AUTH_NS);
            };

            this.setSessionData = function(data, useLocalStorage) {
                this.sessionData = new SessionData(data);
                $rootScope.currentUser = this.sessionData.user;
                $http.defaults.headers.common['Authorization'] = this.sessionData.token;

                sessionStorage.setItem(AUTH_NS, angular.toJson(this.sessionData));
                if (useLocalStorage) {
                    localStorage.setItem(AUTH_NS, sessionStorage.getItem(AUTH_NS));
                } else {
                    localStorage.removeItem(AUTH_NS);
                }
            };

            /**
             * Test if user is authenticated
             *
             * @return {boolean}
             */
            this.hasIdentity = function() {
                return !!this.sessionData.user.Id;
            };
        });
});
