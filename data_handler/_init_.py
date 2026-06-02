import pandas as pd
def load_clean(filepath):
    df = pd.read_csv(filepath)

    ##identification
    print("Shape:", df.shape)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nData types:\n", df.dtypes)

    ##cleaning
    #drop
    df=df.drop(columns=["Loan_ID"])

    #fix dependents(3+ to 3)
    df["Dependents"] = df["Dependents"].replace("3+", "3")
    df["Dependents"] = pd.to_numeric(df["Dependents"], errors="coerce")

    #fill in missing values
    categorical_cols = ["Gender", "Married", "Self_Employed", "Credit_History", "Loan_Amount_Term"]
    for col in categorical_cols:
        df[col] = df[col].fillna(df[col].mode()[0])

    numerical_cols = ["Dependents", "LoanAmount"]
    for col in numerical_cols:
        df[col] = df[col].fillna(df[col].median())

    #loan status to binary
    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    #add income bracket column
    df["Income_Bracket"] = pd.cut(
        df["ApplicantIncome"],
        bins=[0,3000,6000,999999],#rbi income classification
        labels=["Low", "Medium", "High"]
    )

    #capping outliers in income(99th percentile)
    cap = df.ApplicantIncome.quantile(0.99)
    df["ApplicantIncome"] = df["ApplicantIncome"].clip(upper=cap)


    #final verification
    print("\nMissing after cleaning:\n", df.isnull().sum())
    print("\nFinal shape:", df.shape)
    print("\nLoan_Status distribution:\n", df["Loan_Status"].value_counts())

    return df
