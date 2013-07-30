define([
    'angular',
    'jquery',
    'utils/sha512',
    'bootstrap',
    'angular-resource'
], function(angular, $, jsSHA) {
    'use strict';

    var TOKEN_KEY = 'superdesk.login.session';

    angular.module('superdesk.auth', ['ngResource']).
        factory('Session', function($resource) {
            return $resource('/resources/Security/Authentication', {}, {
                save: {method: 'POST'}
            });
        }).
        factory('Login', function($resource) {
            return $resource('/resources/Security/Authentication/Login');
        }).
        service('tokenService', function($rootScope, $http, $route, $q, Session, Login) {
            window.tokenService = this; // publish service
            this.storage = localStorage;
            var self = this;

            var getHashedToken = function(username, password, loginToken) {
                var shaPassword = new jsSHA(password, "ASCII");
                var shaStep1 = new jsSHA(shaPassword.getHash("SHA-512", "HEX"), "ASCII");
                var shaStep2 = new jsSHA(loginToken, "ASCII");
                var HashedToken = shaStep1.getHMAC(username, "ASCII", "SHA-512", "HEX");
                return shaStep2.getHMAC(HashedToken, "ASCII", "SHA-512", "HEX");
            };

            this.auth = function(username, password) {
                var delay = $q.defer();
                Session.save({userName: username}, function(session) {
                    Login.save({
                        UserName: username,
                        Token: session.Token,
                        HashedToken: getHashedToken(username, password, session.Token)
                    }, function(login) {
                        self.setToken(login.Session);
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

            this.setToken = function(token) {
                this.storage.setItem(TOKEN_KEY, token);
            };

            this.removeToken = function() {
                this.setToken(null);
            };

            this.hasToken = function() {
                return !!this.storage.getItem(TOKEN_KEY);
            };
        }).
        directive('sdLoginModal', function($rootScope, tokenService) {
            return {
                restrict: 'A',
                templateUrl: '/content/lib/core/templates/login.html',
                link: function(scope, element, attrs) {
                    $(element).dialog({
                        draggable: false,
                        resizable: false,
                        modal: true,
                        width: "40.1709%",
                        buttons: [
                            {
                                text: 'Login',
                                class: 'btn btn-primary',
                                click: function() {
                                    scope.$apply(function() {
                                        tokenService.auth(scope.username, scope.password).
                                            then(function() {
                                                scope.loginError = false;
                                                $(element).dialog('close');
                                            }, function() {
                                                scope.loginError = true;
                                            });
                                    });
                                }
                            }
                        ]
                    });

                    $rootScope.$on('auth.doLogin', function(event) {
                        $(element).dialog('open');
                    });

                    if (tokenService.hasToken()) {
                        $(element).dialog('close');
                    }
                }
            };
        }).
        config(function($routeProvider) {
            $routeProvider.
                when('/auth', {
                    template: '<h1>hello {{name}}</h1>',
                    controller: function($scope) {
                        $scope.name = 'world';
                    }
                });
        }).
        run(function($rootScope, tokenService) {
            $rootScope.$on('$locationChangeStart', function(event) {
                if (!tokenService.hasToken()) {
                    event.preventDefault();
                    $rootScope.$broadcast('auth.doLogin');
                }
            });
        });
});
