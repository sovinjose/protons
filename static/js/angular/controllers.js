
// edit_survey.html, add_survey.html
function SurveyController($scope, $http){
    // Fetching the Survey Details by passing the survey id as an argument in init method
    $scope.init = function(csrf_token, survey_id){
        $scope.csrf_token = csrf_token;
        $scope.survey_id = survey_id;
        if ($scope.survey_id){
            $http.get('/survey/edit/'+$scope.survey_id+'/').success(function(data){
                $scope.survey = data;
                $scope.questions = data.questions;
                $scope.survey_questions = data.survey_questions;
                $scope.select_question();
            });
        }
    }
    // Fetching the Question Details 
    $scope.select_question = function(){
        if ($scope.survey_id){
            $scope.surv_quest = $scope.survey_questions;
        }
        if ($scope.surv_quest == undefined) {
            $scope.surv_quest = [];
        }
    	params = {
    		'question_ids': $scope.surv_quest.toString(),
            'csrfmiddlewaretoken': $scope.csrf_token,
    	}
    	$http({
    		method: "post",
			url: "/survey/question_details/",
			data: $.param(params),
			headers : {
                'Content-Type' : 'application/x-www-form-urlencoded'
            }
    	}).success(function(data){
            $scope.questions_data = [];
            $scope.questions_data = data;
    	}).error(function(data){
    		console.log(data);
    	})
    }
    // Validating the survey fields before sending the save request
    $scope.validate = function(){
        if ($scope.survey.survey_title == undefined || $scope.survey.survey_title == ''){
            return false;
        } else if ($scope.survey.survey_description == undefined || $scope.survey.survey_description == ''){
            return false;
        } else if ($scope.survey.survey_condition == undefined || $scope.survey.survey_condition == ''){
            return false;
        } else if ($scope.survey.customer == undefined || $scope.survey.customer == ''){
            return false;
        } else if ($scope.survey.survey_questions == undefined){
            return false;
        }
        return true;
    }
    // Sending Survey save request
    $scope.edit_survey = function(){
        $scope.survey.survey_questions = $scope.survey_questions;
        params = {
            'csrfmiddlewaretoken': $scope.csrf_token,
            'survey': angular.toJson($scope.survey),
        }
        if ($scope.validate()){
            $http({
                method: "post",
                url: "/survey/edit/"+$scope.survey_id+"/",
                data: $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                document.location.href = '/survey/list/';
            });
        }
    }
}

// survey_response.html
// Handling survey Response

function SurveyResponseController($scope, $http){

    $scope.survey = {
        'survey_id': '',
        'ticket_id': '',
        'questions': [],
    }
    // Fetching the Survey Details by passing the survey id, ticket id, user id as an argument in init method
    $scope.init = function(csrf_token, survey_id, ticket_id, user_id){
        $scope.survey_id = survey_id;
        $scope.ticket_id = ticket_id;
        $scope.user_id = user_id;
        $scope.survey.survey_id = survey_id;
        $scope.survey.ticket_id = ticket_id;
        $scope.csrf_token = csrf_token;
        if ($scope.survey_id && $scope.ticket_id){
            $http.get('/survey/'+$scope.survey_id+'/ticket/'+$scope.ticket_id+'/user/'+$scope.user_id+'/?ajax=true').success(function(data){
                $scope.survey_questions = data.questions;
            });
        }
    }
    $scope.choose_answer = function(choice, question){
        // choosing qusetion's answer and make the checkbox clicked by adding the 'checked' class
        question.answer_choice = choice.choice_id;
        for(var i=0; i < question.choices.length; i++){
            parent_div = $('#'+question.choices[i].id_val).parent();
            parent_div.removeClass('checked');
        }
        parent_div = $('#'+choice.id_val).parent();
        parent_div.addClass('checked');
    }
    $scope.response_validation = function(){
        // validating survey response
        $scope.error_message = '';
        for (var i=0; i < $scope.survey.questions.length; i++){
            console.log($scope.survey.questions[i]);
            if ($scope.survey.questions[i].q_type == 'choice'){
                if ($scope.survey.questions[i].answer_choice == '' || $scope.survey.questions[i].answer_choice == undefined){
                    $scope.error_message = 'Please choose the option for the question '+(i+1);
                    $('#error_msg').addClass('alert alert-danger');
                    return false;
                }
            } else {
                if ($scope.survey.questions[i].answer_text == '' || $scope.survey.questions[i].answer_text == undefined){
                    $scope.error_message = 'Please answer to the question '+(i+1);
                    $('#error_msg').addClass('alert alert-danger');
                    return false;
                }
            }
        }return true;
    }
    $scope.save_response = function(){
        // sending request to save the survey response
        // $scope.survey.questions = $scope.survey_questions;
        $scope.survey.questions = [];
        for (var i=0; i<$scope.survey_questions.length; i++){
            $scope.survey.questions.push({
                'q_id': $scope.survey_questions[i].q_id,
                'q_type': $scope.survey_questions[i].q_type,
                'answer_choice': $scope.survey_questions[i].answer_choice,
                'answer_text': $scope.survey_questions[i].answer_text,
            })
        }
        if ($scope.response_validation()){
            params = {
                'csrfmiddlewaretoken': $scope.csrf_token,
                'survey': angular.toJson($scope.survey),
            }
            $http({
                method: "post",
                url: "/survey/"+$scope.survey_id+"/ticket/"+$scope.ticket_id+'/user/'+$scope.user_id+'/',
                data: $.param(params),
                headers : {
                    'Content-Type' : 'application/x-www-form-urlencoded'
                }
            }).success(function(data){
                document.location.href = '/?survey=ok';
            });
        }
    }
}