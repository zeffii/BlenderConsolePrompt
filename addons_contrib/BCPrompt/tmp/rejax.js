marked.setOptions({
  renderer: new marked.Renderer(),
  gfm: true,
  tables: true,
  breaks: false,
  pedantic: false,
  sanitize: true,
  smartLists: true,
  smartypants: false
});

// console.log(marked('I am using __markdown__.'));
function draw_content(rawhtml){
    var _div4 = d3.select("#display");
    _div4.html(rawhtml);
}

$(document).ready(function(e) {
    rawdata = jsonObject.items;
    rawhtml = marked(rawdata);
    draw_content(rawhtml);
});
