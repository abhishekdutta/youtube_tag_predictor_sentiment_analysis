$(document).ready(function(){
    var $default_videos = $("#results-cell").find($(".result"));

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
        event.preventDefault();

        return checkQuery(event, searchVideos);
    });

    function checkQuery(event, next) {
        var value = $("#query").val();
        console.log(value);
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
            success: function(data){
                appendVideos(data);
            },
            error: function(err) {
                alert(err);
                return false;
            }
        });
    }

    function appendVideos(data) {
        var curr_videos = $("#results-cell").find($(".result"));
        var i = 0;
        var $vid = $(curr_videos[i]);
        data.forEach(function(video, next) {
            $vid.attr('id', video.video_id);
            console.log($vid.find('iframe'));
            $vid.find('iframe').attr('src', 'http://youtube.com/embed/'+video.video_id);
            var $sent = $vid.find(".sentiment")
            $sent.text(video.sentiment_percentage);
            $sent.removeClass();
            $sent.addClass("sentiment " + video.sentiment_category);
            $vid.find('a').attr('href', 'http://youtube.com/watch?v=' + video.video_id);
            $vid.show();
            i++;
            $vid = $(curr_videos[i]);
        });
        console.log($vid)
        if (i === data.length) {
            for (i; i < 10; i++) {
                $vid = $(curr_videos[i]);
                $vid.hide();
            }

            if (i === 10){
                console.log(curr_videos);
                $("#results-cell").append(curr_videos);
                console.log($("results-cell").find("*"));

            }
        }
    }
});