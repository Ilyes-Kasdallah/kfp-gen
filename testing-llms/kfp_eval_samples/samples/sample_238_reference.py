import kfp.dsl as dsl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import string
from typing import List
import joblib


# Component 1: Extract data
@dsl.component(
    base_image='python:3.8',  # Specifying the base image
    packages_to_install=['requests', 'pandas']
)
def extract_data() -> dsl.OutputPath(str):
    import requests
    import zipfile
    import io
    import pandas as pd

    url = 'https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip'

    # Step 1: Download the zip file
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Step 2: Extract the contents of the zip file
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        with z.open('SMSSpamCollection') as f:
            # Step 3: Read the contents into a DataFrame
            df = pd.read_csv(f, sep='\t', names=["label", "message"], header=None)

    # Step 4: Save the DataFrame to a CSV file
    output_path = '/mnt/data/smsspamcollection.csv'
    df.to_csv(output_path, index=False)

    return output_path


# Component 2: Data Preprocessing
@dsl.component(
    base_image='python:3.8',
    packages_to_install=['pandas']
)
def preprocess_data(file_path: dsl.InputPath(str)) -> None:
    import pandas as pd
    import string
    
    df = pd.read_csv(file_path)
    
    # Add 'length' and 'punct' features
    df['length'] = df['message'].apply(len)
    df['punct'] = df['message'].apply(lambda x: sum([1 for char in x if char in string.punctuation]))
    
    # Save the preprocessed data
    df.to_csv('/mnt/data/preprocessed_smsspamcollection.csv', index=False)


# Component 3: Exploratory Data Analysis (EDA)
@dsl.component(
    base_image='python:3.8',
    packages_to_install=['pandas', 'matplotlib', 'numpy']
)
def eda() -> None:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    df = pd.read_csv('/mnt/data/preprocessed_smsspamcollection.csv')

    print('Missing values: ')
    print(df.isnull().sum(),'\n')

    print('Categories: ',df['label'].unique(),'\n')

    print('Rate of each category: ')
    print(df['label'].value_counts())

    plt.xscale('log')
    bins = 1.15**(np.arange(0,50))
    plt.hist(df[df['label']=='ham']['length'], bins=bins,alpha=0.8)
    plt.hist(df[df['label']=='spam']['length'], bins=bins,alpha=0.8)
    plt.legend(('ham','spam'))
    plt.title('Inference: usually spams are longer in text compared to ham')
    plt.xlabel('Text length')
    plt.ylabel('Category rate')
    plt.savefig('/mnt/data/length_histogram.png')
    plt.clf()

    plt.xscale('log')
    bins = 1.15**(np.arange(0,50))
    plt.hist(df[df['label']=='ham']['punct'], bins=bins,alpha=0.8)
    plt.hist(df[df['label']=='spam']['punct'], bins=bins,alpha=0.8)
    plt.legend(('ham','spam'))
    plt.title('Inference: a small tendency of spams towards more punctutations (not a firm inference)')
    plt.xlabel('Text length')
    plt.ylabel('Category rate')
    plt.savefig('/mnt/data/punct_histogram.png')


# Component 4: Train Model
@dsl.component(
    base_image='python:3.8',
    packages_to_install=['pandas', 'scikit-learn', 'joblib']
)
def train_model() -> None:
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn import metrics
    import joblib

    df = pd.read_csv('/mnt/data/preprocessed_smsspamcollection.csv')

    X = df['message']
    y = df['label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    text_clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', RandomForestClassifier())])
    text_clf.fit(X_train, y_train)

    predictions = text_clf.predict(X_test)

    df_conf_mat = pd.DataFrame(metrics.confusion_matrix(y_test, predictions), index=['ham', 'spam'], columns=['ham', 'spam'])
    print(df_conf_mat, '\n')

    clf_report = metrics.classification_report(y_test, predictions)
    print(clf_report, '\n')

    acc = metrics.accuracy_score(y_test, predictions)
    print('Model accuracy: ', acc * 100)

    # Save the model to a file
    joblib.dump(text_clf, '/mnt/data/text_clf.joblib')


# Component 5: Test Model
@dsl.component(
    base_image='python:3.8',
    packages_to_install=['scikit-learn', 'joblib']
)
def test_model( sample_messages: List[str]) -> List[str]:
    import joblib
    model = joblib.load('/mnt/data/text_clf.joblib')
    predictions = model.predict(sample_messages)
    return predictions


# Define the pipeline
@dsl.pipeline(
    name='SMS Spam Detection Pipeline',
    description='A pipeline for detecting spam messages from SMS data'
)
def sms_spam_detection_pipeline():
    # Step 1: Extract data
    extracted_data = extract_data()
    print(extracted_data.output)
    # Step 2: Preprocess data
    preprocess_data(
        file_path=extracted_data.output,
    )

    # Step 3: Perform EDA
    eda()

    # Step 4: Train model
    train_model()

    # Step 5: Test model
    test_samples = ['Hi, how you doing?', 'Congratulations! You have won a $1000 prize! Text 1 to 1423.']
    test_output = test_model(sample_messages=test_samples)
    print(test_output)

# Compile the pipeline
if __name__ == '__main__':
    import kfp.compiler as compiler
    compiler.Compiler().compile(sms_spam_detection_pipeline, 'sms_spam_detection_pipeline.yaml')
