import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import os

def load_data(file_path):
    """Load and validate the dataset."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset not found at {file_path}")
        
        # Try different encodings
        encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
        last_error = None
        
        for encoding in encodings:
            try:
                print(f"Trying to load dataset with {encoding} encoding...")
                dataset = pd.read_csv(file_path, encoding=encoding)
                print(f"Successfully loaded dataset with {encoding} encoding")
                break
            except UnicodeDecodeError as e:
                last_error = e
                continue
        else:
            raise ValueError(f"Failed to load dataset with any encoding. Last error: {last_error}")
        
        # Print available columns
        print("\nAvailable columns in dataset:", dataset.columns.tolist())
        
        # Map common column names
        query_columns = ['Query', 'query', 'text', 'SQL_Query', 'sql_query']
        label_columns = ['Label', 'label', 'class', 'type', 'is_sql']
        
        # Find matching columns
        query_col = next((col for col in query_columns if col in dataset.columns), None)
        label_col = next((col for col in label_columns if col in dataset.columns), None)
        
        if not query_col or not label_col:
            print("\nAvailable columns:", dataset.columns.tolist())
            raise ValueError("Could not find query and label columns. Please specify the correct column names.")
        
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
        # Get the correct column names
        query_columns = ['Query', 'query', 'text', 'SQL_Query', 'sql_query']
        label_columns = ['Label', 'label', 'class', 'type', 'is_sql']
        
        query_col = next((col for col in query_columns if col in dataset.columns), None)
        label_col = next((col for col in label_columns if col in dataset.columns), None)
        
        if not query_col or not label_col:
            raise ValueError("Could not find query and label columns")
            
        # Take a smaller subset for initial testing
        subset_size = 5000  # Adjust this number as needed
        dataset = dataset.sample(n=min(subset_size, len(dataset)), random_state=42)
        print(f"\nUsing {len(dataset)} samples for training...")
            
        X = dataset[query_col].values
        y = dataset[label_col].values
        
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
    """Train a simple SVM model with RBF kernel and make predictions."""
    try:
        print("\nStarting training with RBF kernel...")
        
        # Create and fit TF-IDF vectorizer with limited features
        print("Vectorizing training data...")
        vectorizer = TfidfVectorizer(
            analyzer='char_wb',
            ngram_range=(3, 5),
            max_features=10000  # Limit features for faster training
        )
        X_train_tfidf = vectorizer.fit_transform(X_train)
        print(f"Training data shape: {X_train_tfidf.shape}")
        
        print("Vectorizing test data...")
        X_test_tfidf = vectorizer.transform(X_test)
        print(f"Test data shape: {X_test_tfidf.shape}")
        
        # Initialize SVM classifier with linear kernel for faster training
        print("\nInitializing SVM classifier...")
        classifier = SVC(
            kernel='linear',  # Linear kernel is faster than RBF
            C=1.0,
            class_weight='balanced',
            random_state=0,
            verbose=True
        )
        
        # Train the model
        print("Training SVM classifier...")
        classifier.fit(X_train_tfidf, y_train)
        
        # Make predictions
        y_pred = classifier.predict(X_test_tfidf)
        
        # Print basic prediction info
        print("\nPrediction completed!")
        
        return vectorizer, classifier, y_pred
    except Exception as e:
        print(f"Error during model training: {str(e)}")
        raise

def evaluate_model(y_test, y_pred):
    """Evaluate the model."""
    try:
        accuracy = accuracy_score(y_test, y_pred)
        print('\n' + '='*50)
        print(f'Model Accuracy: {accuracy:.4f}')
        print('='*50)
        return accuracy
    except Exception as e:
        print(f"Error during model evaluation: {str(e)}")
        raise

def check_sql_injection(query, vectorizer, classifier):
    """Check if a query is SQL injection or not."""
    # Transform the query using the same vectorizer
    query_vector = vectorizer.transform([query])
    # Predict
    prediction = classifier.predict(query_vector)[0]
    probability = classifier.decision_function(query_vector)[0]
    
    is_dangerous = bool(prediction)
    confidence = abs(probability)
    
    print("\nQuery Analysis:")
    print("="*50)
    print(f"Query: {query}")
    print(f"Result: {'DANGEROUS - SQL Injection detected!' if is_dangerous else 'SAFE - No SQL Injection detected'}")
    print(f"Confidence Score: {confidence:.2f}")
    print("="*50)
    
    return is_dangerous, confidence

def main():
    try:
        # Load and train model
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dataset_path = os.path.join(script_dir, '..', 'dataset', 'Modified_SQL_Dataset.csv')
        dataset_path = os.path.abspath(dataset_path)
        
        print(f"Loading dataset from: {dataset_path}")
        dataset = load_data(dataset_path)
        
        print("Preprocessing data...")
        X_train, X_test, y_train, y_test = preprocess_data(dataset)
        
        print("Training SVM model...")
        vectorizer, classifier, y_pred = train_model(X_train, X_test, y_train, y_test)
        
        print("\nTraining completed!")
        accuracy = evaluate_model(y_test, y_pred)
        
        # Interactive query checking
        print("\nEnter queries to check for SQL injection (press Ctrl+C to exit):")
        try:
            while True:
                query = input("\nEnter a query to check: ").strip()
                if not query:
                    continue
                check_sql_injection(query, vectorizer, classifier)
        except KeyboardInterrupt:
            print("\nExiting query checker...")
        
        return vectorizer, classifier
        
    except Exception as e:
        print(f"An error occurred during execution: {str(e)}")
        return None, None

if __name__ == "__main__":
    vectorizer, classifier = main()