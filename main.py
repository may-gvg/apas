from flask import Flask, render_template, redirect, url_for, request, flash, abort
import tmdb_client
import random
import datetime


app = Flask(__name__)
app.secret_key = b'my-secret'


FAVORITES = set()

@app.route('/')
def homepage():
    args = ""
    return render_template("homepage.html", args=args)

@app.route('/list')
def list_page():
    args = ""
    return render_template("list.html", args=args)

@app.route('/tuple')
def tuple_page():
    args = ""
    return render_template("tuple.html", args=args)

@app.route('/set')
def set_page():
    args = ""
    return render_template("set.html", args=args)


@app.route('/dict')
def dict_page():
    args = ""
    return render_template("dict.html", args=args)


@app.route('/text')
def text_page():
    args = ""
    return render_template("text.html", args=args)


@app.route('/numbers')
def numbers_page():
    args = ""
    return render_template("numbers.html", args=args)


@app.route('/bool')
def bool_page():
    args = ""
    return render_template("bool.html", args=args)




@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    data = request.form
    movie_id = data.get('movie_id')
    movie_title = data.get('movie_title')
    if movie_id and movie_title:
        FAVORITES.add(movie_id)
        flash(f'Dodano film {movie_title} do ulubionych!')
    return redirect(url_for('homepage'))


@app.route("/favorites/")
def show_favorites():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    for movie in movies:
        movie['image'] = get_homepage_cover_image(movie)

    return render_template("homepage.html", movies=movies, filtry=get_filtry())


def get_filtry():
    filtry = {"popular": "Popular", "top_rated": "Top Rated", "now_playing": "Now Playing", "upcoming": "Upcoming" }
    return filtry


def get_homepage_cover_image(movie):
    return tmdb_client.get_poster_url(movie['poster_path'], "w780")
    pass




@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    if not details.get('success'):
        abort(404)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    movie_images = tmdb_client.get_movie_images(movie_id)
    for actor in cast:
        actor['image'] = tmdb_client.get_poster_url(actor['profile_path'], "w185")
    if movie_images.get('backdrops'):
        selected_backdrop = random.choice(movie_images['backdrops'])
        image = tmdb_client.get_poster_url(selected_backdrop['file_path'], "w780")
    else:
        selected_backdrop = ""
        image = ""
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop, image=image)


@app.route('/search')
def search():
    search_query = request.args.get("q", "")
    if search_query:
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    for movie in movies:
        movie['image'] = get_homepage_cover_image(movie)
    return render_template("search.html", movies=movies, search_query=search_query)


@app.route('/today')
def today():
    movies = tmdb_client.get_airing_today()
    for movie in movies:
        movie['image'] = get_homepage_cover_image(movie)
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)


if __name__ == '__main__':
    app.run(debug=True)