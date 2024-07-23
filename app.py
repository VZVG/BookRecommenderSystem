from flask import Flask, render_template,request
import pickle
import numpy as np
import pandas as pd

with open('popular.pkl', 'rb') as file:
    popular_df = pd.read_pickle(file)

with open('pt.pkl', 'rb') as file1:
    pt = pd.read_pickle(file1)    

with open('books.pkl', 'rb') as file2:
    books = pd.read_pickle(file2)

with open('similarity_scores.pkl', 'rb') as file3:
    similarity_scores = pd.read_pickle(file3)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_ratings'].to_list()
                           )

@app.route('/index')
def home_ui():
    return render_template('index.html',
                           book_name=popular_df['Book-Title'].to_list(),
                           author=popular_df['Book-Author'].to_list(),
                           image=popular_df['Image-URL-M'].to_list(),
                           votes=popular_df['num_ratings'].to_list(),
                           rating=popular_df['avg_ratings'].to_list()
                           )

@app.route('/contact')
def contact_ui():
    return render_template('contact.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')



@app.route('/recommend_books',methods = ['POST'])
def recommend():
    try:
        user_input = request.form.get('user_input')
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]

            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

            data.append(item)

        print(data)
        return render_template('recommend.html',data=data)
    except:
        return render_template('recommend.html', data=[])

if __name__ == '__main__':
    app.run(debug=True)
