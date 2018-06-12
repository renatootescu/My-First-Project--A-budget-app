from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)  # modules required to create the routes for the forms to be filled in
from flask_login import current_user, login_required  # modules that are used to ensure the user is logged in
from budget import db  # the database
from budget.models import Post, ActualPost, GraphData  # GraphData function, used to generetate graphs queries the database. Post (planned data) and ActualPost (Actuals) are the db tables
from budget.posts.forms import PostForm, PostActualForm  # the forms that will be used
import itertools  # module that provides facilities to iterate easier through data structures
import pygal  # module used to generate SVG graphs


posts = Blueprint('posts', __name__)  # Blueprint allows us to create the posts application component


@posts.route("/post/new", methods=['GET', 'POST'])  # the route decorator allows Flask to pass data to and from the frontend
@login_required
def new_post():
    """function for adding new Planned entries in the budget"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, category=form.category.data
                    , name=form.name.data, planned_amount_month=form.planned_amount_month.data
                    , date_period=form.date_period.data
                    , comments=form.comments.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.planned'))
    return render_template('create_post.html', title='Planned',
                           form=form, legend='New Planned Amount')  # pass the data to the create_post template


@posts.route("/post/new_actual", methods=['GET', 'POST'])
@login_required
def new_actual_post():
    """function for adding new Actual amounts in the budget"""
    form = PostActualForm()
    if form.validate_on_submit():
        actualpost = ActualPost(title_actual=form.title_actual.data, category_actual=form.category_actual.data
                    , actual_amount_name=form.actual_amount_name.data.name
                    , actual_amount=form.actual_amount.data, date_posted=form.date_posted.data
                    , comments=form.comments.data, actual_author=current_user)
        db.session.add(actualpost)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.actual'))
    return render_template('create_actual_post.html', title='Actual',
                           form=form, legend='New Actual Amount')


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_planned_post(post_id):
    """function for updating Planned entries"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.category = form.category.data
        post.name = form.name.data
        post.planned_amount_month = form.planned_amount_month.data
        post.comments = form.comments.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.planned', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.category.data = post.category
        form.name.data = post.name
        form.planned_amount_month.data = post.planned_amount_month
        form.comments.data = post.comments
    return render_template('create_post.html', title='Update Planned',
                           form=form, legend='Update Planned')


@posts.route("/post/<int:post_id>/update_actual", methods=['GET', 'POST'])
@login_required
def update_actual_post(post_id):
    """function for updating Actuals"""
    post = ActualPost.query.get_or_404(post_id)
    if post.actual_author != current_user:
        abort(403)
    form = PostActualForm()
    if form.validate_on_submit():
        post.title_actual = form.title_actual.data
        post.category_actual = form.category_actual.data
        post.actual_amount_name = form.actual_amount_name.data.name
        post.actual_amount = form.actual_amount.data
        post.comments = form.comments.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.actual', post_id=post.id))
    elif request.method == 'GET':
        form.title_actual.data = post.title_actual
        form.category_actual.data = post.category_actual
        form.actual_amount_name.data = post.actual_amount_name
        form.actual_amount.data = post.actual_amount
        form.comments.data = post.comments
    return render_template('create_actual_post.html', title='Update Actual',
                           form=form, legend='Update Actual')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_planned_post(post_id):
    """function to delete Planned entries"""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.planned', post_id=post.id))


@posts.route("/post/<int:post_id>/delete_actual", methods=['POST'])
@login_required
def delete_actual_post(post_id):
    """function to delete Actuals"""
    post = ActualPost.query.get_or_404(post_id)
    if post.actual_author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.actual', post_id=post.id))


@posts.route("/home")
def graphing():
    """function that creates teh graphs used to visualize the db data"""
    data_planned, data_actual = GraphData()  # instantiating the data variables generated with the GraphData function

    # create list variables that will be used to manipulate the data
    title_planned = []
    category_planned = []
    value_planned = []
    title_actual = []
    category_actual = []
    value_actual = []
    planned = []
    actual = []
    planned_category = []
    actual_category = []

    # manipulate the data to be displayed in teh graph
    for planned_row in data_planned:
        title_planned.append(planned_row[2])  # filling the list with data present only on index [2]. These are the names (Salary, Car, Food, Bills, etc.)
        category_planned.append(planned_row[1])  # filling the list with data present only on index [1]. These are the categories (Revenue, Expense, Savings)
        value_planned.append(planned_row[3])  # filling the list with data present only on index [3]. These are the amounts.
        planned_list = zip(title_planned, value_planned)  # combining the data in one data structure: nested tuples in a list, e.g. [('name', amount), ('name2', amount2)]
        category_planned_list = zip(category_planned, value_planned)

        # iterating through the lists generated above to make sure that tah tuples that have the same data on index [0] are combined and the data (float) on index [1] is summed up.
        for key, group in itertools.groupby(sorted(planned_list), lambda x: x[0]):
            asum_planned = 0
            for i in group:
                asum_planned += i[1]
            planned.append((key, asum_planned))

        for key, group in itertools.groupby(sorted(category_planned_list), lambda x: x[0]):
            asum_planned_category = 0
            for i in group:
                asum_planned_category += i[1]
            planned_category.append((key, asum_planned_category))

    # transforming the generated data into dictionaries to be easily passed to the graphs
    planned_dict = dict(planned)
    planned_category_dict = dict(planned_category)

    for actual_row in data_actual:
        title_actual.append(actual_row[2])
        category_actual.append(actual_row[1])
        value_actual.append(actual_row[3])
        actual_list = zip(title_actual, value_actual)
        category_actual_list = zip(category_actual, value_actual)

        for key, group in itertools.groupby(sorted(actual_list), lambda x: x[0]):
            asum_actual = 0
            for i in group:
                asum_actual += i[1]
            actual.append((key, asum_actual))

        for key, group in itertools.groupby(sorted(category_actual_list), lambda x: x[0]):
            asum_actual_category = 0
            for i in group:
                asum_actual_category += i[1]
                actual_category.append((key, asum_actual_category))

    actual_dict = dict(actual)
    actual_category_dict = dict(actual_category)

    graph = pygal.Bar(title=u'Total Planned vs Total Actual by Category')  # generating the empty bar graph
    graph.x_labels = set(category_planned)  # add labels to the graph
    graph.add('Planned', planned_category_dict)  # add the planned budget data
    graph.add('Actual', actual_category_dict)  # add the actuals data
    graph_data = graph.render_data_uri()  # render the graph with the data

    graph_all = pygal.Bar(title=u'Planned Budget vs Actual Amounts per Item')
    graph_all.x_labels = title_planned
    graph_all.add('Planned', planned_dict)
    graph_all.add('Actual', actual_dict)
    graph_all_data = graph_all.render_data_uri()

    return render_template('home.html', graph_data=graph_data, graph_all_data=graph_all_data)  # pass the graphs to the home template
