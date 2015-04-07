(function()
{
	/*$(function()
        {
           $('#preferred_apps').jScrollPane(); 
           $('#cus_scroll').jScrollPane(); 
        });
	*/
	var app = angular.module('preferences',[]);
  var list_of_ids = [];
	app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
  });

  app.controller('PostController',function($scope){
    $scope.friends = "";
    var userName = $('#current_user').html();
    var userEmail = $('#current_user_email').html();
    var userId = $('#current_user_id').html();
    

    $scope.makePost = function()
      {
        //get content , and post it to database
        var r = confirm("Are you sure you want to add this app ?");
        if (r==true)
        {
          var post_content = $("#post_content").val(); 
          var dic_data = {post_content:post_content,id:userId,tags:JSON.stringify(list_of_ids)}
          $.post("/make_posts",dic_data,function(response){
              location.reload();
          });  
        }
        
      };

  });




	app.controller('SearchPreferenceController',function($scope){
		$scope.friends = "";
		var userName = $('#current_user').html();
		var userEmail = $('#current_user_email').html();
    var userId = $('#current_user_id').html();
    var aq = [];
		$('#query').keypress(function(){
                    var query = $("#query").val();
                    $.post("/find_friends",{query:query,id:userId}, function( data ) {
                        aq = eval('('+data+')');
                        //console.log(aq);
                        $scope.friends = aq;
                        //console.log($scope.friends);
                    }); 
             });

		$scope.tagFriend = function(friendId)
			{
				//alert(bundleId);
					console.log(friendId[0][0]);
          //console.log(aq);
          console.log(list_of_ids);
          if (list_of_ids.indexOf(friendId[0][0]) == -1)
          {
            list_of_ids.push(friendId[0][0]);
            var str = $("#current_tags").html();
            var html_to_be_added = ""
            for(var i=0;i<aq.length;i++)
            {
              if(aq[i]['id']==friendId)
              {
                html_to_be_added+="<ol style='list-style:none;margin-left:10px'><li class='stbody'><div class='stimg'><img src='"+aq[i]['pic']+"' width='60' height='60' /></div><div class='sttext'>"+aq[i]['name']+"</div></li></ol>"
              }
            }
            var total = str+html_to_be_added;
            $("#current_tags").html(total);
          }
          else
          {
            alert("Already Tagged this user");
          }
          
          //var html_to_be_added = "
          //var data = {user:userName,email:userEmail,friendId:friendId,sourceId:userId};
					//$.post("/tag_friends",data,function(response){
          //    
					//});
				
			};

	});



})();
