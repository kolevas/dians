# Stage 1: Build the application
FROM maven:3.9.4-eclipse-temurin-17-alpine AS build

# Set the working directory
WORKDIR /app

# Copy the project files
COPY pom.xml ./
RUN mvn dependency:go-offline -B

COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Stage 2: Create a lightweight runtime image
FROM eclipse-temurin:17-jre-alpine AS runtime

# Set the working directory
WORKDIR /app

# Copy the Spring Boot fat JAR from the build stage
COPY --from=build /app/target/*.jar app.jar

# Expose the application port
EXPOSE 9090

# Configure environment variables for runtime properties
ENV JAVA_OPTS=""
ENV SPRING_APPLICATION_JSON=""

# Run the application
CMD ["sh", "-c", "java $JAVA_OPTS -Dspring.application.json=$SPRING_APPLICATION_JSON -jar app.jar"]
