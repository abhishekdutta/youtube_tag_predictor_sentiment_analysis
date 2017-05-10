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
        var value = $("#query").val();

        if ($.trim(value).length === 0) {
            $('#error-message').show();
            return false;
        } else {
            $.get( "/searchVideos", { query: value} )
                .done(function( data ) {

                    alert( "Data Loaded: " + data );
                });
        }
    });

    $(".tag").on('click', function() {
        var query = this.id;
        getVideos(query);
    });

    function getVideos(query) {

    }
});