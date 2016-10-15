'use strict';

// Declare app level module which depends on filters, and services
var app1 = angular.module('skillsortApp1', []);


app1.config(['$httpProvider', function($httpProvider) {
    // Get Auth Token
	var authToken = $('meta[name=\"csrf-token\"]').attr("content");
	$httpProvider.defaults.headers.common["X-CSRF-TOKEN"] = authToken
}]);