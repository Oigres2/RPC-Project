# RPC-Project

To first use this project, we need to execute this command: "docker build -t image_processor ."
This creates a Docker image called image_processor.

After that we need to execute this following command: "docker run -p 8000:8000 image_processor"
With this, the server will be running in the Docket conteiner.

With the server running in the Docket conteiner we then after execute the client file "python client.py". This will process the image that we chose to process.
