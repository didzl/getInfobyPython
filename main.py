import requests
from flask import Flask, render_template, request

base_url = "http://hn.algolia.com/api/v1"

# This URL gets the newest stories.
new = f"{base_url}/search_by_date?tags=story"

# This URL gets the most popular stories
popular = f"{base_url}/search?tags=story"


# This function makes the URL to get the detail of a storie by id.
# Heres the documentation: https://hn.algolia.com/api
def make_detail_url(id):
  return f"{base_url}/items/{id}"

db = {}
app = Flask("DayNine")


def get_info(id):
  comments = []
  url = f'https://hn.algolia.com/api/v1/items/{id}'
  result = requests.get(url)
  json = result.json()
  title = json['title']
  point = json['point']
  author = json['author']
  url = json['url']
  children = json['children']
  for child in children:
    user = child['author']
    if user is None:
      user = 'None'
    text = child['text']
    comment = {
      'author': user,
      'text' : text
    }
    comments.append(comment)
  info = {
    'title' : title,
    'point' : point,
    'author' : author,
    'url' : url,
    'comment' : comments
  }
  return info




def get_article(name):
  if name =='new':
    url = new
  else:
    url = popular
  
  news = []
  result = requests.get(url)
  json = result.json()['hits']
  articles = json
  for article in articles:
    if article is not None:
      title = article['title']
      url = article['url']
      point = article['point']
      author = article['author']
      comment = article['num_comments']
      id = article['objectID']
      article_detail = {
        'title' :title,
        'url' : url,
        'point' : point,
        'author' : author,
        'comment' : comment,
        'id' : id
      }
      news.append(article_detail)

  return news

@app.route('/')
def index():
  order_by = request.args.get('order_by', default='popular')
  getDB = db.get(order_by)
  if getDB:
    news = getDB
  else:
    news = get_article(order_by)
    db[order_by] = news
  return render_template('index.html', order_by = order_by, news = news)



@app.route('/<id>')
def detail(id):
  coms = get_info(id)
  title = coms['title']
  point = coms['point']
  author = coms['author']
  url = coms['url']
  comments = coms['comment']
  return render_template('detail.html',title= title, author = author, url = url, point= point, comments = comments)


app.run(host="0.0.0.0")