from flask import Flask
from flask import render_template,redirect,url_for,request
from flask import jsonify
from bson.objectid import ObjectId

app=Flask(__name__)


# database
from pymongo import MongoClient

client = MongoClient("")

db=client.get_database("cabs")

collection =db.get_collection("items")
#database


@app.route('/',methods=['GET'])
def cabs():
    cabs_d=collection.find()
    return render_template("index.html",allcabs=cabs_d)

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        fn=request.form
        data={
            "s_loc":fn['s_loc'],
            "d_loc":fn['d_loc'],
            "name":fn["name"],
            "p_no":fn["p_no"],
            "vehicle":fn['vehicle'],
            "money":fn['money'],
            't_d':fn['t_d'],
            'pk_add':fn['pk_add'],
        }
        
        response=collection.insert_one(data)
        print(response,"working")
        return redirect("/")
    else:
        return render_template("add.html")

@app.route('/adminpage',methods=['GET','POST'])
def login():
    cabs_d=collection.find()
    return render_template('adminpage.html',allcabs=cabs_d)


@app.route('/login',methods=['GET'])
def page():
    return render_template('admin.html')


@app.route('/del/<id>',methods=['PUT'])
def delit(id):
    x= collection.delete_one({'_id':ObjectId(id)})
    print(x)
    return jsonify(posts={"data":"ok"})

@app.route('/service-worker.js')
def sw():
    return app.send_static_file('service-worker.js')


if __name__ == '__main__':
    app.run(host="localhost",port=5000,debug=True)
