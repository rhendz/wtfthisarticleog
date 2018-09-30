// Assume field is given article
function getArticleAnalysis() {
  var url = document.getElementById("url").value
  getArticleAnalysis2(url)
};

async function getArticleAnalysis2(url) {
  $.ajax({
    url: "http://127.0.0.1:5000/" + url,
    type: "GET",
    success: function(result) {
      fillArticleBox(result);
    }
  })
}

function fillArticleBox(result) {
  const articleObject = result;
  console.log(articleObject)

  fillRelatedArticles(articleObject.relatedArticles);

  $("#title").text(articleObject.title);
  if (articleObject.author) {
    $("#author").text(articleObject.author);
  }
  $("#bias").text(articleObject.score + articleObject.magnitude);
  if (articleObject.publish_date) {
    $("#datePublished").text(articleObject.publish_date);
  }
  $("#summary").text(articleObject.summary);
  $('#mainArticleBox').removeAttr('hidden');
}

async function fillRelatedArticles(relatedArticles) {
  let count = 0;
  let articleObject;
  relatedArticles.forEach(article => {
    $.ajax({
      url: "http://127.0.0.1:5000/" + url,
      type: "GET",
      success: function(result) {
        articleObject = result;
      }
    })

    let title = "#relatedTitle" + count;
    let author = "#relatedAuthor" + count;
    let bias = "#relatedBias" + count;
    let datePublished = "#relatedDate" + count;
    let description = "#relatedDescription" + count;
    let img = "#relatedImg" + count;

    $(title).text(articleObject.title);
    if (articleObject.author) {
      $(author).text(articleObject.author);
    }
    $(bias).text(articleObject.score);
    if (articleObject.publish_date) {
      $(datePublished).text(articleObject.publish_date);
    }
    $(description).text(articleObject.summary);
    if (article.img) {
      $(img).src(img);
    }
    count++;
  });
}
