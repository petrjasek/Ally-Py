define([
    'angular',
    'jquery',
    'bootstrap'
], function(angular, $) {
    'use strict';

    angular.module('superdesk.auth.directives', []).
        directive('sdLoginModal', function($rootScope, authService) {
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
                                        authService.login(scope.username, scope.password, scope.rememberMe).
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

                    if (authService.hasIdentity()) {
                        $(element).dialog('close');
                    }
                }
            };
        });
});
