# Use an official Node.js runtime as a parent image
FROM node:18.3.0

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install any needed packages
RUN npm install --legacy-peer-deps

# Copy the rest of the application to the working directory
COPY . .

# Build the React app
RUN npm run build

# Install serve to serve the build
RUN npm install -g serve

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run serve to serve the build directory in SPA mode
CMD ["serve", "-s", "build", "-l", "3000"]
