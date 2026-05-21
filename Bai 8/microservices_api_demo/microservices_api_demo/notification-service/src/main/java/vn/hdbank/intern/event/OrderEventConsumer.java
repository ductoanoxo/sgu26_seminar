package vn.hdbank.intern.event;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import vn.hdbank.intern.dto.OrderNotificationMessage;

import java.util.Objects;

@AllArgsConstructor
@Service
@Slf4j
public class OrderEventConsumer {

    private final ProcessConsumer processConsumer;
    private final ObjectMapper objectMapper;

    @KafkaListener(topics = "notificationTopic", groupId = "notification-group")
    public void listen(String message) {
        log.info("Received notification message: {}", message);
        
        if (message == null || message.isEmpty()) {
            log.warn("Received empty message, skipping processing ........ ");
            return;
        }

        try {
            // Parse JSON message format: {"orderNumber": "ORD123", "message": "Order Placed Successfully"}
            OrderNotificationMessage notificationMessage = objectMapper.readValue(message, OrderNotificationMessage.class);
            
            log.info("Processing order notification - Order Number: {}, Message: {}", 
                    notificationMessage.getOrderNumber(), notificationMessage.getMessage());
            
            // Simulate sending email confirmation for order
            String to = "yentuan130803@gmail.com";
            String subject = "ORDER CONFIRMATION - " + notificationMessage.getOrderNumber();
            String text = "Dear Customer,\n\nYour order " + notificationMessage.getOrderNumber() + 
                         " has been placed successfully.\n\nMessage: " + notificationMessage.getMessage() + 
                         "\n\nThank you for your order!";
            
            log.info("Sending email to {}", to);
            processConsumer.sendEmail(to, subject, text);
            
            log.info("Order notification processed successfully for order: {}", notificationMessage.getOrderNumber());
            
        } catch (JsonProcessingException e) {
            log.error("Failed to parse notification message: {}. Error: {}", message, e.getMessage());
            // Fallback: treat raw message as plain text if not JSON
            String to = "yentuan130803@gmail.com";
            String subject = "ORDER";
            String text = message;
            log.info("Fallback: Sending raw message as email to {}", to);
            processConsumer.sendEmail(to, subject, text);
        }
    }

}