var getRequests;

getRequests = function() {
  var apiKey, options;
  apiKey = $('meta[name=api_key]')[0].content;
  options = {
    beforeSend: (function(_this) {
      return function(xhr) {
        return xhr.setRequestHeader('Authorization', "Bearer " + apiKey);
      };
    })(this),
    url: '/dashboard/requests',
    method: 'GET'
  };
  return $.ajax(options).done(function(data) {
    console.log(data);
    return $('#requests-made').html(data.data.length);
  }).fail(function(data) {
    return console.log(data);
  });
};

$(function() {
  return getRequests();
});
