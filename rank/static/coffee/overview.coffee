getApiKey = ->
  $('meta[name=api_key]')[0].content

changeGraph = (show) ->
  if show == 'daily'
    $('#weekly-chart').addClass('hidden')
    $('#daily-chart').removeClass('hidden')
  if show == 'weekly'
    $('#weekly-chart').removeClass('hidden')
    $('#daily-chart').addClass('hidden')

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
      makeCharts(data.data) if chartsNotInitialized
    .fail (data) ->
      console.log data

makeDailyChart = (requests) ->
  todaysHours = make2DArray 24
  for req in requests
    d = new Date(req.time_requested)
    todaysHours[d.getUTCHours()] = todaysHours[d.getUTCHours()] + 1
  lineFunction = d3.svg.line()
    .x((d, i) -> x(i))
    .y((d, i) -> y(d))
    .interpolate("linear")
  dailyChart = new LineChart todaysHours, 'Daily Requests'
  dailyChart.render('#daily-chart')

makeWeeklyChart = (requests) ->
  past7Days = make2DArray 7
  now = new Date
  for req in requests
    idx = diffDays(req.time_requested, now)
    past7Days[idx] = past7Days[idx] + 1
  lineFunction = d3.svg.line()
    .x((d, i) -> x(i))
    .y((d, i) -> y(d))
    .interpolate("linear")
  weeklyChart = new LineChart past7Days.reverse(), 'Weekly Requests', (3600 * Number($('meta[name=num_users]')[0].content))
  weeklyChart.render('#weekly-chart')

$ ->
  getRequests()
  $('#daily').on('click', () -> changeGraph('daily'))
  $('#weekly').on('click', () -> changeGraph('weekly'))
