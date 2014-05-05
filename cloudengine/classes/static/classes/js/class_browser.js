
$app_object = null;
$curr_class = null;
$selected_objects = [];
$curr_page = 0;
$page_length = 10; /* todo: this has to be same as server */


var classBrowserApp = angular.module('classBrowserApp', []);


classBrowserApp.controller('classListCtrl', function classListCtrl($scope) {
	
	
	if($curr_app == null){
		$scope.selectedApp = "Select an App";
	}
	else{
		$scope.selectedApp = $curr_app;
	}
	
	
	  $scope.currAppObject = null;
	  $scope.id_field = null;
	  $scope.selectedClass = "";
	  $scope.classes = [];
	  $scope.object_fields = null;
	  $scope.obj_list = [];
	  $scope.prev_page = $scope.next_page = null;
	  $scope.apps = [];
	  
	  
	  update_apps_list($scope);
	  
	  

	  $scope.selectApp = function(app){
		  
		  $scope.id_field = "";
		  
//		  //$store.set("session_app", app);
		  
		  /* disable the class delete button when a new app is selected */
		  $scope.selectedClass = "";
		  $selected_objects = [];

		  
		  $scope.object_fields = null;
		  $scope.selectedApp = app;
		  $scope.classes = [];
		  $scope.obj_list = [];
		  myspinner.spin($("#spinner")[0]);
		  
		  var apps = $scope.apps;
		  
		  for(index in apps){
			var cur_app = apps[index];
			if( cur_app.name == app){
				$app_object = cur_app;
				break;
			}
		  }
		  
		  $scope.currAppObject = $app_object;
		  
		  $.ajax({
		         url: "/api/v1/classes/",
		         type: "GET",
		         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $app_object.key);},
		         success: function(data) {
		        	myspinner.stop();
		        	classlist = data["result"];
				  	$scope.$apply(function(){
				  		console.log(classlist);
					  	$scope.classes = classlist;
					  	if($klass!=null){
							  $scope.selectClass($klass, 0);
						  }
				    }); 
				  	
				  },
				  
				  error: function(xhr, status, err){
					  
					  myspinner.stop();
					  alert("Unable to complete operation. Server Error!");
				  }
		      });
		  
		  
	  };
	  
	  
	  $scope.selectClass = function(cls, index){
		  $scope.selectedClass = cls;
		  $curr_class = cls;
		  cls.selected = true;
		  $scope.obj_list = [];
		  $selected_objects = [];
		  
		  
		  myspinner.spin($("#spinner")[0]);
		  
		  all_rows = $('#classes-table').find('tr');
		  for(i=0; i<all_rows.length; i++){
			  row = all_rows[i];
			  row.className = row.className.replace("checked", "");
		  }
		  
		  row = all_rows[index + 1];
		  if(row != undefined){
			  if(row.className.indexOf("checked") == -1){
				  row.className += " checked";
			  }
			  else{
				  row.className = row.className.replace("checked", "");
			  }  
		  }
		  
		  
		  
	  }
	  
	  
	
})















