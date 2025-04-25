import argparse
import pickle
import pandas as pd
from pkr import PKR

def main():
    parser = argparse.ArgumentParser(
        description="Pure Kernel Regression CLI: fit/train and predict in one command"
    )
    parser.add_argument(
        "--train", required=True, help="Path to train CSV file"
    )
    parser.add_argument(
        "--test", required=True, help="Path to test CSV file"
    )
    parser.add_argument(
        "--target", required=True, help="Name of the target column in train CSV"
    )
    parser.add_argument(
        "--output", default="submission.csv", help="Output CSV for predictions"
    )
    parser.add_argument(
        "--max_dim", type=int, default=3, help="Max kernel dimension to scan"
    )
    parser.add_argument(
        "--top_k", type=int, default=120, help="Number of top kernels to keep"
    )
    args = parser.parse_args()

    # Load data
    train_df = pd.read_csv(args.train)
    test_df = pd.read_csv(args.test)

    # Fit model
    model = PKR(max_dim=args.max_dim, top_k=args.top_k)
    model.fit(train_df, target=args.target)

    # Predict
    preds = model.predict(test_df)

    # Prepare submission
    if "id" not in test_df.columns:
        test_df["id"] = test_df.index
    submission = test_df[["id"]].copy()
    submission[args.target] = preds
    submission.to_csv(args.output, index=False)
    print(f"Submission saved to {args.output}")

    # Save model
    with open("pkr_model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("Model saved to pkr_model.pkl")

if __name__ == "__main__":
    main()
