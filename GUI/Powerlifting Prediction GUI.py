#importing libraries#
import PySimpleGUI as sg
from sklearn.linear_model import LinearRegression
import numpy as np
import pickle

#theme (styles / colours)#
sg.theme("DarkGreen")

#testing of pickle file#
##print("Example Of Loading Model In a Pickle File:")
##model_bench = pickle.load(open("model_bench.sav","rb"))
##pred_B_data = np.array([[244,274,107,20,100]])

##print("Prediction:",model_bench.predict(pred_B_data))



#functions#
def PredictBench(Dead,Squat,BW,Age,S):
    pred_data = [Dead,Squat,BW,Age,S] #store predictor variables
    coeff = [0.37657831, 0.15869449, 0.16271611, 0.18003004, 0.20705358] #coefficents of the Benchpress model
    intercept = -18.62240687443294 #intercept of the Benchpress model
    #pred = model_bench.predict(pred_data) #prediction to be made with sklearn (had pickle files worked)
    pred = intercept + np.sum(np.array(coeff)*np.array(pred_data)) # manual prediction calculation
    lift = "Benchpress"
    return pred,lift

def PredictDeadlift(Bench,Squat,BW,Age,S):
    pred_data = [Bench,Squat,BW,Age,S]
    coeff = [0.26578934, 0.72757238, -0.04576597,  0.10282917,  0.13281858]
    intercept = 35.07770482152151
    pred = intercept + np.sum(np.array(coeff)*np.array(pred_data))
    lift = "Deadlift"
    return pred,lift

def PredictSquat(Dead,Bench,BW,Age,S):
    pred_data = [Dead,Bench,BW,Age,S]
    print(pred_data)
    coeff = [0.49597113, 0.59499505, 0.22841687, -0.28082879, -0.10201938]
    intercept = -6.690797907730513
    pred = intercept + (np.sum(np.array(coeff)*np.array(pred_data)))
    lift = "Squat"
    return pred,lift

#layout GUI
layout = [[sg.Column(layout=[
                    [sg.Text('Enter your Squat PR (kg):')], #text fields for input fields
                    [sg.Text('Enter your Benchpress PR (kg):')],
                    [sg.Text('Enter your Deadlift PR (kg):')],
                    [sg.Text('Enter your Bodyweight (kg):')],
                    [sg.Text('Enter your Age:')],
                    [sg.Text('')],
                ], element_justification='left'), #put them to the left of the GUI
           sg.Column(layout=[
                [sg.Input(key='input1', enable_events=True)], #adjacent column with input fields
                [sg.Input(key='input2', enable_events=True)],
                [sg.Input(key='input3', enable_events=True)],
                [sg.Input(key='input4', enable_events=True)],
                [sg.Input(key='input5', enable_events=True)],
                [sg.Text(key='output', visible=True, size=(40,1),font=("Helvectica",13))], #output for predicted value
                ], element_justification='left')],
          [sg.Button('Submit as Male'),sg.Button('Submit as Female'), sg.Cancel()], #buttons to submit as Male/Female and cancel
          [sg.Text("""How To Use: 
        Enter your details into the correct fields.
        Leave the field blank you wish to predict
            (Squat, Benchpress or Deadlift)
        Press "Submit as Male" if you are male, or "Submit as Female" if you are female
        Predictions will show when you press submit
        Only enter numbers and leave one lift blank at a time""")]] #instruction text field

#instanciate window
window = sg.Window('Competing Power Lifter Score Prediction', layout)

#loop
while True:
    
    event, values = window.read()
    #when cancel is pressed, window closes as loop is broken
    if event in (None, 'Cancel'):
        break
    
###MALE PREDICTION###
    #when you press submit as male
    elif event == 'Submit as Male':
        
        #SQUAT 
        if values['input1'] == "": #if squat field is empty
            input_list = [values['input2'], values['input3'], values['input4'], values['input5'],100] #take input fields as values and store to list (100 relates to sex being male)
            try: #error checking for valid inputs
                input_list = [float(i) for i in input_list] #convert inputs to float values
                pred_list = PredictSquat(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #call prediction function for squat
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #update text to show what the prediction is
            except: #if an error (invalid field input)
                window["output"].update("Error: Please only use numbers") #tell user there is an error

        #BENCH
        elif values['input2'] == "":
            input_list = [values['input1'], values['input3'], values['input4'], values['input5'],100] #inputs
            try: #error handling
                input_list = [float(i) for i in input_list]
                pred_list = PredictBench(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #make prediction
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #output prediction
            except:

                window["output"].update("Error: Please only use numbers")
            
        #DEADLIFT
        elif values['input3'] == "":
            input_list = [values['input2'], values['input1'], values['input4'], values['input5'],100] #inputs
            try: #error handling
                input_list = [float(i) for i in input_list]
                pred_list = PredictDeadlift(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #make prediction
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #output prediction
            except:
                window["output"].update("Error: Please only use numbers")

                
###FEMALE PREDICTION###
    #works the same as male prediction
    elif event == 'Submit as Female':
        if values['input1'] == "":
            input_list = [values['input2'], values['input3'], values['input4'], values['input5'],10] #inputs (10 relates to sex being female)
            try: #error handling
                input_list = [float(i) for i in input_list]
                pred_list = PredictSquat(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #make prediction
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #output prediction
            except:
                window["output"].update("Error: Please only use numbers")

        #BENCH 
        elif values['input2'] == "":

            input_list = [values['input1'], values['input3'], values['input4'], values['input5'],10] #inputs
            try:
                input_list = [float(i) for i in input_list]
                pred_list = PredictBench(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #make prediction
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #output prediction
            except:
                window["output"].update("Error: Please only use numbers")

        #DEADLIFT
        elif values['input3'] == "":
            input_list = [values['input2'], values['input1'], values['input4'], values['input5'],10] #input values
            try:
                input_list = [float(i) for i in input_list]
                pred_list = PredictDeadlift(input_list[0],input_list[1],input_list[2],input_list[3],input_list[4]) #make predictions
                pred = pred_list[0]
                lift = pred_list[1]
                window["output"].update("We predict you can lift {:.1f}kg in the {}".format(pred,lift)) #output predictions
            except:
                window["output"].update("Error: Please only use numbers")

                
#close window when loop is broken
window.close()
