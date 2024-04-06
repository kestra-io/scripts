import argparse
import time

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

start_time = time.time()

parser = argparse.ArgumentParser(description="Generate a sales forecast.")
parser.add_argument("--days", type=int, help="The number of days to forecast.", default=30)
parser.add_argument("--file_path", type=str, help="The path to the CSV file.", default="sales_data.csv")
parser.add_argument("--n_estimators", type=int, default=500)
parser.add_argument("--learning_rate", type=float, default=0.1)
parser.add_argument("--max_depth", type=int, default=3)
parser.add_argument("--subsample", type=float, default=0.7)
parser.add_argument("--colsample_bytree", type=float, default=0.7)
parser.add_argument("--gamma", type=float, default=1)
parser.add_argument("--early_stopping_rounds", type=int, default=100)

args = parser.parse_args()

# ==================== TRAIN ===================
df = pd.read_csv(args.file_path)
df["ds"] = pd.to_datetime(df["ds"])
df = df.sort_values(by="ds")

# Feature engineering
df["day_of_year"] = df["ds"].dt.dayofyear
df["year"] = df["ds"].dt.year

X = df[["day_of_year", "year"]]
y = df["y"]

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# XGBoost Model
xgb_model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=args.n_estimators,
    learning_rate=args.learning_rate,
    max_depth=args.max_depth,
    subsample=args.subsample,
    colsample_bytree=args.colsample_bytree,
    gamma=args.gamma
)
xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], early_stopping_rounds=args.early_stopping_rounds, verbose=False)

# ==================== PREDICT ==================
# Generate future dates
last_date = df["ds"].iloc[-1]
future_dates = [last_date + pd.Timedelta(days=x) for x in range(1, args.days + 1)]
future_df = pd.DataFrame(future_dates, columns=["ds"])
future_df["day_of_year"] = future_df["ds"].dt.dayofyear
future_df["year"] = future_df["ds"].dt.year

# Predict with Linear Regression
future_df["yhat_lr"] = lr_model.predict(future_df[["day_of_year", "year"]])

# Predict with XGBoost
future_df["yhat_xgb"] = xgb_model.predict(future_df[["day_of_year", "year"]])
future_df.to_csv("forecast.csv", index=False)
xgb_model.save_model("xgboost_model.json")

# ==================== VISUALIZE ================
start_date = "2023-01-01"
end_date = "2024-12-31"
mask_original = (df["ds"] >= start_date) & (df["ds"] <= end_date)
filtered_df = df.loc[mask_original]

mask_future = (future_df["ds"] >= start_date) & (future_df["ds"] <= end_date)
filtered_future_df = future_df.loc[mask_future]

plt.figure(figsize=(12, 6))
plt.scatter(filtered_df["ds"], filtered_df["y"], color="blue", label="Original Data", marker="o", s=10)
plt.scatter(filtered_future_df["ds"], filtered_future_df["yhat_lr"], color="red", label="LR Forecast", marker="x", s=10)
plt.scatter(filtered_future_df["ds"], filtered_future_df["yhat_xgb"], color="green", label="XGB Forecast", marker="^", s=10)

plt.title("Sales Forecast Comparison")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gcf().autofmt_xdate()
plt.legend()
plt.tight_layout()
plt.savefig("forecast_comparison_plot.png")
plt.show()

end_time = time.time()
processing_time = end_time - start_time

print(f"Processing Time: {processing_time} seconds")
