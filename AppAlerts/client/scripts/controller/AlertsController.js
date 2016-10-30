(function (angular, lab) {
    'use strict';
    
    function AlertsController($http) {
        var vm = this,
            httpRequest;

      var filterKeys = ["bomberos", "ecu911quito", "policia", "accidente", "sismo", "terremoto", "cruzroja", "robo", "peligro", "ambulancia", "ayuda"]
      vm.initialKeyWords = [];
      vm.generalKeyWords = [];

        
   


      function callElasticSearchFilter(filter, destiny){
         var config = {
          method: 'POST',
          url: '/elasticsearch',
          headers : { "Content-Type": "application/json" },
          data: { filtro :  filter}
        };
        $http(config)
        .success(function(data) {
           console.log(data)
           if (destiny.length == 0) {
              data.forEach( function (arrayItem){
                var item = {
                  key : arrayItem.key,
                  doc_count: arrayItem.doc_count,
                  current_doc_count: 0,
                  diff: 0
                }
                destiny.push(item);
              });
           } else {
              destiny.forEach( function(arrayInitial, oldIndex){
                data.forEach( function (arrayNew, newIndex){
                  if(arrayInitial.key == arrayNew.key){
                    var item = {
                      key : arrayInitial.key,
                      doc_count: arrayInitial.doc_count,
                      current_doc_count: arrayNew.doc_count,
                      diff: arrayNew.doc_count - arrayInitial.doc_count 
                    }
                    destiny[oldIndex] = item
                  }
                });
              });
           }
        })
        .error(function(response) {
              console.log(response);
        });
      }

      callElasticSearchFilter(filterKeys, vm.initialKeyWords)
      callElasticSearchFilter([], vm.generalKeyWords)
      
      vm.clickElasticsearch = function(){
        callElasticSearchFilter(filterKeys, vm.initialKeyWords)
      }

      vm.getGeneralKeyWords = function(){
        callElasticSearchFilter([], vm.generalKeyWords)
      }

      vm.getFilterKeyWords = function(){
        return filterKeys.join(" OR ");
      }

    }
    AlertsController.$inject = ['$http'];
    
    angular.module(lab.MODULE)
        .controller('AlertsController', AlertsController);

}(window.angular, window.lab));

