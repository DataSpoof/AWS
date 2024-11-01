import json
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    # Log the event to see its structure
    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    s3 = boto3.client('s3')
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Define output bucket (different from input)
    output_bucket = 'preprocessed1234'
    output_folder = 'preprocessedData/'

    try:
        # Fetch the file from S3
        response = s3.get_object(Bucket=input_bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(StringIO(file_content))

        # Preprocess the data
        df_cleaned = preprocess_data(df)

        # Save the cleaned data back to a CSV string
        csv_buffer = StringIO()
        df_cleaned.to_csv(csv_buffer, index=False)
        
        # Define cleaned file key in the output folder
        cleaned_key = output_folder + 'cleaned_' + key.split('/')[-1]

        # Save the cleaned data to the output S3 bucket
        s3.put_object(Bucket=output_bucket, Key=cleaned_key, Body=csv_buffer.getvalue())

        return {
            'statusCode': 200,
            'body': json.dumps('File processed and saved as ' + cleaned_key)
        }
    except Exception as e:
        print(e)
        print(f"Error processing object {key} from bucket {input_bucket}. Make sure they exist and your buckets are in the same region as this function.")
        raise e

def preprocess_data(df):
    # Impute missing values
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column].fillna(df[column].mode()[0], inplace=True)
        else:
            df[column].fillna(df[column].mean(), inplace=True)
    
    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove outliers using IQR method
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    Q1 = df[numeric_columns].quantile(0.25)
    Q3 = df[numeric_columns].quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df[numeric_columns] < (Q1 - 1.5 * IQR)) |(df[numeric_columns] > (Q3 + 1.5 * IQR))).any(axis=1)]

    # Label encoding for categorical columns
    categorical_columns = df.select_dtypes(include=['object']).columns
    for column in categorical_columns:
        df[column] = df[column].astype('category').cat.codes

    return df
