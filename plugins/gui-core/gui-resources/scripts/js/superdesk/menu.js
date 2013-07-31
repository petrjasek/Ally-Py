define(['angular', 'superdesk/auth/services'], function(angular) {
    angular.module('superdesk.menu', ['superdesk.auth.services']).
        controller('NavController', ['$scope', 'authService', function($scope, authService) {
            $scope.templateUrl = '/content/lib/core/templates/navbar.html';
            $scope.logout = function() {
                authService.logout();
            };
        }]);
});
