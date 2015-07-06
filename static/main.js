(function() {
  $(function() {
    return $("#toc").tocify({
      selectors: ".title_bz"
    }).data("toc-tocify");
  });

}).call(this);
