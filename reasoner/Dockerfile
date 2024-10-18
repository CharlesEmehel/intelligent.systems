# Base image with Java for Reasoner
FROM openjdk:8-jdk

# Set the working directory
WORKDIR /usr/src/andromedad

# Copy the local code to the container
COPY ./app /usr/src/andromedad

# Build your application
RUN javac cysgo.java

# Run your application
CMD ["java", "cysgo"]
