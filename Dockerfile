FROM apache/airflow:2.7.0

# Set the working directory
WORKDIR /opt/airflow

# Copy the requirements file to the container
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt


ENV PYTHONPATH="/opt/airflow/src:/opt/airflow/plugins:${PYTHONPATH}"

# Copy DAGs, plugins, and other necessary files
COPY ./src /opt/airflow/src
COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins
