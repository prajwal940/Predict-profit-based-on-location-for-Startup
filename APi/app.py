# importing the neccessary libraries
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
import pickle


# loading the trained model pickle file in (read binary)rb mode
model = pickle.load(open("Label.pkl","rb"))

# creation of an instance of the app in the current working module(__name__)
app = Flask(__name__)

CORS(app)   # Enabling Cross Origin Resource Sharing
# If CORS is not used, an error will be displayed mentioning that the access request for connection is blocked by CORS policy.


# fetching the inputs and displaying of the predicted output will be done in this function
@app.route("/predict_data",methods=['POST'])
def predict_data():
    try:
        # fetching data entered in the form
        data = request.json
        

        # segregating the inputs
        rd = data['rd_spend']
        admin = data['administration']
        market = data['marketing']
        state = data['state']

        # checking for values entered by user for negative values
        errrd =  True if float(rd)<0 else False
        errad =  True if float(admin)<0 else False
        errmar =  True if float(market)<0 else False

        if errrd or errad or errmar :
            return jsonify({"error":"invalid literal entered"}),500
        
        
        # encoding the state entered in the form according to that given by the model
        if state == "California":
            state = 0
        elif state == "New York":
            state = 1
        elif state == "Florida":
            state = 2
        

        # typecasting the fetched inputs since they are strings and model takes floats        
        fetched = [[float(rd),float(admin),float(market),state]]


        # storing predicted output
        prediction = model.predict(fetched)


        # formatting the output to be displayed only upto 2 decimal places
        output = '{0:.{1}f}'.format(prediction[0][0],2)


        # The fetched inputs are top be displayed back on the result page, therefore, converting the states back to strings
        if state == 0:
            state = "California"
        elif state == 1:
            state = "New York"
        elif state == 2:
            state = "Florida"
            

        # we want to display the output in a table format, therefore converting the output to dict to be sent to the react
        final = {"R&D spend": rd, "Administration": admin, "Marketing": market, "State": state, "Predicted Profit": output}

        return jsonify(final)
        # return render_template("result.html",result=final)
    
    except Exception as e:
        return jsonify({'error':str(e)}), 500



# running the application
if __name__ == '__main__':
    app.run(debug = True)
