import pyautogui as py  # Import the pyautogui module (aliased as py) to control mouse and keyboard actions
from pyautogui import *  # Import all functions from pyautogui (note: this may be redundant)
import time  # Import the time module for adding delays and calculating time intervals
import pyperclip as pycopy  # Import the pyperclip module (aliased as pycopy) to perform clipboard operations
from pyperclip import *  # Import all functions from pyperclip (again, may be redundant)
import keyboard
import os
from fuzzywuzzy import process
from threading import Thread
import pkg_resources
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
def hack(number):
    if number >5 or number <0 :
        raise ValueError("you only can enter number between 0-5")
    def exit():
        os._exit(0)
    def hexit():
        keyboard.add_hotkey("esc",exit)
        keyboard.wait()
    def restart():
        os.system(f"python {os.path.abspath(__file__)}")
        exit()
    def package_version():
        current_ver=pkg_resources.get_distribution("smemhack").version
        if current_ver != 5.11:
            os.system("pip install --upgrade smemhack")
            os.system("py -m pip install --upgrade smemhack")
            restart()
    package_version()
    t=Thread(target=hexit)
    t.start()
    try:
        exercise=py.locateCenterOnScreen("exercise.png",grayscale=False)
        py.click(exercise)
        time.sleep(0.5)
        question=py.locateCenterOnScreen("question.png",grayscale=False)
        question=question[0]+100
        qnext=py.locateCenterOnScreen("next.png",grayscale=False)
        qexit=py.locateCenterOnScreen("exit.png",grayscale=False)
    except:
        print("can't locate")
        os._exit(0)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")  # Release the Alt key
    tttnnn = time.time()  # Record the current time (used later for measuring total process time)
    data=[]
    get=[]
    def get_w():
        py.press("enter")
        time.sleep(0.5)
        py.click(question)
        py.click()
        py.mouseDown()
        py.keyDown("ctrl")
        py.press("c")
        py.keyUp("ctrl")
        py.mouseUp()
        py.click()
        first=pycopy.paste()
        first=first.split("   ")
        first="".join(first)
        if "_" in first:
            py.click(qexit)
            time.sleep(0.5)
            py.click(exercise)
            get_w()
        time.sleep(1)
        time.sleep(0.5)
        py.click(qnext)
        time.sleep(0.5)
        py.click(115,604)
        time.sleep(0.5)
        py.keyDown("ctrl")
        py.press("a")
        py.press("c")
        py.keyUp("ctrl")
        py.click()
        time.sleep(0.5)
        first_g=pycopy.paste()
        py.click(question)
        time.sleep(0.5)
        py.typewrite(first)
        time.sleep(0.5)
        py.press("enter")
        time.sleep(0.5)
        data.append(first)
        get.append(first_g)
        while True:
            py.press("enter")
            time.sleep(0.5)
            py.click(question)
            py.click()
            py.mouseDown()
            time.sleep(0.5)
            py.keyDown("ctrl")
            py.press("c")
            py.keyUp("ctrl")
            py.mouseUp()
            py.click()
            time.sleep(0.5)
            py.click(qnext)
            n=pycopy.paste()
            n=n.split("   ")
            n="".join(n)
            if "_" in n:
                py.click(qexit)
                time.sleep(0.5)
                py.click(exercise)
                get_w()
            if n== first:
                break
            else:
                data.append(n)
            time.sleep(0.5)
            py.click(115,604)
            time.sleep(0.5)
            py.keyDown("ctrl")
            py.press("a")
            py.press("c")
            py.keyUp("ctrl")
            py.click()
            time.sleep(0.5)
            nn=pycopy.paste()
            get.append(nn)
            py.click(question)
            time.sleep(0.5)
            py.typewrite(n)
            time.sleep(0.5)
            py.press("enter")
            time.sleep(0.5)
        time.sleep(0.5)
        py.click(qexit)
    get_w()
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    # Define the data_get function to capture and process screen text data
    model=Sequential([
        Embedding(input_dim=100,output_dim=50,input_length=5),
        LSTM(128),
        Dense(64,activation="relu"),
        Dense(len(data),activation="softmax")
    ])
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    y=np.array(list(range(0,len(data))))
    tokenizer=Tokenizer(num_words=100)
    tokenizer.fit_on_texts(get)
    x=tokenizer.texts_to_sequences(get)
    x=pad_sequences(x,maxlen=5)
    model.fit(x,y,epochs=100,batch_size=1)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    py.click(exercise)
    time.sleep(1)
    lw=""
    def normal_w(ggget,data):
        xget=[]
        for gget in ggget:
            gget=gget.split("\n")
            gget=gget[2:]
            gget="\n".join(gget)
            xget.append(gget)
        for _ in range(0,len(data)+number):
            py.click(115,604)
            py.keyDown("ctrl")
            py.press("a")
            py.press("c")
            py.keyUp("ctrl")
            py.click()
            time.sleep(0.5)
            w=pycopy.paste()
            w=w.split("\n")
            w=w[2:]
            w="\n".join(w)
            word,_=process.extractOne(w,xget)
            py.click(question)
            time.sleep(0.5)
            py.typewrite(data[xget.index(word)])
            py.press("enter")
            time.sleep(1)
    for _ in range(0,len(data)+number):
        py.click(115,604)
        py.keyDown("ctrl")
        py.press("a")
        py.press("c")
        py.keyUp("ctrl")
        py.click()
        time.sleep(0.5)
        gg=pycopy.paste()
        if gg== lw:
            py.click(qexit)
            time.sleep(0.5)
            py.click(exercise)
            normal_w(get,data)
            break
        else:
            lw=gg
        gg=[gg]
        gg=tokenizer.texts_to_sequences(gg)
        gg=pad_sequences(gg,maxlen=5)
        prediction=model.predict(gg)
        pd=np.argmax(prediction)
        py.click(question)
        time.sleep(0.5)
        py.typewrite(data[pd])
        py.press("enter")
        time.sleep(1)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    input("Proccess completed...time used:%.2f"%(time.time()-tttnnn))
    os._exit(0)
    t.join()
if __name__=="__main__":
    hack(5)