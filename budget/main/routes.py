from flask import render_template, request, Blueprint  # Blueprint allows us to point to application components
from budget.models import Post, ActualPost  # import the database models (tables)

main = Blueprint('main', __name__)  # instantiate the main Blueprint


# creating the main routes
@main.route("/home")  # the route decorator allows Flask to pass data to and from the frontend
def index():
    return render_template('home.html') # Blueprint allows us to create application components


@main.route("/home")
def home():
    return render_template('home.html')


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/planned", methods=['GET', 'POST'])
def planned():
    """This function queries the Post table and returns the Planned entries in planned.html"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.id.asc()).paginate(page=page, per_page=30)
    return render_template('planned.html', posts = posts, legend = 'Planned Budget')


@main.route("/actual", methods=['GET', 'POST'])
def actual():
    """This function queries the ActualPost table and returns the Actuals in actual.html"""
    page = request.args.get('page', 1, type=int)
    actual_posts = ActualPost.query.order_by(ActualPost.id.asc()).paginate(page=page, per_page=30)
    return render_template('actual.html', actual_posts = actual_posts, legend = 'Actual Amounts')
