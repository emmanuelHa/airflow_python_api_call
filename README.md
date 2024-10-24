# Call to eodhd.com API to get the Government Bonds
The spread between yield bond of France over 10Y and yield bond of Germany over 10Y gives an indicator
of the health of France.   
If spread 10Y is > 50(pb) (so > 0.5%) 
=> it is a bad indicator for France
Another indicator is spread 3Y

# Pre requisites:
- Signup at https://eodhd.com/register
You will get an API key or token
Replace its value in .env file
- An AWS account with a .pem file to get connected to your EC2 instance. 
```
cp .env.template .env
```
Then:
- create an S3 bucket
- add your BONDS_API_TOKEN and S3_UNIQUE_BUCKET_NAME into .env file

# dependencies:
You will need the folowing packages:
- pandas
- s3fs     

   

# RUN LOCALLY IF you still have API credit then you can generate Yield Bond 10Y difference from your local machine :
```
python3 interest_rates_etl.py
```



# OTHERWISE INSTALLATION TIME on EC2 (ubuntu AMI):

**You need Python 3.10 not Pyhton 3.12 to install Airflow**
```bash
sudo apt update
sudo apt -y upgrade
```

**Install Python**
```bash  
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3-pip
sudo apt install python3.10-venv
# Update the symbolic link***  
ls -la /usr/bin/python3
sudo rm /usr/bin/python3
sudo ln -s python3.10 /usr/bin/python3
python3 --version

python3 -m venv airflow_venv
source airflow_venv/bin/activate
sudo pip install pandas
sudo pip install s3fs
pip install python-dotenv
pip install matplotlib
```

**INSTALL AIRFLOW** 
***https://airflow.apache.org/docs/apache-airflow/2.7.0/installation/installing-from-pypi.html*** 


https://moderndataengineering.substack.com/p/installing-apache-airflow-on-aws

```bash
export AIRFLOW_VERSION=2.7
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

python -m ensurepip --default-pip
pip3 install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

airflow db migrate

airflow users create \
    --username admin \
    --password admin \
    --firstname <your_name> \
    --lastname <your_last_name> \
    --role Admin \
    --email 
```

Access airflow public DNS address with http  

Then import your DAG (bond-api-dag.py) from Airflow UI.  
=> This should create a DAG named "bonds_api_dag"  
Launch it manually  
=> This should create the graph into the S3 bucket name you 


