# MakeOfficeHours

## Getting Started

Currently, the frontend is built using the Vue framework.

To run the frontend in development, cd into the client directory and run the following commands:
```bash
npm install
```
```bash
npm run dev
```

This will start the development server on port 3000.

The frontend server expects the backend to be running on port 5000, and requests for paths starting with `/api/` to be proxied to the backend. Vite is configured to do this; however, in deployment this will have to be done independently.

### Some Notes

At the moment, all Vue files are written in Typescript. For consistency, future files should be as well unless this gets changed globally.