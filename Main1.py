from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request

import mysql.connector

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/DriverLogin")
def DriverLogin():
    return render_template('DriverLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/NewOwner")
def NewOwner():
    return render_template('NewOwner.html')


@app.route("/OwnerInfo")
def OwnerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb")
    data = cur.fetchall()
    return render_template('OwnerInfo.html', data=data)


@app.route("/NewDriver")
def NewDriver():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb")
    data = cur.fetchall()

    return render_template('NewDriver.html', company=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' or request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/newdriver", methods=['GET', 'POST'])
def newdriver():
    if request.method == 'POST':
        uname = request.form['uname']
        company = request.form['company']
        dno = request.form['dno']
        ano = request.form['ano']
        exp = request.form['exp']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM ownertb where  CompanyName='" + company + "'")
        data = cursor.fetchone()

        if data:
            Mobile = data[3]
            Email = data[4]
            Address = data[5]


        else:
            return 'Incorrect username / password !'
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + company + "','" + Mobile + "','" + Email + "','" + Address + "','" + dno + "','" + ano + "','" + exp + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
    return render_template("DriverLogin.html")


@app.route("/newowner", methods=['GET', 'POST'])
def newowner():
    if request.method == 'POST':
        oname = request.form['oname']
        cname = request.form['cname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into ownertb values('','" + oname + "','" + cname + "','" + mobile + "','" + email + "','" + address + "')")
        conn.commit()
        conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb")
    data = cur.fetchall()
    return render_template('OwnerInfo.html', data=data)


@app.route("/driverlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['dname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
        cursor = conn.cursor()
        cursor.execute("truncate  table checktb ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            return 'Username or Password is wrong'
        else:
            session['mob'] = data[2]
            session['email'] = data[3]

            print(data[3])

            import cv2
            from ultralytics import YOLO

            dd1 = 0

            # Load the YOLOv8 model
            model = YOLO('runs/detect/Driver/weights/best.pt')
            # Open the video file
            # video_path = "path/to/your/video/file.mp4"
            cap = cv2.VideoCapture(0)

            # Loop through the video frames
            while cap.isOpened():
                # Read a frame from the video
                success, frame = cap.read()

                if success:
                    # Run YOLOv8 inference on the frame
                    results = model(frame, conf=0.4)
                    for result in results:
                        if result.boxes:
                            box = result.boxes[0]
                            class_id = int(box.cls)
                            object_name = model.names[class_id]
                            print(object_name)

                            if object_name != 'awake':
                                dd1 += 1
                                print(dd1)

                            if dd1 == 50:
                                dd1 = 0

                                import winsound

                                filename = 'alert.wav'
                                winsound.PlaySound(filename, winsound.SND_FILENAME)

                                annotated_frame = results[0].plot()

                                cv2.imwrite("alert.jpg", annotated_frame)
                                sendmail()
                                sendmsg(session['mob'], "Driver Action For:" + object_name)

                    # Visualize the results on the frame
                    annotated_frame = results[0].plot()

                    # Display the annotated frame
                    cv2.imshow("YOLOv8 Inference", annotated_frame)

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
            # Release the video capture object and close the display window
            cap.release()
            cv2.destroyAllWindows()

        return render_template('DriverHome.html')


def examvales1():
    vid = session['dname']
    Email = session['email']
    Phone = session['mob']

    return vid, Email, Phone


def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = session['email']

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Drowsy Driver Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
