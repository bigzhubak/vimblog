$ ->
  window.header_search = (search_value)->
    url = "/list/"+ search_value
    window.open(url)

