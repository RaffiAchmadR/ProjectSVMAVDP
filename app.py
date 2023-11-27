from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# Load the pre-trained decision tree model
model = joblib.load('model.pkl')
def convert_categorical(value):
    banding_harga = {'Tidak': 0, 'Ya': 1}

    # Use the provided mapping to convert categorical value to numeric
    if 'banding_harga' in value:
        return banding_harga.get(value['banding_harga'], None)

    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user input from the form
        belanja_online_sebulan = request.form['belanja_online_sebulan']
        belanja_offline_sebulan = request.form['belanja_offline_sebulan']
        pengaruh_ecommerce = request.form['pengaruh_ecommerce']
        cari_produk = request.form['cari_produk']
        banding_harga = request.form['banding_harga']
        
        # Convert categorical data to numeric
        input_data = {
        'belanja_online_sebulan': int(belanja_online_sebulan),
        'belanja_offline_sebulan': int( belanja_offline_sebulan),
        'pengaruh_ecommerce': int(pengaruh_ecommerce),
        'cari_produk': int(cari_produk),
        'banding_harga': convert_categorical({'banding_harga' : banding_harga}),
        }


        # Reshape the input data to match the format expected by the model
        input_data_reshaped = pd.DataFrame([input_data])

        # Use the model to make a prediction
        prediction = model.predict(input_data_reshaped)[0]

        # Convert the prediction to human-readable format
        prediction_text = "E_Commerce" if prediction == 1 else "Toko Offline"

        # Pass the prediction result to the HTML template
        return render_template("index.html", prediction_text=prediction_text)

    # Render the initial HTML form
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
