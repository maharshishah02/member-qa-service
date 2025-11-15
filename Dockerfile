FROM python:3.10

# Create working directory
WORKDIR /code

# Copy dependency list
COPY requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy entire project
COPY . /code

# Expose port required by Hugging Face
EXPOSE 7860

# Run FastAPI server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
