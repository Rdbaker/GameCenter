getApiKey = ->
  $('meta[name=api_key]')[0].content

dailyChart = d3.select("#daily-chart").append("svg")
  .attr("width", 960)
  .attr("height", 500)

changeGraph = (show) ->
  if show == 'daily'
    $('#weekly-chart').hide()
    $('#daily-chart').show()
  if show == 'weekly'
    $('#daily-chart').hide()
    $('#weekly-chart').show()

setHeaders = (xhr) ->
  xhr.setRequestHeader('Authorization', "Bearer #{getApiKey()}")

chartsNotInitialized = true

makeCharts = (data) ->
  chartsNotInitialized = false
  makeDailyChart(data.daily_reqs)
  makeWeeklyChart(data.weekly_reqs)

make2DArray = (length) ->
  (0 for num in [1..length])

diffDays = (before, now) ->
  # hours*minutes*seconds*milliseconds
  oneDay = 24*60*60*1000
  Math.round(Math.abs((now.getTime() - new Date(before).getTime())/(oneDay)))

getRequests = ->
  options =
    beforeSend: setHeaders
    url: '/dashboard/requests'
    method: 'GET'
  $.ajax(options)
    .done (data) ->
      $('#requests-made').html(data.data.daily_reqs.length)
      makeCharts(data.data) if chartsNotInitialized
    .fail (data) ->
      console.log data

makeDailyChart = (requests) ->
  $(dailyChart).empty()
  console.log 'wow look at that chart!'

makeWeeklyChart = (requests) ->
  past7Days = make2DArray 7
  now = new Date
  for req in requests
    idx = diffDays(req.created_at, now)
    past7Days[idx] = past7Days[idx]+1
  lineFunction = d3.svg.line()
    .x((d, i) -> x(i))
    .y((d, i) -> y(d))
    .interpolate("linear")
  weeklyChart = new LineChart past7Days.reverse(), 'Weekly Requests', lineFunction
  weeklyChart.render('#weekly-chart')

$ ->
  getRequests()
  setInterval(getRequests, 3000)
  $('#daily').on('click', () -> changeGraph('daily'))
  $('#weekly').on('click', () -> changeGraph('weekly'))
