getRequests = ->
  apiKey = $('meta[name=api_key]')[0].content
  options =
    beforeSend: (xhr) =>
      xhr.setRequestHeader('Authorization', "Bearer #{apiKey}")
    url: '/dashboard/requests'
    method: 'GET'
  $.ajax(options)
    .done (data) ->
      $('#requests-made').html(data.data.daily_reqs.length)
    .fail (data) ->
      console.log data

$ ->
  setInterval(getRequests, 1000)
