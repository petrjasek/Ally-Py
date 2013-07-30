define(['angular', 'angular-resource'], function(angular) {
    angular.module('superdesk.menu', ['ngResource']).
        controller('NavController', ['$scope', function($scope) {
            $scope.$on('auth.login', function(event, args) {
                // TODO render menu for given user
            });
        }]);
});
