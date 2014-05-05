



var pushMsgApp = angular.module('pushMsgApp', []);


pushMsgApp.controller('pushMsgCtrl', function pushMsgCtrl($scope) {
	
	update_apps_list($scope);
	
	$scope.selectedApp = "Select an App";
	
})