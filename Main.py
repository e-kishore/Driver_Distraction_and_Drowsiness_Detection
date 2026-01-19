from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
# from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
# from werkzeug.utils import secure_filename

import mysql.connector
import sys, fsdk, math, ctypes, time

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
    import LiveRecognition as liv

    # liv.att()
    # dname = session['name']
    # print(dname)
    del sys.modules["LiveRecognition"]

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ownertb")
    data = cur.fetchall()
    # return render_template('AdminHome.html', data=data)

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
            # return render_template('index.html')
            return 'Username or Password is wrong'
        else:
            session['mob'] = data[2]
            session['email'] = data[3]

            print(data[3])

            import LiveRecognition1 as liv
            del sys.modules["LiveRecognition1"]

        return check()
        # return render_template('DriverHome.html')


def check():
    username = session['dname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1drowsydb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from checktb where UserName='" + username + "'")
    data = cursor.fetchone()
    if data is None:

        return 'Face Mismatch'
    else:

        import cv2
        from ultralytics import YOLO

        dd1 = 0

        # Load the YOLOv8 model
        model = YOLO('runs/detect/drivernew/weights/best.pt')
        # Open the video file
        # video_path = "path/to/your/video/file.mp4"
        cap = cv2.VideoCapture(0)

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = model(frame, conf=0.3)
                for result in results:
                    if result.boxes:
                        box = result.boxes[0]
                        class_id = int(box.cls)
                        object_name = model.names[class_id]
                        print(object_name)

                        if object_name != 'awake':
                            dd1 += 1
                            print(dd1)
                        else:
                            dd1 = 0


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

        return render_template('DriverLogin.html')


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


def emotion():
    import numpy as np
    import time
    import cv2
    import os
    import numpy as np

    import threading
    import smtplib
    # import pygame
    import time
    import datetime

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    args = {"confidence": 0.5, "threshold": 0.3}
    flag = False

    labelsPath = "./yolo-coco/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")
    final_classes = ['cell phone', 'bottle', 'wine glass', 'cup', 'banana', 'apple', 'sandwich', 'pizza', 'donut']

    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
                               dtype="uint8")

    weightsPath = os.path.abspath("./yolo-coco/yolov3-tiny.weights")
    configPath = os.path.abspath("./yolo-coco/yolov3-tiny.cfg")

    # print(configPath, "\n", weightsPath)

    net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    vs = cv2.VideoCapture(0)
    writer = None
    (W, H) = (None, None)

    flag = True

    flagg = 0

    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break

        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > args["confidence"]:
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top
                    # and and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates,
                    # confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
                                args["threshold"])

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                if (LABELS[classIDs[i]] in final_classes):

                    flagg += 1
                    # print(flag)

                    if (flagg == 10):
                        flagg = 0
                        import winsound

                        filename = 'alert.wav'
                        winsound.PlaySound(filename, winsound.SND_FILENAME)

                        cv2.imwrite("alert.jpg", frame)
                        sendmail()
                        # sendmsg("9486365535", " Driver  Distraction " + LABELS[classIDs[i]])
                        sendmsg(session['mob'], session['dname'] + " Driver  Distraction " + LABELS[classIDs[i]])

                    color = [int(c) for c in COLORS[classIDs[i]]]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                                               confidences[i])
                    cv2.putText(frame, text, (x, y - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        else:
            flag = True

        cv2.imshow("Output", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # release the webcam and destroy all active windows
    vs.release()
    cv2.destroyAllWindows()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
