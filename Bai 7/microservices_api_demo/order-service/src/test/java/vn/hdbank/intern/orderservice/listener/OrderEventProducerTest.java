package vn.hdbank.intern.orderservice.listener;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.KafkaTemplate;

import static org.mockito.Mockito.verify;

@ExtendWith(MockitoExtension.class)
class OrderEventProducerTest {

    @Mock
    private KafkaTemplate<String, String> kafkaTemplate;

    @InjectMocks
    private OrderEventProducer orderEventProducer;

    @Test
    void sendOrderEventShouldPublishToNotificationTopic() {
        orderEventProducer.sendOrderEvent("Order placed");

        verify(kafkaTemplate).send("notificationTopic", "Order placed");
    }
}
