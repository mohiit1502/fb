from flask import request, Response, render_template, send_from_directory
from mini_amazon import app
from mini_amazon.models.product import Product, MongoProduct
from mini_amazon.models.user import User, MongoUser

mongo_product = MongoProduct()
mongo_user = MongoUser()
product_list = []


@app.route('/health', methods=['GET'])
def health():
    return 'healthy'


@app.route('/api/product', methods=['POST', 'GET'])
def products():
    if request.method == 'GET':
        matches = mongo_product.search_by_name(request.args['name'])
        output_type = request.args.get('output_type', None)
        if output_type == 'html':
            return render_template('results.html', results=matches, query=request.args['name'], user_id=request.args.get('user_id'))
        else:
            return Response(str(matches), mimetype='application/json', status=200)
    elif request.method == 'POST':
        product = dict()
        operation_type  = request.form.get('operation_type', None)
        if operation_type is not None:
            if operation_type == 'add':
                product['_id'] = request.form['_id']
                product['name'] = request.form['name']
                product['description'] = request.form['description']
                product['price'] = request.form['price']
                # p = Product(12, request.form['name'], request.form['description'], request.form['price'])
                mongo_product.save(product)
                return Response(str({'status': 'success'}), mimetype='application/json', status=200)
            elif operation_type == 'delete':
                _id = request.form.get('_id')
                mongo_product.delete_by_id(_id)
                return Response(str({'status': 'success'}), mimetype='application/json', status=200)
            elif operation_type == 'update':
                p = Product(request.form['name'], request.form['description'], request.form['price'])
                mongo_product.update_by_id(request.form['_id'], p)
                return Response(str({'status': 'success'}), mimetype='application/json', status=200)
                db.products.update_one(update={'$set': product}, filter={'name': currentname})
                return Response(str({'status': 'success'}), mimetype='application/json', status=200)


@app.route('/listProducts', methods=['GET'])
def list_all():
    matching_prods = mongo_product.list_all_products()
    matches = []
    for prod in matching_prods:
        matches.append(prod)
    return Response(str(matches), mimetype='application/json', status=200)


@app.route('/addStuff', methods=['GET'])
def add_stuff():
    mongo_product.add_stuff()
    return Response(str({'status': 'success'}), mimetype='application/json', status=200)


@app.route('/api/user/<action>', methods=['GET', 'POST'])
def user_actions(action):
    if action == 'login':
        user = User(None, None, request.form.get('username'), request.form.get('password'))
        is_valid = mongo_user.authenticate(user)
        name = mongo_user.find_user_name_by_credentials(user)
        if is_valid is not None and is_valid:
            return render_template('profile.html', sign_up_msg="Welcome to Mini-Amazon", name = name if name is not None else "Anonymous", user_id=mongo_user.get_id_by_username(request.form.get('username')))
        else:
            return render_template("index.html", message="Invalid Username/Password")
    elif action == 'signup':
        user = dict()
        user['name'] = request.form.get('name')
        user['email'] = request.form.get('email')
        user['username'] = request.form.get('username')
        user['password'] = request.form.get('password')
        does_user_exist = mongo_user.check_if_user_exists(request.form.get('username'))
        if does_user_exist:
            return render_template("index.html", user_exists_msg="Username exists, please enter a different user name!")
        else:
            mongo_user.save(user)
            return Response(str({'status' : 'User Added!'}), mimetype='application/json', status=200)

    else:
        status = {
            'status' : 'Invalid Action'
        }
        return Response(str(status), mimetype='application/json', status=400)


@app.route('/listUsers', methods=['GET'])
def list_all_users():
    matching_users = mongo_user.list_all_users()
    matches = []
    if matching_users is not None:
        for user in matching_users:
            matches.append(user)
    return render_template('users.html', results=matches)


@app.route('/addUsers', methods=['GET'])
def add_users():
    mongo_user.add_stuff()
    return Response(str({'status': 'success'}), mimetype='application/json', status=200)

@app.route('/api/cart', methods=['GET','POST'])
def cart():
   if request.args.get('op_type') == 'getcart':
       userId = request.args.get('user_id')
       matched_ids = mongo_user.get_usercart_by_userid(userId)
       matches = mongo_product.get_product_list_from_product_ids(matched_ids)
       return render_template('cart.html', user_id=userId, results=matches)
   elif request.args.get('op_type') == 'addToCart':
       pass
   else:
       user_id = request.args.get('user_id',None)
       product_id = request.args.get('product_id', None)

       user= mongo_user.get_by_id(user_id)
       success = mongo_user.add_to_cart(user_id,product_id)
       user_data = mongo_user.get_by_id(user_id)

       return render_template('profile.html',name=user_data['name'],user_id=user_id)


# @app.route('/admin.html')
# def admin_tasks():
#     return render_template('../../static/admin.html')
