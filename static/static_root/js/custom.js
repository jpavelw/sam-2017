/**
 * Created by Jairo on 09/29/2015.
 */
$(document).ready(function($) {
    $(".clickable-row-check").click(function() {
        var checkbox = ($("#"+$(this).data("checkbox")));
        if(checkbox.is(":checked"))
            checkbox.prop('checked', false);
        else
            checkbox.prop('checked', true);
    });
    $( ".datepicker" ).datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: "yy-mm-dd"
        // You can put more options here.
    });
    $( "#id_enabled" ).addClass( "status-list" );
    $(".clickable-row-deadline").click(function() {
        window.document.location = $(this).data("href");
    });
});

(function(){

    var app = angular.module('submissionsApp', []);
    app.config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    });

    app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    });

    app.directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function(scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function(){
                    scope.$apply(function(){
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };
    }]);

    app.controller('SubmissionController', [ '$http', function($http){
        var outCtr = this;

        this.getSubmissions = function(){
            var URL = $( "#url" ).text();
            outCtr.url_ = URL;
            $http.get(URL).success(function(data){
                if(data.statusCode == 200){
                    outCtr.media = data.media;
                    outCtr.postURL = data.postURL;
                    outCtr.submissions = JSON.parse(data.data);
                }
            });
        };

        this.submitFile = function(){
            $('#msg-box').hide();
            var $csrftoken = $('input[name="csrfmiddlewaretoken"]');
            var token = $csrftoken.attr( "value" );
            var fd = new FormData();
            fd.append('file', outCtr.file);
            fd.append('csrfmiddlewaretoken', token);
            $http.post(outCtr.postURL, fd,{
                transformRequest: angular.identity,
                headers: {'Content-Type': undefined}
            }).success(function(data){
                if(data.statusCode == 200){
                    outCtr.submissions.unshift(JSON.parse(data.data)[0]);
                    $("#id_file").val("");
                    var list_url = outCtr.url_.split("/");
                    var button_id = list_url[list_url.length-2];
                    var $button = $('#'+button_id);
                    var text = parseInt($button.text());
                    $button.text(text+1);
                }
                else{
                    var $msg_box = $('#msg-box');
                    $msg_box.text(data.message);
                    $msg_box.show();
                }
            });
        };

    }]);

    $('#subModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var URL = button.data('url'); // Extract info from data-* attributes
        // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
        // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.

        $('#msg-box').hide();
        var modal = $(this);
        modal.find('#url').text(URL);
        modal.find('#getSubmissionsBtn').click();
    });
})();