(function($) {
  $(function() {
    var TYPES = ['nor', 'fir', 'wat', 'ele', 'gra', 'ice',
                 'fig', 'poi', 'gro', 'fly', 'psy', 'bug',
                 'roc', 'gho', 'dra', 'dar', 'ste']
    var TYPES_TRANSLATE = {'nor': 'ノーマル',
                           'fir': 'ほのお',
                           'wat': 'みず',
                           'ele': 'でんき',
                           'gra': 'くさ',
                           'ice': 'こおり',
                           'fig': 'かくとう',
                           'poi': 'どく',
                           'gro': 'じめん',
                           'fly': 'ひこう',
                           'psy': 'エスパー',
                           'bug': 'むし',
                           'roc': 'いわ',
                           'gho': 'ゴースト',
                           'dra': 'ドラゴン',
                           'dar': 'あく',
                           'ste': 'はがね'};
    var TRANSLATE_DICT = {'less': '以下', 'more': '以上', 'equal': 'のみ',
                          '4': '四倍', '2': '二倍', '1': '等倍',
                          '0.5': '半減', '0.25': '1/4', '0': '無効'}
    var TYPES_LENGTH = TYPES.length
    var BASE_URL = 'http://' + window.location.host + '/';

    function tweetlink(id) {
      $("#" + id).attr("href", "https://twitter.com/intent/tweet?text=" +
                       encodeURIComponent($('title').html()) + "&url=" + 
                       encodeURIComponent(window.location.href));
    }
    function changeTitle(hash) {
      var i, t, c, e, line, lines=[], text;
      var params = getUrlQueries(hash);
      for (i in params) {
        if ($.inArray(i, TYPES) !== -1) {
          c = params[i].split('_')[0];
          e = params[i].split('_')[1];
          line = TYPES_TRANSLATE[i] + TRANSLATE_DICT[e] + TRANSLATE_DICT[c];
          lines.push(line);
        }
      }
      if (lines) {
        text = lines.join('・') + 'のポケモン';
        $('title').html(text);
      }
    }

    function load()  {
      var date = new Date;
      var thread_id = 'tid_' + date.getTime();
      var gen, evo, trt, or_;
      
      $('#result')
        .addClass('loading')
        .addClass(thread_id)
        .removeClass('loaded');
      evo = '0';
      trt = '0';
      or_ = '0';
      if ($('input[name="evo"]').attr('checked') == 'checked') {
        evo = '1';
      }
      if ($('input[name="trt"]').attr('checked') == 'checked') {
        trt = '1';
      }
      if ($('input[name="or"]').attr('checked') == 'checked') {
        or_ = '1';
      }
      gen = $('#genc').val() + '_' + $('#gen').val();
      var queries = {evo: evo,
                     gen: gen,
                     trt: trt,
                     or: or_};
      var selector_string;
      for (var i=0; i<TYPES_LENGTH; i++) {
        selector_string = '#' + TYPES[i];
        if ($(selector_string).val() !== "-1") {
          queries[TYPES[i]] = $(selector_string + 'c').val() + 
                              '_' + $(selector_string).val();
        }
      }
      $.ajax({
        url: '/api',
        type: 'GET',
        dataType: 'jsonp',
        data: queries,
        success: function(data) {
          var len = data.length;
          $('#result').removeClass(thread_id)
          if ($('#result').attr('class') === 'result loading') {
            $('#result').addClass('loaded')
              .removeClass('loading');
          }
          $('#result').empty();
          $('#result').append(
            $('<h1></h1>').html('検索結果: ' + len + '匹')
          );
          $('#result').append($('<ol></ol>'));
          for (var i = 0; i < len; i++) {
            var typeStr = '<span class="types"><span class="' + 
                  data[i]['types'][0] + '">' + 
                  TYPES_TRANSLATE[data[i]['types'][0]] + '</span>';
            if (data[i]['types'][1]) {
              typeStr += '<span class="' + data[i]['types'][1] + '">'+ 
                TYPES_TRANSLATE[data[i]['types'][1]] + '</span>';
            }
            typeStr += '</span>';

            var traitStr = '';
            if (data[i]['trait']) {
              traitStr = '<em class="trait">' + data[i]['trait'] + '</em>';
            }
            $('#result ol').append(
              $('<li></li>').html(data[i]['name'] + typeStr + traitStr)
            );
          }
        },
        error: function(){
          $('#result').empty();
          $('#result').html('error');
        }
      });
      return false;
    }
    function reset() {
      $('.effect select:nth-child(1)').val('-1');
      $('.effect select:nth-child(2)').val('less');
    }

    function getUrlQueries(hash) {
      var params_dic = {};
      var param;
      var params = hash;
      
      for (var i=0; i<params.length; i++) {
        param = params[i].split('=');
        params_dic[param[0]] = param[1];
      }

      return params_dic;
    }

    function load_from_query(hash) {
      var q = getUrlQueries(hash)
      var e, c, splited, opts;
      var swt = 0;
      reset();
      for (var k in q) {
        if (q[k].indexOf('_') !== -1) {
          splited = q[k].split('_');
          c = splited[0];
          e = splited[1];

          $('#' + k).val(e)
          $('#' + k + 'c').val(c);
        }
      }

      // backward
      if(q['evo'] || q['trt'] || q['or']) {
        if (q['evo'] === '1') {
          $('#evo').attr('checked', 'checked');
        } else {
          $('#evo').removeAttr('checked');
        }
        if (q['trt'] === '1') {
          $('#trt').attr('checked', 'checked');
        } else {
          $('#trt').removeAttr('checked');
        }
        if (q['or'] === '1') {
          $('#or').attr('checked', 'checked');
        } else {
          $('#or').removeAttr('checked');
        }
      }
      // end backword

      if (q['opt']) {
        opts = q['opt'].split('+');
        if ($.inArray('evo', opts) !== -1) {
          $('#evo').attr('checked', 'checked');
        } else {
          $('#evo').removeAttr('checked');
        }
        if ($.inArray('trt', opts) !== -1) {
          $('#trt').attr('checked', 'checked');
        } else {
          $('#trt').removeAttr('checked');
        }
        if ($.inArray('or', opts) !== -1) {
          $('#or').attr('checked', 'checked');
        } else {
          $('#or').removeAttr('checked');
        }
      }

      if (q['gen'] !== undefined) {
        var gen_values = q['gen'].split('_');
        $('#gen').val(gen_values[1]);
        $('#genc').val(gen_values[0]);
      } else {
        $('#gen').val('1');
        $('#genc').val('after');
      }

      if (q['opt'] || q['gen']) {
        $('.options > ul > li').addClass('show');
      }

      load();
    }

    function refer() {
      var query_str,  val, s, gen_values;
      var query_list = [];
      var opt_list = [];

      if ($('#evo').attr('checked') === 'checked') {
        opt_list.push('evo');
      }
      if ($('#trt').attr('checked') === 'checked') {
        opt_list.push('trt');
      }
      if ($('#or').attr('checked') === 'checked') {
        opt_list.push('or');
      }
      // if ($('#gen').val() !== '1' || $('#genc').val() !== 'after') {
      //   opt_list.push($('#genc') + '_' + $('#gen').val())
      // }
      if (opt_list.length) {
        query_list.push('opt=' + opt_list.join('+'));
      }
      if ($('#gen').val() !== '1' || $('#genc').val() !== 'after') {
        gen_values = 'gen=' + $('#genc').val() + '_' + $('#gen').val();
        query_list.push(gen_values);
      }

      for (var i=0; i<TYPES_LENGTH; i++) {
        val = $('#' + TYPES[i]).val()
        if (val !== '-1') {
          s = TYPES[i] + '=' + $('#' + TYPES[i] + 'c').val() + '_' + val;
          query_list.push(s);
        }
      }

      query_str = query_list.join('&');
      window.location.href = BASE_URL + "#!/" + query_str;
    }

    $('.options .label').click(function() {
      $('.options > ul > li').toggleClass("show");
    });

    $('select, .options input').change(function() {refer(); return false;});
    $('#situation').submit(function() {refer(); return false;});

    $('#reset').click(function() {reset(); return false;});

    $(window).hashchange(function() {
      var hash, hash_index, hash_str;
      hash_index = window.location.href.indexOf('/#!/');
      hash_str = window.location.href.slice(hash_index + 4);
      if (hash_index !== -1) {
        if (hash_str) {
          hash = hash_str.split('&');
          load_from_query(hash);
          changeTitle(hash);
          tweetlink("tweetlink");
        }
        else {
          reset();
        }
      }
      else {
        window.location.href = BASE_URL + '#!/';
      }
    });
    $(window).hashchange();
  });
})(jQuery);
