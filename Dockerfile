FROM renciorg/renci-python-image:v0.0.1

# Add image info
LABEL org.opencontainers.image.source https://github.com/TranslatorSRI/IssueRouter

# set up requirements
WORKDIR /app

# make sure all is writeable for the nru USER later on
RUN chmod -R 777 .

# Install requirements
ADD requirements-lock.txt .
RUN pip install -r requirements-lock.txt

# switch to the non-root user (nru). defined in the base image
USER nru

# Copy in files
ADD . .

EXPOSE 4007

CMD ["uvicorn", "issue_router.main:app", "--host", "0.0.0.0", "--port", "4007"]
