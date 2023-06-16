# FastAPI Blog Platform

> Simple blog platform built with FastAPI and PostgreSQL with SQLAlchemy ORM.

## Features

- [x] User registration
- [x] User login
- [x] Post CRUD
- [x] Comment CRUD

## How to host

To set up the project on your VPS, follow these instructions:

1. Connect to your VPS using SSH or any other preferred method.

2. Clone the project repository onto your VPS using the `git clone` command. For example:

   ```bash
   git clone https://github.com/Dank-del/fastapi-blog-platform.git
   ```

3. Change into the project directory:

   ```bash
   cd fastapi-blog-platform
   ```

4. Create a `.env` file in the project directory. You can use the provided `.env.sample` file as a template. Run the following command to create the `.env` file:

   ```bash
   cp .env.sample .env
   ```

   This command copies the contents of the `.env.sample` file into a new `.env` file.

5. Open the `.env` file and set the values for the environment variables according to your requirements. For example:

   ```env
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=your_database_name
   JWT_SECRET=your_jwt_secret
   ```

   Replace `your_username`, `your_password`, `your_database_name`, and `your_jwt_secret` with your desired values.

6. Save the `.env` file.

7. Build and start the containers by running the following command:

   ```bash
   docker-compose up -d
   ```

   This command will use the existing `docker-compose.yml` file in the repository, which reads environment variables from the `.env` file.

8. Access your FastAPI application by opening your browser and navigating to `http://your_vps_ip:8000` or using any other HTTP client. Replace `your_vps_ip` with the IP address of your VPS.

9. You can also connect to the PostgreSQL database using a PostgreSQL client program like `pgAdmin` by configuring the connection with the following details:
   - Host: `your_vps_ip`
   - Port: `5432`
   - Username and password: The values you specified in the `.env` file.

With these instructions, you should be able to set up the project on your VPS. The existing Docker Compose file will read the environment variables from the `.env` file, which you can customize with your desired values. The containers will be built and started using these environment variables, allowing you to access the FastAPI application and the PostgreSQL database on your VPS.

> **An assignment project for Kniru submitted by Sayan Biswas**
