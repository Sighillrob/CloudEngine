



var filesBrowserApp = angular.module('filesBrowserApp', []);


filesBrowserApp.controller('fileListCtrl', function fileListCtrl($scope) {
	
	update_apps_list($scope);
	
	$scope.selectedApp = "Select an App";
	
})