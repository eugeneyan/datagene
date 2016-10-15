'use strict';

// Declare app level module which depends on filters, and services
angular.module('skillsortApp2', [
	'ngAnimate',
	'skillsortApp2.filters',
  	'skillsortApp2.services',
  	'skillsortApp2.directives',
  	'skillsortApp2.controllers']).
	config(['$httpProvider', function($httpProvider) {
	    // Get Auth Token
		var authToken = $('meta[name=\"csrf-token\"]').attr("content");
		$httpProvider.defaults.headers.common["X-CSRF-TOKEN"] = authToken
	}]);