# Stage 1: Build
FROM maven:3.9.6-eclipse-temurin-21 AS builder

WORKDIR /build

# Copy parent pom and all module poms (needed by reactor)
COPY pom.xml .
COPY api-gateway/pom.xml api-gateway/
COPY product-service/pom.xml product-service/
COPY order-service/pom.xml order-service/
COPY inventory-service/pom.xml inventory-service/
COPY notification-service/pom.xml notification-service/
COPY discovery-server/pom.xml discovery-server/

# Download api-gateway dependencies only (ignore other modules that have no source)
RUN mvn -pl api-gateway dependency:go-offline -q 2>/dev/null || true

# Copy api-gateway source
COPY api-gateway/src api-gateway/src

# Build only api-gateway
RUN mvn -pl api-gateway package -DskipTests -q

# Stage 2: Run
FROM eclipse-temurin:21-jre-alpine

WORKDIR /app

COPY --from=builder /build/api-gateway/target/api-gateway-0.0.1-SNAPSHOT.jar /app/api-gateway.jar

ENTRYPOINT ["java", "-jar", "/app/api-gateway.jar"]

EXPOSE 8181
