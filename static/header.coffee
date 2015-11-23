#require './app.less'
Vue = require './vue_local.coffee'

error = require 'lib/functions/error.coffee'
v_header = new Vue
  created:->
    error.setOnErrorVm(@)
  data:->
    navbar_header:
      name:'BigZhu的窝'
      href:'/'
    nav_links:[
      {
        name:'全部'
        href:'/list'
        target:''
      },
      {
        name:'vim'
        href:'/list/vim'
        target:''
      },
      {
        name:'python'
        href:'/list/python'
        target:''
      },
      {
        name:'关于bigzhu'
        href:'//me.bigzhu.org'
        target:''
      },
      {
        name:'云南程序员'
        href:'http://yncoder.github.io/'
        target:'_blank'
      }

    ]
  el:'#v_header'
  components:
    'vnav': require('lib/components/nav')
