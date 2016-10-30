(function (global, angular) {
    'use strict';
    
    var lab = {
            MODULE: 'AngularAlerts'
        },
        dependencies = ['ngMessages'];
    
    function ApplicationConfig() {
    }
    ApplicationConfig.$inject = [];
    
    
    angular.module(lab.MODULE, dependencies)
        .config(ApplicationConfig);
    
    global.lab = lab;
    
}(window, window.angular));

