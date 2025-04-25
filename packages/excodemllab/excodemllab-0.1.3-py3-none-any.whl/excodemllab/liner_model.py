def lin_reg(X_train, y_train, X_test, y_test, **kwargs):
    """
    Linear Regression Model
    
    Imports:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like regularization parameters)
    
    Returns:
    model : LinearRegression : Trained linear regression model
    
    Code:
    
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error, r2_score
    
    model = LinearRegression(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Mean Squared Error: ", mean_squared_error(y_test, y_pred))
    print("R-squared: ", r2_score(y_test, y_pred))
    
    return model
    """
    

def log_reg(X_train, y_train, X_test, y_test, **kwargs):
    """
    Logistic Regression Model
    
    Imports:
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like solver, max_iter)
    
    Returns:
    model : LogisticRegression : Trained logistic regression model
    
    Code:
    
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = LogisticRegression(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def slp(X_train, y_train, X_test, y_test, **kwargs):
    """
    Support Vector Machine (SVM) Linear Kernel
    
    Imports:
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like C, kernel)
    
    Returns:
    model : SVC : Trained SVM classifier model
    
    Code:
    
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = SVC(kernel='linear', **kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def mlp(X_train, y_train, X_test, y_test, **kwargs):
    """
    Multi-Layer Perceptron (MLP) Model
    
    Imports:
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like hidden_layer_sizes, activation)
    
    Returns:
    model : MLPClassifier : Trained MLP model
    
    Code:
    
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = MLPClassifier(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def naive_bayes(X_train, y_train, X_test, y_test):
    """
    Naive Bayes Model (GaussianNB)
    
    Imports:
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    
    Returns:
    model : GaussianNB : Trained Naive Bayes model
    
    Code:
    
    from sklearn.naive_bayes import GaussianNB
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = GaussianNB()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def ensemble_learning(X_train, y_train, X_test, y_test, model_type="stacking", **kwargs):
    """
    Ensemble Learning: Stacking, Bagging, or Boosting
    
    Imports:
    from sklearn.ensemble import StackingClassifier, BaggingClassifier, GradientBoostingClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    model_type : str : Model type (stacking, bagging, boosting)
    kwargs : Optional arguments for ensemble models
    
    Returns:
    model : Classifier : Trained ensemble model
    
    Code:
    
    from sklearn.ensemble import StackingClassifier, BaggingClassifier, GradientBoostingClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.svm import SVC
    
    if model_type == "stacking":
        base_learners = [
            ('svm', SVC(probability=True)),
            ('dt', DecisionTreeClassifier())
        ]
        model = StackingClassifier(estimators=base_learners, final_estimator=LogisticRegression(), **kwargs)
    elif model_type == "bagging":
        model = BaggingClassifier(base_estimator=DecisionTreeClassifier(), **kwargs)
    elif model_type == "boosting":
        model = GradientBoostingClassifier(**kwargs)
    else:
        raise ValueError("Invalid model type. Choose from 'stacking', 'bagging', or 'boosting'.")
    
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def random_forest(X_train, y_train, X_test, y_test, **kwargs):
    """
    Random Forest Model
    
    Imports:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like n_estimators, max_depth)
    
    Returns:
    model : RandomForestClassifier : Trained random forest model
    
    Code:
    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = RandomForestClassifier(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def decision_tree(X_train, y_train, X_test, y_test, **kwargs):
    """
    Decision Tree Model
    
    Imports:
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like max_depth, min_samples_split)
    
    Returns:
    model : DecisionTreeClassifier : Trained decision tree model
    
    Code:
    
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = DecisionTreeClassifier(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def knn(X_train, y_train, X_test, y_test, **kwargs):
    """
    K-Nearest Neighbors Model
    
    Imports:
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    Parameters:
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    kwargs : Optional arguments (like n_neighbors, algorithm)
    
    Returns:
    model : KNeighborsClassifier : Trained KNN model
    
    Code:
    
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score, confusion_matrix
    
    model = KNeighborsClassifier(**kwargs)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy: ", accuracy_score(y_test, y_pred))
    print("Confusion Matrix: \n", confusion_matrix(y_test, y_pred))
    
    return model
    """
    

def k_means(X_train, **kwargs):
    """
    K-Means Clustering Model
    
    Imports:
    from sklearn.cluster import KMeans
    
    Parameters:
    X_train : DataFrame : Training feature data
    kwargs : Optional arguments (like n_clusters)
    
    Returns:
    model : KMeans : Trained KMeans model
    
    Code:
    
    from sklearn.cluster import KMeans
    
    model = KMeans(**kwargs)
    model.fit(X_train)
    
    return model
    """
    

def grid_search(model, X_train, y_train, param_grid):
    """
    Perform Grid Search for model hyperparameter tuning
    
    Imports:
    from sklearn.model_selection import GridSearchCV
    
    Parameters:
    model : estimator : Model for hyperparameter tuning
    X_train : DataFrame : Training feature data
    y_train : Series : Training target data
    param_grid : dict : Hyperparameter grid to search
    
    Returns:
    best_model : estimator : Best model with tuned hyperparameters
    
    Code:
    
    from sklearn.model_selection import GridSearchCV
    
    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(X_train, y_train)
    
    print("Best Parameters: ", grid_search.best_params_)
    print("Best Score: ", grid_search.best_score_)
    
    return grid_search.best_estimator_
    """
    

def train_test_split_fn(X, y, test_size=0.2, random_state=42):
    """
    Train-Test Split Function
    
    Imports:
    from sklearn.model_selection import train_test_split
    
    Parameters:
    X : DataFrame : Features
    y : Series : Labels
    test_size : float : Fraction of data to be used for testing
    random_state : int : Random seed
    
    Returns:
    X_train, X_test, y_train, y_test
    
    Code:
    
    from sklearn.model_selection import train_test_split
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    return X_train, X_test, y_train, y_test
    """
    

def standard_scaler_fn(X_train, X_test):
    """
    Standard Scaler Function
    
    Imports:
    from sklearn.preprocessing import StandardScaler
    
    Parameters:
    X_train : DataFrame : Training feature data
    X_test : DataFrame : Test feature data
    
    Returns:
    X_train_scaled, X_test_scaled
    
    Code:
    
    from sklearn.preprocessing import StandardScaler
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled
    """
