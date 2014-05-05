
$app_object = null;
$curr_class = null;
$selected_objects = [];
$curr_page = 0;
$page_length = 10; /* todo: this has to be same as server */


$.ready(function(){		
	
	$("#btn-file-upload").click(function(){
		if($app_object == null){
			alert("Please select an app first");
			return false;
		}
	});
	
	$("#btn-file-download").click(function(){
		if($app_object == null){
			alert("Please select an app first");
			return false;
		}
		if($curr_class == null){
			alert("Please select a class first");
			return false;
		}
	});
		
}());


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
		  /* disable the class delete button when a new app is selected */
		  var del_btn = $('#delete-class')[0];
		  var is_disabled = del_btn.className.indexOf("disabled");
		  if(is_disabled == -1){
			  del_btn.className += " disabled";
		  }
		  
		  var del_btn = $('#delete-objects')[0];
		  var is_disabled = del_btn.className.indexOf("disabled");
		  if(is_disabled == -1){
			  del_btn.className += " disabled";
		  }
		  
		  
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
		         url: "/api/v2/classes/",
		         type: "GET",
		         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $app_object.key);},
		         success: function(data) {
		        	myspinner.stop();
		        	classlist = data["results"];
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
		  
		  
		  /* Get Class Schema */
		  $.ajax({
		         url: "/api/v2/classes/schema/" + cls + "/",
		         type: "GET",
		         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $scope.currAppObject.key);},
		         success: function(data){
		        	
		        	 $scope.$apply(function(){
		        		 $scope.schema = data;	 
		        	 });
		         }
		         
		  });
		  
		  /* enable class delete button */
		  var del_btn = $('#delete-class')[0];
		  del_btn.className = del_btn.className.replace("disabled", "");
		  
		  /* disable objects delete button */
		  var del_btn = $('#delete-objects')[0];
		  var is_disabled = del_btn.className.indexOf("disabled");
		  if(is_disabled == -1){
			  del_btn.className += " disabled";
		  }
		  
		  
		  
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
		  
		  
		  
		  $.ajax({
		         url: "/api/v2/classes/" + cls + "/",
		         type: "GET",
		         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $scope.currAppObject.key);},
		         success: function(data) { 
		        	obj_list = data["results"];
		        	$scope.count = data["count"];
		        	
		        	myspinner.stop();
		        	
		        	///////////////
		        		$scope.object_fields = [] 
			  		  var fields = {}
			  		  for(index in obj_list){
			  			 obj = obj_list[index]
			  			 for(f in obj){
			  				 fields[f] = 1;
			  			 }
			  		  }
			  		 
		        		$scope.id_field = "_id";
		        		$scope.$apply(function(){
		        			
		        			delete fields["_id"];
		        			
		        			for(var field in fields){
		  		  			  $scope.object_fields.push(field);
		  		  		  }
		  		  		  $scope.obj_list = obj_list;
		  		  		  $scope.prev_page = data["previous"];
		  		  		  $scope.next_page = data["next"];
		  		  		  
					    });	       
		        		
		        		$("#btn-paginator").show();
		        		
		        		$scope.show_page_message();	        		
		        		
		         },
		         error: function(xhr, status, err){
					  
					  myspinner.stop();
					  alert("Unable to complete operation. Server Error!");
				  }
		      });
		  
	  }
	  
	  
	  $scope.show_page_message = function(){
		  
		  var $start = $end = 0; 
		  if($scope.prev_page == null){
			  $start = 1;
			  $end = $scope.obj_list.length;
		  }
		  else{
			  var match = $scope.prev_page.match(/\d+/);
			  var prev = match[0];
			  $start  = eval(prev) * $page_length + 1;
			  $end = $start + $scope.obj_list.length - 1;
		  }
		  
		  var msg = "Showing result " + $start.toString() + " to " + $end.toString() + " of " + $scope.count; 
		  $("#page-info").text(msg);
		  
	  }
	  
	  
	  $scope.previousPage = function(){
		  
		  if($scope.prev_page != null){
			  
			  myspinner.spin($("#spinner")[0]);
			  
			  $.ajax({
			         url: "/api/v2/classes/" + $scope.selectedClass + "/" + $scope.prev_page,
			         type: "GET",
			         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $scope.currAppObject.key);},
			         success: function(data) { 
			        	obj_list = data["results"];
			        	myspinner.stop();
			        	
			        	///////////////
			        		$scope.object_fields = [] 
				  		  var fields = {}
				  		  for(index in obj_list){
				  			 obj = obj_list[index]
				  			 for(f in obj){
				  				 fields[f] = 1;
				  			 }
				  		  }
				  		 
			        		$scope.id_field = "_id";
			        		$scope.$apply(function(){
			        			
			        			delete fields["_id"];
			        			
			        			for(var field in fields){
			  		  			  $scope.object_fields.push(field);
			  		  		  }
			  		  		  $scope.obj_list = obj_list;
			  		  		  $scope.prev_page = data["previous"];
			  		  		  $scope.next_page = data["next"];
			  		  		  $scope.count = data["count"];
			  		  		  
			  		  		  
						    });	       
			        		
			        		$scope.show_page_message();
			        		
			        		/* disable objects delete button */
			        		  var del_btn = $('#delete-objects')[0];
			        		  var is_disabled = del_btn.className.indexOf("disabled");
			        		  if(is_disabled == -1){
			        			  del_btn.className += " disabled";
			        		  }
			         },
			         error: function(xhr, status, err){
						  
						  myspinner.stop();
						  alert("Unable to complete operation. Server Error!");
					  }
			      });
			  
		  }
		  else{
			  return false;
		  }
		  
	  }
	  
	  
	$scope.nextPage = function(){
		
		 if($scope.next_page != null){
			 
			 myspinner.spin($("#spinner")[0]);
			 
			  $.ajax({
			         url: "/api/v2/classes/" + $scope.selectedClass + "/" + $scope.next_page,
			         type: "GET",
			         beforeSend: function(xhr){xhr.setRequestHeader('AppId', $scope.currAppObject.key);},
			         success: function(data) { 
			        	obj_list = data["results"];
			        	myspinner.stop();
			        	
			        	///////////////
			        		$scope.object_fields = [] 
				  		  var fields = {}
				  		  for(index in obj_list){
				  			 obj = obj_list[index]
				  			 for(f in obj){
				  				 fields[f] = 1;
				  			 }
				  		  }
				  		 
			        		$scope.id_field = "_id";
			        		$scope.$apply(function(){
			        			
			        			delete fields["_id"];
			        			
			        			for(var field in fields){
			  		  			  $scope.object_fields.push(field);
			  		  		  }
			  		  		  $scope.obj_list = obj_list;
			  		  		  $scope.prev_page = data["previous"];
			  		  		  $scope.next_page = data["next"];
			  		  		$scope.count = data["count"];
			  		  		  
						    });	       
			        		
			        		$scope.show_page_message();
			        		
			        		/* disable objects delete button */
			        		  var del_btn = $('#delete-objects')[0];
			        		  var is_disabled = del_btn.className.indexOf("disabled");
			        		  if(is_disabled == -1){
			        			  del_btn.className += " disabled";
			        		  }
			        		
			         },
			         error: function(xhr, status, err){
						  
						  myspinner.stop();
						  alert("Unable to complete operation. Server Error!");
					  }
			      });
			 
		  }
		  else{
			  return false;
		  }
		  
	  }
	  
	  $scope.selectObject = function(objid, index){
		   
		  row = $('#obj-table').find('tr')[index + 1];
		  if(row.className.indexOf("checked") == -1){
			  row.className += " checked"
				  $selected_objects.push(objid);
		  }
		  else{
			  row.className = row.className.replace("checked", "");
			  var removeIndex = $selected_objects.indexOf(objid);
			  if (removeIndex > -1) {
				  $selected_objects.splice(removeIndex, 1);
				}
		  }
		  
		  var del_btn = $('#delete-objects')[0];
		  /* enable objects delete button */
		  if($selected_objects.length > 0){
			  
			  del_btn.className = del_btn.className.replace("disabled", ""); 
		  }
		  else{
			  del_btn.className += " disabled";
		  }
		  
		  
	  }
	  
	  
	  
	
})















