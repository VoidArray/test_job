(function(){
	angular.module('myapp',[])

	.controller('ajax_ctrl',['$http','$scope',function($http,$scope){
		$http.get('/search/').success(function(response){ //make a get request to mock json file.
			$scope.data = response; //Assign data recieved to $scope.data
			console.log($scope.data)
		})
		.error(function(err){
			console.log('failed get json')
		})
	}])
        
})();
