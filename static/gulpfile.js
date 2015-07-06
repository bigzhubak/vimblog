var gulp = require('gulp');
var less = require('gulp-less');
var coffee = require('gulp-coffee');
var jsmin = require('gulp-jsmin');
var plumber = require('gulp-plumber');
var notify = require("gulp-notify");
//var cssmin = require('gulp-cssmin');

gulp.task('watch', function () {
  gulp.watch('./*.less', ['less']);
  gulp.watch('./*.coffee', ['coffee']);
});

gulp.task('less', function () {
    return gulp.src('./*.less')
    .pipe(plumber({errorHandler: notify.onError("Error: <%= error %>")}))
    .pipe(less())
    .pipe(gulp.dest('./'));
});

gulp.task('coffee', function () {
    gulp.src('./*.coffee')
    .pipe(plumber({errorHandler: notify.onError("Error: <%= error %>")}))
    .pipe(coffee())
    .pipe(gulp.dest('./'));
});
gulp.task('default', ['less','coffee', 'watch']);
