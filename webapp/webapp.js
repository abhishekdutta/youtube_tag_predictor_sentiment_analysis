$(document).ready(function(){

    var tags = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('tag'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        identify: function(obj) { return obj.tag; },
        // sorter : function(a, b) {
        //     console.log(a);
        //     console.log(typeof a);
        //     if (a.tag.length < b.tag.length) {
        //             return -1;
        //         } else if (a.tag.length > b.count.tag.length) {
        //             return 1;
        //         } else
        //             return 0;
        //     },
        prefetch: {
            url: 'http://localhost:1881/loadTags'
        }
    });

    $('#query').typeahead({
            minLength: 1,
            items: 10,
            highlight: true
        }, 
        {
            name: 'tags',
            display: 'tag',
            source: tags
    }).blur(function() {
        // var text = $(this).val();
        // if(text.length > 0){
        //     console.log("YOOO");
        //     $('#prefetch').addClass('.has-error');
        //     return false;
        // }
    });

    $("#tag-search").submit(function(event) {
        return checkQuery(event, searchVideos);
    });

    function checkQuery(event, next) {
        var value = $("#query").val();
        if ($.trim(value).length === 0) {
            $('#error-message').show();
            return false;
        } else {
            return next(value);
        }
    }


    $(".tag").on('click', function() {
        var query = this.id;
        searchVideos(query);
    });

    function searchVideos(data) {
        $.ajax({
            url: "http://localhost:1881/searchVideos",
            type: "get", //send it through get method
            data: {query: data},
            success: function(response) {
                response.forEach(function(video) {
                    console.log(video);
                });
                return true;
            },
            error: function(err) {
                alert(err);
                return false;
            }
        });
    }
});