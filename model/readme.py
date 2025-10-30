try:
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os
except ImportError as e:
    print(f"Error: Required package not found. {str(e)}")
    print("Please install required packages using: pip install numpy pandas scikit-learn matplotlib seaborn")
    exit(1)

def load_data(file_path):
    """Load and validate the dataset."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found at {file_path}")
        
        dataset = pd.read_csv(file_path)
        
        # Validate required columns
        required_columns = ['Query', 'Label']
        if not all(col in dataset.columns for col in required_columns):
            raise ValueError("Dataset missing required columns: 'Query' and 'Label'")
        
        # Check for empty dataset
        if dataset.empty:
            raise ValueError("Dataset is empty")
        
        # Check for missing values
        if dataset['Query'].isnull().any() or dataset['Label'].isnull().any():
            print("Warning: Dataset contains missing values. They will be removed.")
            dataset = dataset.dropna()
        
        return dataset
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        raise

def preprocess_data(dataset):
    """Preprocess the data and perform train-test split."""
    try:
        X = dataset['Query'].values
        y = dataset['Label'].values
        
        # Validate that we have at least some samples of each class
        unique_labels = np.unique(y)
        if len(unique_labels) < 2:
            raise ValueError("Dataset must contain at least two classes")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=True, random_state=0
        )
        
        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error preprocessing data: {str(e)}")
        raise

def train_model(X_train, X_test, y_train, y_test):
    """Train the model and make predictions."""
    try:
        # Create and fit TF-IDF vectorizer
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)
        
        # Train classifier
        classifier = LogisticRegression(class_weight='balanced', 
                                      random_state=0,
                                      max_iter=1000)  # Increased max_iter to ensure convergence
        classifier.fit(X_train_tfidf, y_train)
        
        # Make predictions
        y_pred = classifier.predict(X_test_tfidf)
        
        return vectorizer, classifier, y_pred
    except Exception as e:
        print(f"Error during model training: {str(e)}")
        raise

def evaluate_model(y_test, y_pred, save_path='confusion_matrix.png'):
    """Evaluate the model and create visualization."""
    try:
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Model Accuracy: {accuracy:.4f}')
        
        # Create confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
        
        plt.savefig(save_path)
        plt.close()
        
        return accuracy
    except Exception as e:
        print(f"Error during model evaluation: {str(e)}")
        raise

def main():
    try:
        # Define file paths and try different possible locations using absolute paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(script_dir, 'Modified_SQL_Dataset.csv'),  # Try model directory first
            os.path.join(script_dir, '..', 'dataset', 'Modified_SQL_Dataset.csv')  # Then try dataset directory
        ]
        
        # Find the first path that exists
        dataset_path = None
        for path in possible_paths:
            path = os.path.abspath(path)  # Ensure absolute path
            print(f"Checking path: {path}")  # Debug print
            if os.path.exists(path):
                dataset_path = path
                break
        
        if dataset_path is None:
            raise FileNotFoundError("Could not find Modified_SQL_Dataset.csv in any of the expected locations")
        
        print(f"Found dataset at: {dataset_path}")
        print("Loading dataset...")
        dataset = load_data(dataset_path)
        
        print("Preprocessing data...")
        X_train, X_test, y_train, y_test = preprocess_data(dataset)
        
        # Train model
        print("Training model...")
        vectorizer, classifier, y_pred = train_model(X_train, X_test, y_train, y_test)
        
        # Evaluate model
        print("Evaluating model...")
        accuracy = evaluate_model(y_test, y_pred)
        
        print("Process completed successfully!")
        print(f"Final model accuracy: {accuracy:.4f}")
        
        return vectorizer, classifier
        
    except Exception as e:
        print(f"An error occurred during execution: {str(e)}")
        return None, None

if __name__ == "__main__":
    vectorizer, classifier = main()