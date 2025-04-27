# utils.py

def validate_columns(df, required_columns):
    """
    Validates that all required columns exist in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        required_columns (list): List of required column names.

    Raises:
        ValueError: If any required column is missing.
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
