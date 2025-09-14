from flask import Flask, render_template, jsonify, request
import pandas as pd
from pathlib import Path

from npk_rec.etl.liason import APILiason
from npk_rec.etl.bucket_wrapper import BucketWrapper

# Include AWS api information

app = Flask(__name__)

# Sample data (replace with your actual data source)
# Get data from AWS
PLANT_DEFAULT = "PLANT"
NPK_DEFAULT = "0-0-0"
data = [
    {"id": 1, "plant": PLANT_DEFAULT, "npk": NPK_DEFAULT, "opt_npk": NPK_DEFAULT},
    {"id": 2, "plant": PLANT_DEFAULT, "npk": NPK_DEFAULT, "opt_npk": NPK_DEFAULT},
    {"id": 3, "plant": PLANT_DEFAULT, "npk": NPK_DEFAULT, "opt_npk": NPK_DEFAULT},
]

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/api/data', methods=['GET'])
def get_data():
    # Implement sorting, filtering, pagination logic here based on request.args
    return jsonify(data)

@app.route('/api/update_cell', methods=['POST'])
def update_cell():
    # Handle cell updates from client-side (e.g., editable cells)
    updated_data = request.json
    # Update your data source based on updated_data
    return jsonify({"status": "success"})

@app.route('/api/fetch_data', methods=['POST'])
def fetch_data():
    # Get the optimal data from the request
    request_data = request.json
    selected_plant_id = request_data.get('id')
    selected_plant_type = request_data.get('plant')

    # CSV path
    csv_file_path = Path('../data/plant_data.csv')
    print(csv_file_path.resolve())

    df = pd.read_csv(csv_file_path) # Read file path
    row = df[df['plant'] == selected_plant_type]

    if row.empty:
        print('Error: Row empty!')
        return jsonify({'error': 'Plant not found'}), 404
    
    optimal_npk = row['npk'].values[0]

    # Get the actual data from the device
    bucket = BucketWrapper(bucket_name='npkdata', object_key='random_npk_data.csv')

    liason = APILiason(bucket)
    bucket_data = liason.get_data()
    actual_npk_vals = bucket_data.iloc[-1][['N', 'P', 'K']].astype(int).tolist()
    actual_npk = '-'.join(map(str, actual_npk_vals))

    for item in data:
        if item['id'] == selected_plant_id:
            item['npk'] = actual_npk

    print(f'New NPK ratio for plant {selected_plant_id} is {actual_npk}')

    return jsonify({'plant_id': selected_plant_id, 'optimal_npk': optimal_npk, 'actual_npk': actual_npk})

@app.route('/api/update_dropdown', methods=['POST'])
def update_dropdown():
    # Get the updated dropdown value and row ID from the request
    request_data = request.json
    row_id = request_data.get('id')
    new_plant = request_data.get('plant')

    print(f'Dropdown changed; {row_id=}, {new_plant=}')

    for item in data:
        if item['id'] == row_id:
            item['plant'] = new_plant

    print(data)

    return jsonify({"status": "success"})
    
if __name__ == '__main__':
    app.run(debug=True)