Vue.config.debug = true
Vue.config.silent = false
Vue.config.delimiters = ['(%', '%)']
Vue.transition 'fade',
  enter: (el, done) ->
    # 此时元素已被插入 DOM
    # 动画完成时调用 done 回调
    $(el).css('opacity', 0).animate { opacity: 1 }, 2000, done
    return
  enterCancelled: (el) ->
    $(el).stop()
    #$(el).animate { opacity: 0 }, 2000, done
    return
  leave: (el, done) ->
    # 与 enter 钩子同理
    $(el).animate { opacity: 0 }, 2000, done
    return
  leaveCancelled: (el) ->
    $(el).stop()
    return

module.exports = Vue
