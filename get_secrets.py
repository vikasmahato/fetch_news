import boto3
import json

SECRET_API_KEY_ARN = "arn:aws:secretsmanager:ap-south-1:864981733004:secret:test/news_api_key-3cjnL9"
SECRETS_DB_ARN_PROD = "arn:aws:secretsmanager:ap-south-1:864981733004:secret:rds!db-760fa0b2-a49b-4ec9-b5e0-084689152368-VVxepb"
SECRETS_DB_ARN = "arn:aws:secretsmanager:ap-south-1:864981733004:secret:test/nisee/backend-rds-r0Jcjf"
secrets_client = boto3.client("secretsmanager")

def get_news_data_api_key():
    response = secrets_client.get_secret_value(SecretId=SECRET_API_KEY_ARN)
    secret = json.loads(response["SecretString"])
    return secret.get("API_KEY")


def get_db_credentials(is_prod=False):
    if is_prod:
        response = secrets_client.get_secret_value(SecretId=SECRETS_DB_ARN_PROD)
        host="nisee-prod.cx4yoacwm0sy.ap-south-1.rds.amazonaws.com"
    else:
        response = secrets_client.get_secret_value(SecretId=SECRETS_DB_ARN)
        host="nisee-test.cx4yoacwm0sy.ap-south-1.rds.amazonaws.com"
    secret = json.loads(response["SecretString"])



    return {
        "host": host,
        "user": secret.get("username"),
        "password": secret.get("password"),
        "database": "nisee_prod" if is_prod else "nisee_test"
    }


def get_db_url():
    db_credentials = get_db_credentials()
    return f"mysql+pymysql://{db_credentials['user']}:{db_credentials['password']}@{db_credentials['host']}:3306/{db_credentials['database']}"
# sqlacodegen mysql+pymysql://admin:7Ey2x4AntEhaRrY@nisee-test.cx4yoacwm0sy.ap-south-1.rds.amazonaws.com:3306/nisee_test --outfile models/models.py


if __name__ == "__main__":
    print(get_news_data_api_key())
    print(get_db_credentials(is_prod=False))
    print(get_db_url())