'use strict';

/* Controllers */
angular.module('skillsortApp2.controllers', []).
	controller('GameCtrl', ['$http', '$rootElement', '$scope', '$compile', function($http, $rootElement, $scope, $compile){
		
		var stage_template = angular.element("<stage></stage>");
        var game_type = $rootElement[0].attributes["game-type"].value;

		$http.get('/api/axes?game_type='+game_type+'').success( function(data) {
    		$scope.axes = data;

    		$http.get('/api/skills').success( function(data) {
    			$scope.skills = data;
                $scope.game_type = game_type;
    			
    			$rootElement.append(stage_template);
    			$compile(stage_template)($scope);


                // Configure Slider settings for Game 3
                $('#slider').slider({
                    value: 15,
                    min: 0,
                    max: 30,
                    step: 1,
                    slide: function( event, ui ) {
                        $( "#hours" ).text( ui.value );
                    }
                });


                // Configure Joyride for game instructions. This simulates the button click and return card.
                // $(document).foundation('joyride', 'start');
                $(document).foundation({
                    joyride: {
                        expose: true,
                        modal: true
                    }
                }).foundation('joyride', 'start');

                if(game_type == 1){
                    $($(".joyride-content-wrapper a")[4]).click( function(){
                        $scope.stage_scope.selected(5);
                    });
                    $($(".joyride-content-wrapper a")[6]).click( function(){
                        $scope.stage_scope.moveBack(1);
                    });
                }
                if(game_type == 2){
                    $($(".joyride-content-wrapper a")[4]).click( function(){
                        $scope.stage_scope.selected(4);
                    });
                    $($(".joyride-content-wrapper a")[6]).click( function(){
                        $scope.stage_scope.moveBack(1);
                    });
                }
                if(game_type == 3){
                    $($(".joyride-content-wrapper a")[4]).click( function(){
                        $scope.stage_scope.sortHours();
                    });
                    $($(".joyride-content-wrapper a")[6]).click( function(){
                        $scope.stage_scope.moveBack(1);
                    });
                }

                // Configure the tooltips style
                $(document).foundation({
                  tooltips: {
                    selector : '.has-tip',
                    additional_inheritable_classes : [],
                    tooltip_class : '.tooltip',
                    touch_close_text: 'tap to close',
                    disable_for_touch: false,
                    tip_template : function (selector, content) {
                      return '<span data-selector="' + selector + '" class="'
                        + Foundation.libs.tooltips.settings.tooltipClass.substring(1)
                        + '">' + content + '<span class="nub"></span></span>';
                    }
                  }
                });
    		});
    	});
	}]);