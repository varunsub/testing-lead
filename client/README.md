
# Next.js Frontend Setup

## Features

- **Next.js Frontend**

## Step 1: Install Dependencies

Use `npm` to install the necessary packages for the Next.js frontend app.

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install the required packages:
   ```bash
   npm install
   ```

## Step 2: Environment Setup

Fill out the `.env` variable. There is currently only one, and it's just the backend API URL.

By default, this will be `http://localhost:8000`.

Create a `.env.local` file in the root of the `frontend` directory and add the following line:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 3: Running the Frontend

Run the development server locally using:
```bash
npm run dev
```
This will run on `localhost:3000` by default.

## Frontend Routes

There are 3 main routes in this Next.js app:

1. **Home Route (`/`)**
   - This is the landing page of the application. It may include general information and navigation options to other parts of the app.
   
2. **Protected Route (`/internal`)**
   - This is a auth protected route that allows a user to view leads and then mark leads as REACHED_OUT. 

   
3. **Login Route (`/login`)**
   - This route allows users to log in to the application. It handles user authentication and redirects authenticated users to the protected route.

## Additional Details

Make sure to replace placeholders in the example `.env.local` file with actual values. Here is an example:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

With these steps, you should be able to set up, run, and test the Next.js application locally.