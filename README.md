# Overview

## Features

- **GCP Cloud Bucket File Upload**
- **Postgres setup with SQLAlchemy ORM**
- **API built on FastAPI**
- **SendGrid for Email Sending**

There are two applications:

1. **Client**
2. **Server**

Please enter each directory to check the specific information regarding environment setup for each app.

To use the deployed version of the app, please use the following URL:

[Deployed App](https://lead-form-front.vercel.app/)

You can use this to test the code.

## Frontend Routes

There are 3 main routes in this Next.js app:

1. **Home Route (`/`)**
   - This is the landing page of the application. It may include general information and navigation options to other parts of the app.
   
2. **Protected Route (`/internal`)**
   - This is a auth protected route that allows a user to view leads and mark them as REACHED_OUT.
   
3. **Login Route (`/login`)**
   - This route allows users to log in to the application. It handles user authentication and redirects authenticated users to the internal route.

More information about the routes and the internal/login page are available in the client directory.

## Test User

- **Email**: varunsubraprof@gmail.com
- **Password**: password

## Potential Issues

1. **Cold Start**: The backend is hosted on a hobby tier, which has a cold start. It may take a while for the backend to start up after the first request.
2. **Email Delivery**: Since I'm using a personal Gmail account with SendGrid, emails frequently get sent to spam or are blocked. Please do not overuse this feature to avoid being permanently blocked.

## Hosting Details

- **Backend**: Hosted on Heroku
- **Frontend**: Hosted on Vercel