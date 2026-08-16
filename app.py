from flask import Flask, render_template, url_for, request, redirect
from connection import connect_db
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/layout/base')
def base():
    return render_template('layout/base.html')

@app.route('/category/')
def category_index():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT*FROM categories')
    db.commit()
    db.close()
    categories = cursor
    return render_template('category/index.html', data = categories)

@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    if request.method=="POST":
        name = request.form['name']
        description = request.form['description']

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO categories(name, description)" \
        "VALUE(%s, %s)",(name, description))
        db.commit()
        db.close()
        return redirect(url_for('category_index'))
    return render_template('category/create.html')

@app.route('/category/edit/<int:id>', methods=['GET', 'POST'])
def category_update(id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM categories where id=%s', (id,))
    category = cursor.fetchone()

    if not category:
        cursor.close()
        db.close()
        return "Category not found!"

    if request.method=="POST":
        new_name = request.form['new_name']
        new_description = request.form['new_description']

        cursor.execute(
            'UPDATE categories SET name=%s, description=%s WHERE id=%s',
            (new_name, new_description, id)
        )

        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('category_index'))
    cursor.close()
    db.close()
    return render_template('category/edit.html', category=category)

@app.route('/category/delete/<int:id>', methods=['POST'])
def category_delete(id):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM categories where id=%s', (id,))
    category = cursor.fetchone()
    
    if not category:
        cursor.close()
        db.close()
        return "Category not found!"

    cursor.execute('DELETE FROM categories WHERE id=%s', (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('category_index'))


# product route
@app.route('/product/')
def index_product():
    return render_template('product/index.html')


UPLOAD_FOLDER = "uploads/products"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

@app.route('/product/create', methods=['GET', 'POST'])
def create_product():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    if request.method=="POST":
        name = request.form['productName']
        price = request.form['productPrice']
        qty = request.form['productQty']
        category_id = request.form['category_id']
        
        image = request.files.get('image')

        image_name = None

        if image and image.filename:

            if allowed_file(image.filename):

                image_name = secure_filename(image.filename)

                os.makedirs(
                    app.config["UPLOAD_FOLDER"],
                    exist_ok=True
                )

                image.save(
                    os.path.join(
                        app.config["UPLOAD_FOLDER"],
                        image_name
                    )
                )

        cursor.execute('INSERT INTO products(name, price, quantity, category_id, image)' \
        'VALUES(%s, %s, %s, %s, %s)',(name, price, qty, category_id, image_name))

        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index_product'))
    return render_template('product/create.html', categories=categories)

if __name__=="__main__":
    app.run(debug=True)