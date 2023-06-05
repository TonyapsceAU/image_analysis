from flask import Flask, request

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    index = data['index']
    print(f'Received index: {index}')

    # Perform further processing based on the index

    return 'Prediction received'

if __name__ == '__main__':
    app.run(port=8000)
