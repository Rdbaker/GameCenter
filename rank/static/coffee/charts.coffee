class ChartSettings
  constructor: () ->
    @margin = { top: 20, right: 20, bottom: 30, left: 40 }
    @width = 640 - @margin.left - @margin.right
    @height = 500 - @margin.top - @margin.bottom
    @title_height = 16
    @color = d3.scale.ordinal().range([
      'rgb(241,238,246)','rgb(208,209,230)','rgb(166,189,219)','rgb(116,169,207)',
      'rgb(54,144,192)','rgb(5,112,176)','rgb(3,78,123)'
    ].reverse())

  svgWidth: ->
    @width + @margin.left + @margin.right

  svgHeight: ->
    @height + @margin.top + @margin.bottom

  svgTransformValue: ->
    "translate(#{@margin.left}, #{@margin.top})"


class LineChart
  constructor: (@chart_data, @chart_title, max_y_val) ->
    @chart_settings = new ChartSettings()
    @max_y_val = max_y_val or 3600
    @setChartAxes()

  line_function: ->
    d3.svg.line()
      .x((d, i) => @x(i))
      .y((d) => @y(d))

  setChartAxes: =>
    max = d3.max @chart_data
    if @chart_title == "Weekly Requests"
      max = d3.max([@max_y_val+(@max_y_val * 0.1), d3.max(@chart_data)])
    @x = d3.scale.linear().domain([0, @chart_data.length-1]).range([0, @chart_settings.width])
    @y = d3.scale.linear().domain([0, max]).range([@chart_settings.height, @chart_settings.title_height])
    @x_axis = d3.svg.axis().scale(@x).orient('bottom').tickFormat(d3.format('d')).tickSubdivide(0)
    @y_axis = d3.svg.axis().scale(@y).orient('left').tickFormat(d3.format('d')).tickSubdivide(0)

  render: (selector) ->
    # create the svg
    svg = d3.select(selector).append "svg"
        .attr "width", @chart_settings.svgWidth()
        .attr "height", @chart_settings.svgHeight()
      .append 'g'
        .attr 'transform', @chart_settings.svgTransformValue()

    # draw the x_axis
    svg.append 'g'
        .attr 'class', 'x-axis axis'
        .attr 'transform', "translate(0, #{@chart_settings.height})"
        .call @x_axis

    # draw the y_axis
    svg.append 'g'
        .attr 'class', 'y-axis axis'
        .call @y_axis
      .append 'text'
        .attr 'transform', 'rotate(-90)'
        .attr 'y', 6
        .attr 'dy', '.7em'
        .style 'text-anchor', 'end'
        .text 'Request Count'

    # draw the data
    svg.append 'path'
      .attr('d', @line_function()(@chart_data))
      .attr 'stroke', 'steelblue'
      .attr 'stroke-width', 2
      .attr 'fill', 'none'

    # draw the hard-coded throttle limit
    if @chart_title == "Weekly Requests"
      throttle_line = (@max_y_val for i in [1..@chart_data.length])
      svg.append 'path'
        .attr('d', @line_function()(throttle_line))
        .attr 'stroke', 'steelblue'
        .style 'stroke-dasharray', ('3, 3')
        .attr 'stroke-width', 2
        .attr 'fill', 'none'
