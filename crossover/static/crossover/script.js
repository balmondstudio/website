// Crossover Module
var crossover = (function() {

  var interval;
  var screen_name;

  var config = {
    //source: 'http://0.0.0.0:5000/data',
    source: 'http://crossover.balmondstudio.com/data',
  };

  var init = function() {
    $('div#form > form > button').click(function() {
      screen_name = $('div#form > form > input').val();
      if (screen_name) {
        $('div#form').fadeOut(1000);
      }
    });

    graphics.init();

    interval = window.setInterval(load, 1000);
  };

  var load = function() {
    $.getJSON(config.source, consume);
  };

  var consume = function(data) {
    $.each($('div#content:first').data(), function(key, value) {
      if (value.fields.text != data[key].fields.text) {
        update(key, data);
        if (data[key].fields.screen_name == screen_name) {
          lock();
        }
      }
    });
    $('div#content:first').data(data);
  };

  var update = function(key, data) {
    $('li>h3').eq(key).css('color', graphics.config.stroke.color[key]);
    $('li>p').eq(key).text(data[key].fields.text);
    graphics.update(key);
  };

  var lock = function() {
    window.clearInterval(interval);
    $('div#tweet').fadeOut(1000);
  };

  return {
    init: init,
    config: config
  };

})();


// Graphics Module
var graphics = (function() {

  var container;
  var center;
  var frame;
  var amplitude;
  var start;
  var step;
  var paper;
  var paths;

  var config = {
    frame: {
      width: 0.5,
      height: 0.3,
    },
    amplitude: {
      width: 0.25,
      height: 1
    },
    stroke: {
      color: ['#7a1719', '#3043a1', '#2a622e', '#fdd318', '#532c8d', '#f9a5ce'],
      join: 'round', // bevel, round, miter
      opacity: 0.9,
      width: 0.5,
      reset: 'black'
    },
    animation: {
      duration: 300,
      easing: 'easeInOut' // linear, easeIn, easeOut, easeInOut, backIn, backOut, elastic, bounce
    },
    structure: {
      container: 'div#graphics',
      folds: 3,
      size: 6
    },
    callback: undefined
  };

  var init = function() {
    container = {
      w: $(config.structure.container).width(),
      h: $(config.structure.container).height()
    };

    center = {
      w: container.w * 0.5,
      h: container.h * 0.5
    };

    frame = {
      w: container.w * config.frame.width,
      h: container.h * config.frame.height
    };

    amplitude = {
      w: frame.w * config.amplitude.width,
      h: frame.h * config.amplitude.height
    };

    start = {
      w: center.w - frame.w * 0.5,
      h: center.h - frame.h * 0.5
    };

    step = {
      w: frame.w / (config.structure.folds + 1),
      h: frame.h / config.structure.size
    };

    paper = Raphael('graphics', container.w, container.h);

    paths = paper.set();
    for (var i = 0; i < config.structure.size; i++) {
      paths.push(
        paper
          .path(line(start, step, i))
          .attr({ 
            stroke: config.stroke.reset, 
            'stroke-linejoin': config.stroke.join,
            'stroke-width': (frame.h / config.structure.size) * config.stroke.width,
            'opacity': 0
          })
      );
    }
  };

  var update = function(key) {
    paths[key]
      .animate({ 
        path: curve(start, step, key), 
        stroke: config.stroke.color[key],
        opacity: config.stroke.opacity
      }, config.animation.duration, config.animation.easing);
  };

  var save = function() {
  };

  var line = function(start, step, key) {
    return 'M0,' + (start.h + step.h * key) + 'L' + container.w + ',' + (start.h + step.h * key);
  };

  var curve = function(start, step, key) {
    var temp =
    'M' + '0' + ',' + (start.h + step.h * key) +
    'L' +  start.w + ',' + (start.h + step.h * key) +
    'R';
    for (var i = 0; i < config.structure.folds; i++) {
      temp +=
        random(
            (start.w + step.w * (i + 1)) - amplitude.w, 
            (start.w + step.w * (i + 1)) + amplitude.w) +
        ',' + 
        random(
            (start.h + step.h * key) - amplitude.h, 
            (start.h + step.h * key) + amplitude.h) +
        ' ';
    }
    temp += 
    (start.w + frame.w) + ',' + (start.h + step.h * key) +
    'L' + container.w + ',' + (start.h + step.h * key);

    return temp;
  };

  var random = function(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
  };

  return {
    config: config,
    init: init,
    update: update,
    paths: paths
  };

})();


// Document Ready
$(document).ready(function() {
  crossover.init();
});
