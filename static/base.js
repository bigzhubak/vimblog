(function() {
  $(function() {
    return window.header_search = function(search_value) {
      var url;
      url = "/list/" + search_value;
      return window.open(url);
    };
  });

}).call(this);
