# Stock Predictor

Predict stocks for Apple, Amazon, Google, Microsoft and Nvidia!

Also, practice investing smartly in the stock market.

# Running Program

Create a folder containing all files.

Create a virtual environment in the folder using the command:
```
python -m venv <my-env>
```
\<my-env> should be replaced by the folder name.

Then, activate the virtual environment using the script belonging to your operating system:

For Linux Based OS Or Mac-OS:
```
source <my_env>/bin/activate
```

For Windows With CMD:
```
.\<my_env>\Scripts\activate.bat
```

For Windows With Powershell:
```
.\<my_env>\Scripts\activate.ps1
```

If not already present, add a file called '.env' to the main directory with the following content:
```
SECRET_KEY="<YOUR-SECRET-KEY>"
```
Replace \<YOUR-SECRET-KEY> with your own key to enable flask sessions.

To install all necessary modules, run the following command:
```
pip install -r requirements.txt
```

To create the necessary databases, run:
```
python data/init_db.py
```

To run the application locally, use:
```
flask --app predictor run
```

Then navigate to localhost:5000

A loading screen should appear. The first load may take up to twenty minutes so the machine learning algorithm may update accordingly. Please be patient.

After the initial update to the database, the application should allow the user to view stock predictions, as well as participate in the stock simulation as long as they have an associated account.

# Live Link
https://stock-predictor-624177250442.us-west1.run.app/home
