from flask import Flask,render_template,request,redirect
import mysql.connector

app2 = Flask(__name__,template_folder="template")

conn=mysql.connector.connect(host="remotemysql.com",user="IMZ0mJ03ut",password="Ohmo8OHuAX",database="IMZ0mJ03ut")
cursor=conn.cursor()

Allocation=[]
Max=[]
Need=[]
Available=[]

@app2.route('/')
def deadlock():
    return render_template('deadlock.html')

@app2.route('/allocation',methods=['POST','GET'])
def allocation():
    global Allocation
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        process =request.form.get('p')
        resource1 =request.form.get('r1')
        resource2 = request.form.get('r2')
        resource3 = request.form.get('r3')
        cursor.execute("""INSERT INTO `Allocation` (`process`,`resource1`,`resource2`,`resource3`) VALUES('{}','{}','{}','{}')""".format(process,resource1,resource2,resource3))
        conn.commit()
    cursor.execute("SELECT * FROM `Allocation`")
    Allocation = cursor.fetchall()
    return redirect('/')

@app2.route('/max',methods=['POST','GET'])
def max():
    global Max
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        process =request.form.get('p')
        resource1 =request.form.get('r1')
        resource2 = request.form.get('r2')
        resource3 = request.form.get('r3')
        cursor.execute("""INSERT INTO `Max` (`process`,`resource1`,`resource2`,`resource3`) VALUES('{}','{}','{}','{}')""".format(process,resource1,resource2,resource3))
        conn.commit()
    cursor.execute("SELECT * FROM `Max`")
    Max = cursor.fetchall()
    return redirect('/')

@app2.route('/need',methods=['POST','GET'])
def need():
    global Need
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        process =request.form.get('p')
        resource1 =request.form.get('r1')
        resource2 = request.form.get('r2')
        resource3 = request.form.get('r3')
        cursor.execute("""INSERT INTO `Need` (`process`,`resource1`,`resource2`,`resource3`) VALUES('{}','{}','{}','{}')""".format(process,resource1,resource2,resource3))
        conn.commit()
    cursor.execute("SELECT * FROM `Need`")
    Need = cursor.fetchall()
    return redirect('/')

@app2.route('/available',methods=['POST','GET'])
def available():
    global Available
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        resource1 =request.form.get('r1')
        resource2 = request.form.get('r2')
        resource3 = request.form.get('r3')
        cursor.execute("""INSERT INTO `Available` (`resource1`,`resource2`,`resource3`) VALUES('{}','{}','{}')""".format(resource1,resource2,resource3))
        conn.commit()
    cursor.execute("SELECT * FROM `Available`")
    Available = cursor.fetchall()
    bankers_algo()
    return render_template('thankyou.html')

def issafe(process,work):
    for i in range(3):
        if Need[process][i+1] > work[i]:
            return False
    return True

def bankers_algo():
    work=list(Available[0])
    n = len(Allocation)
    finish = []
    safe_seq=[]
    for i in range(n):
        finish.append(False)

    count = 0

    while (count < n):
        t = 0
        for process in range(n):
            if (finish[process] == False and issafe(process,work)):
                count = count + 1
                t = 1
                finish[process] = True
                safe_seq.append(process)
                for j in range(3):
                    work[j] = work[j] + Allocation[process][j + 1]
        if t == 0:
            break
    if (count == n):
        print("\nSafe sequence is\n")
        for i in range(n):
            print(safe_seq[i])
    else:
        print("\nDeadlock occured")

if __name__ == "__main__":
    app2.run(debug=True)
