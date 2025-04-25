# visualizations.py

def boxplot_fn(data, x=None, y=None, **kwargs):
    """
    Boxplot Visualization
    
    Imports:
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    Parameters:
    data : DataFrame : Data to visualize
    x : str : Column for x-axis (optional)
    y : str : Column for y-axis (optional)
    kwargs : Optional arguments for customization (like hue, palette)
    
    Code:
 
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.boxplot(data=data, x=x, y=y, **kwargs)
    plt.show()
    """
    

def pairplot_fn(data, **kwargs):
    """
    Pairplot Visualization
    
    Imports:
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    Parameters:
    data : DataFrame : Data to visualize
    kwargs : Optional arguments for customization
    
    Code:
 
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.pairplot(data, **kwargs)
    plt.show()
    """
    

def barplot_fn(data, x=None, y=None, **kwargs):
    """
    Barplot Visualization
    
    Imports:
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    Parameters:
    data : DataFrame : Data to visualize
    x : str : Column for x-axis
    y : str : Column for y-axis
    kwargs : Optional arguments for customization
    
    Code:
 
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.barplot(data=data, x=x, y=y, **kwargs)
    plt.show()
    """
    

def countplot_fn(data, x=None, **kwargs):
    """
    Countplot Visualization
    
    Imports:
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    Parameters:
    data : DataFrame : Data to visualize
    x : str : Column for x-axis
    kwargs : Optional arguments for customization
    
    Code:
 
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.countplot(data=data, x=x, **kwargs)
    plt.show()
    """
    

def roc_curve_fn(model, X_test, y_test):
    """
    ROC Curve Visualization
    
    Imports:
    from sklearn.metrics import roc_curve, auc
    import matplotlib.pyplot as plt
    
    Parameters:
    model : estimator : Trained model
    X_test : DataFrame : Test feature data
    y_test : Series : Test target data
    
    Code:
 
    from sklearn.metrics import roc_curve, auc
    import matplotlib.pyplot as plt
    
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure()
    plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='gray', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.show()
    """
    

def heatmap_fn(data, **kwargs):
    """
    Heatmap Visualization
    
    Imports:
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    Parameters:
    data : DataFrame : Data to visualize
    kwargs : Optional arguments for customization
    
    Code:
 
    import seaborn as sns
    import matplotlib.pyplot as plt
    
    sns.heatmap(data, **kwargs)
    plt.show()
    """
