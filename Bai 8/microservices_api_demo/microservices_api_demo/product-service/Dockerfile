# Chá»n image base (sá»­ dá»¥ng JDK image)
FROM eclipse-temurin:21-jre-alpine

# Thiáº¿t láº­p thÆ° má»¥c lÃ m viá»‡c trong container
WORKDIR /app

# Sao chÃ©p file jar vÃ o container
COPY target/product-service-0.0.1-SNAPSHOT.jar /app/product-service.jar

# Cháº¡y á»©ng dá»¥ng khi container báº¯t Ä‘áº§u
ENTRYPOINT ["java", "-jar", "/app/product-service.jar"]

# Cáº¥u hÃ¬nh cá»•ng mÃ  á»©ng dá»¥ng sáº½ láº¯ng nghe
EXPOSE 8081
