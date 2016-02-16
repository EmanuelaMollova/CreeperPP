function getURLParameter(url, parameter) {
    var parametersPart = url.split("?")[1];
    if(parametersPart) {
        var separator  = parametersPart.indexOf("&amp;") >= 0 ? '&amp;' : '&';
        var parameters = parametersPart.split(separator);
        for (var i = 0; i < parameters.length; i++) {
            var parameterName = parameters[i].split('=');
            if(parameterName[0] == parameter) {
                return parameterName[1];
            }
        }
    }
}

function getTestResults(url) {
    var results = {};
    if(getURLParameter(url, 'oR')) {
        results.o = getURLParameter(url, 'oR');
    }
    if(getURLParameter(url, 'cR')) {
        results.c = getURLParameter(url, 'cR');
    }
    if(getURLParameter(url, 'eR')) {
        results.e = getURLParameter(url, 'eR');
    }
    if(getURLParameter(url, 'aR')) {
        results.a = getURLParameter(url, 'aR');
    }
    if(getURLParameter(url, 'nR')) {
        results.n = getURLParameter(url, 'nR');
    }

    return results;
}

$( document ).ready(function() {
    var data = {};
    var promises = [];

    $('.twitter-timeline-link').each(function() {
        var link = $(this).data('expanded-url');
        if(link) {
            var user = $(this).closest('div.tweet.original-tweet').data('screen-name');

            if(link.indexOf("outofservice") >= 0) {
                var results = getTestResults(link);
                if(!jQuery.isEmptyObject(results)) {
                    data[user] = results;
                }
            } else {
                var encodedUrl = encodeURIComponent(link);
                var requestUrl = 'http://urlxray.com/display.php?url=' + encodedUrl;

                var request = $.get({
                    url: requestUrl,
                    dataType: "html",
                    success: function(response) {
                        response = response.replace(/<img[^>]*>/g,"");
                        var longUrl = $('.resultURL2 a', response).attr('href');
                        if(longUrl) {
                            var results = getTestResults(longUrl);
                            if(!jQuery.isEmptyObject(results)) {
                                data[user] = results;
                            }
                        }
                    }
                });

                promises.push(request);
            }
        }
    });

    $.when.apply(null, promises).done(function(){
        alert('Data is extracted.');
        console.log("There are " + Object.keys(data).length + " user results.");
        console.log(data);
    });
});
