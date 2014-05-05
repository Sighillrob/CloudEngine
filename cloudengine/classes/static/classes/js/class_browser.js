

var classBrowserApp = angular.module('classBrowserApp', []);


classBrowserApp.controller('classListCtrl', function classListCtrl($scope) {
	
	update_apps_list($scope);
	
	$scope.selectedApp = "Select an App";
	
})