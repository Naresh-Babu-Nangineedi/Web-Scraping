from flask import Flask, flash, redirect, render_template, request, url_for
from bs4 import BeautifulSoup
import requests
import re


def cinema(n):
    try:
        if n=="Horror":
            key = 'ls062635494'
        elif n=="Action":
            key = 'ls009668579'
        elif n=="Comedy":
            key = 'ls057433882'
        elif n=="Adventure":
            key = 'ls009609925'
        elif n=="Crime":
            key = 'ls009668704'


        url ='https://www.imdb.com/list/'+key+'/?sort=user_rating,desc&st_dt=&mode=detail&page=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        movie_containers=soup.find_all('div',class_= "lister-item mode-detail")
        length=len(movie_containers)
        data=[]
        for i in range(5):
                first_movie=movie_containers[i]
                first_name=first_movie.h3.a.text
                first_rating = first_movie.find('span', class_='ipl-rating-star__rating')
                first_mscore = first_movie.find('span', class_='metascore favorable')
                first_mscore = (first_mscore.text)
                data.append(first_name)
    

    except Exception as exc:
        print(exc)
        data = None
    return data


app = Flask(__name__)
@app.route('/')
def index():
    return render_template(
        'movie.html',
        data=[{'name':'Action'}, {'name':'Adventure'}, {'name':'Horror'},{'name':'Comedy'}, {'name':'Crime'},])


@app.route("/result" , methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('comp_select')
    resp = cinema(select)
    if resp:
       data = resp

    return render_template(
        'result.html',
        data=data,
        error=error)


if __name__=='__main__':
    app.run(debug=True)