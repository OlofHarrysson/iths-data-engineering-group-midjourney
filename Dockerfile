FROM apache/airflow:latest-python3.10
COPY requirements.txt requirements.txt

# removed -e row from requirements.txt and saves to new file to be albe to run docker init
RUN grep -v "^-e" requirements.txt > requirements_without_editable_install.txt
RUN pip install -r requirements_without_editable_install.txt