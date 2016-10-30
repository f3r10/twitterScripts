var elasticsearch = require('elasticsearch');
var client = new elasticsearch.Client({
  host: 'localhost:9200'
});


module.exports.createFilter = function (req, res){
  console.log(req.body)
  var filtro = req.body.filtro.join(" OR ")
  console.log(filtro)
  client.search({
  index: 'quitotweet5',
  type: 'tweet',
  body: {
    "query": {
      "filtered": {
        "query": {
          "query_string": {
            "query": "*",
            "analyze_wildcard": true
          }
        },
        "filter": {
          "bool": {
            "must": [
              {
                "query": {
                  "query_string": {
                    "query": "*" + filtro,
                    "analyze_wildcard": true
                  }
                }
              },
              {
                "range": {
                  "created_at": {
                    "gte": 1473000923417,
                    "lte": 1477407323417
                  }
                }
              }
            ],
            "must_not": []
          }
        }
      }
    },
    "size": 0,
    "aggs": {
      "dos": {
        "filters": {
          "filters": {
            "all": {
              "query": {
                "query_string": {
                  "query": "*",
                  "analyze_wildcard": true
                }
              }
            }
          }
        },
        "aggs": {
          "tres": {
            "significant_terms": {
              "field": "text",
              "size": 100,
              "min_doc_count": 5
            }
          }
        }
      }
    }
  }
  }).then(function (resp) {
      var hits = resp.aggregations.dos.buckets.all.tres.buckets;
      console.log(hits);
      res.status(201).json(hits);
  }, function (err) {
      console.trace(err.message);
      res.send('error query elasticsearch');
  });
}