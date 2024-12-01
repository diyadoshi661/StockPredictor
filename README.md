# Stock Predictor

Predict stocks for Apple, Amazon, Google, Microsoft and Nvidia!

Also, practice investing smartly in the stock market.

# Running Program

Create a folder containing all files.

Create a virtual environment in the folder using the command
```
python -m venv my-env
```
, then activate the virtual environment using the script belonging to your operating system.

Run 
```
pip install -r requirements.txt
```
to install all necessary modules.

Run
```
flask --app predictor run
```
to run the application locally.

Then navigate to localhost:5000

A loading screen should appear. The first load may take up to twenty minutes so the machine learning algorithm may update accordingly. Please be patient.

After the initial update to the database, the application should allow the user to view stock predictions, as well as participate in the stock simulation as long as they have an associated account.

# Live Link