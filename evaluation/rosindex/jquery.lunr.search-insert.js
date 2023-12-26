var convertToCSV = function(data) {
const csvContent = data.reduce((acc, result) => {
  const row = [result.distro, result.name].join(",");
  return acc + row + "\n";
}, "distro,name\n");

const encodedUri = encodeURI("data:text/csv;charset=utf-8," + csvContent);
const link = document.createElement("a");
link.setAttribute("href", encodedUri);
link.setAttribute("download", "search_result.csv");
document.body.appendChild(link);
link.click();
}

// define lunr.js search class
var LunrSearch = (function() {

function LunrSearch(input, options) {
  var self = this;
  this.$input = input;
  this.baseUrl = options.baseUrl;

  var views = $.map(options.sections, function(section) {
    return section.view;
  });
  $.when.apply($, $.map(options.sections, function(section) {
    return $.getLunrDB(section.partition, function(partition) {
      var query = self.$input.val();
      if (query) {
        var results = partition.search(query);
        // console.log("&&&",results)
        // first query in current site
        if (results.length > 0) {
          // write to csv file
          convertToCSV(results)
          return section.view.render(results, {
            baseurl: self.baseUrl
          });
        }
      }
    }).then(function(partition) {
      var query = self.$input.val();
      if (query) {
        var results = partition.search(query);
        // console.log("###",results)
        // query after first one in current site
        return section.view.render(results, {
          baseurl: self.baseUrl
        }).then(function() {
          section.view.show();
          return partition;
        });
      }
      return section.view.hide().then(function() {
        return partition;
      });
    });
  })).then(function() {
    var sections = zipArray(views, arguments);
    self.$input.bind('search', function() {
      var query = self.$input.val();
      unzipArray(sections, function(view, partition) {
        if (query) {
          var results = partition.search(query);
          // console.log("$$$",results)
          convertToCSV(results)
          return view.render(results, {
            baseurl: self.baseUrl
          }).then(function() {
            view.show();
          });
        }
        return view.hide();
      });
    });
    self.bindInputKeys();
  }).then(function() {
    if (options.ready) {
      return options.ready();
    }
  });
};
