$(document).ready(function(){
    //var tags = []
    // $.get('tags.txt', function(data) {
    //     console.log(data)
    //     tags = data;
    // });

    var tags = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.whitespace,
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      // url points to a json file that contains an array of country names, see
      // https://github.com/twitter/typeahead.js/blob/gh-pages/data/countries.json
      prefetch: {
        url: 'http://localhost:1881/loadTags',
        filter: function(tags){console.log(tags)}
    //     filter: function(response) {      
    //   return response.countries;
    // }
      }
    });

    $('#prefetch .typeahead').typeahead({
        //source: tags,
        name: 'tags',
        source: tags, 
        minLength: 1,
        items: 8,
        highlight: true
    });

    $("#tag-search").submit(function(event) {
        var value = $("input:first").val();
        if ($.trim(value).length === 0) {

        } else {
            
        }
    });

    $(".tag").on('click', function() {
        var query = this.id;
        getVideos(query);
    });

    function getVideos(query) {

    }
});