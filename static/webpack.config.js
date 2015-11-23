var path = require("path");
module.exports = {
  devtool: 'source-map',
  entry: {
        app: "./app.coffee",
        header: "./header.coffee",
  	},
  output: {
  		path: path.join(__dirname, "build"),
  		filename: "[name].js",
  		chunkFilename: "[id].chunk.js"
  	},
  module: {
    loaders: [
      { test: /\.coffee$/, loader: "coffee-loader" },
      { test: /\.less$/, loader: "style!css!less" },
      { test: /\.(html|tpl)$/, loader: "html?attrs=img:requir-src" },
      { test: /\.css$/, loader: "style!css" },
    ]
  },
  resolve: {
    extensions: ["", ".web.coffee", ".web.js", ".coffee", ".js"],
    alias: {
        'lib': '/Users/bigzhu/lib_bz'
      }
  },
  externals: {
    vue: "vue",
    //toastr 要用到，不能external
    //jquery: "jquery",
    underscore: "underscore",
    director:'director',
    simditor:"simditor"
  }
}
