# Use a base image with Java for Fuseki
FROM openjdk:8-alpine

# Set Fuseki version
ENV FUSEKI_VERSION=4.1.0

# Download and unpack Fuseki
RUN wget https://downloads.apache.org/jena/binaries/apache-jena-fuseki-${FUSEKI_VERSION}.tar.gz \
    && tar xzf apache-jena-fuseki-${FUSEKI_VERSION}.tar.gz \
    && mv apache-jena-fuseki-${FUSEKI_VERSION} /fuseki

# Set the working directory
WORKDIR /fuseki

# Expose Fuseki's default port
EXPOSE 3030

# Start Fuseki
CMD ["./fuseki-server"]
