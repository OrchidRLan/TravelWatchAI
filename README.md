# TravelWatchAI
info5368 Flight price prediction + BUY/WAIT agent

## Dataset
Download `Clean_Dataset.csv` from Kaggle:
https://www.kaggle.com/datasets/shubhambathwal/flight-price-prediction

Place it at: `datasets/Clean_Dataset.csv`

## Create Environment in WSL
I run everything inside Ubuntu/WSL instead of Windows Python.

```bash
cd /home/flyingc/TravelWatchAI
python3 -m venv .venv-travelwatch
source .venv-travelwatch/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

```bash
pip install jupyterlab
```

## Our Training Workflow
You may find a reference in `document_reference/PAML_Proposal.pdf` for more:
Notebook path: `notebooks/travelwatchai.ipynb`

1. Prepare data from `datasets/Clean_Dataset.csv`.
2. Perform EDA and preprocessing:
   drop missing values, encode categorical fields, normalize numeric fields, and remove outliers with IQR / Z-score.
3. Train the price prediction models:
   Linear Regression, Polynomial Regression, Ridge Regression, and Lasso Regression.
4. Create Buy/Wait labels programmatically, then train:
   Logistic Regression and KNN.
5. Evaluate with:
   regression using MSE / RMSE / MAE / R², classification using F1 / AUC-ROC.
6. Select deployment models with a bias toward stable, efficient models:
   prefer Ridge when performance is close to Lasso, and prefer Logistic Regression when performance is close to KNN.


Run the notebook in WSL:

```bash
source .venv-travelwatch/bin/activate
jupyter lab
```

## Run the App in WSL
```bash
source .venv-travelwatch/bin/activate
cd streamlit_app
streamlit run app.py
```

## App Pages
- **Dashboard** — overview cards for the most recent watches, multi-route price chart, and Book/Search links per route.
- **See All** — full list of every watch with route, date, current price, recommendation, status, View Detail, and Book/Search action.
- **Add New Watch** — origin, destination, dep/arr date, target price, currency, adults, cabin class (and optional stops/time).
- **Compare** — pick up to 3 routes, see current lowest price, AI predicted price, BUY/WAIT and estimated saving vs target.
- **Task Detail** — single watch view with a Buy/Wait reason narrative, observed-price chart, top Skyscanner itineraries, and a Book Now link that's gated on BUY.
- **ML Insights** — F1 / AUC / confusion matrix / ROC for the classifier, plus R² / RMSE / MAE for Ridge vs Lasso and learning curves.
- **View Data** — dataset preview, columns, missing values, price distribution, correlation heatmap, and the processed (one-hot + standardized) feature matrix.


## Add your API keys
Create `streamlit_app/.streamlit/secrets.toml`:

```toml
RAPIDAPI_KEY = "your key"
```

You can also set `RAPIDAPI_KEY` as an environment variable.
