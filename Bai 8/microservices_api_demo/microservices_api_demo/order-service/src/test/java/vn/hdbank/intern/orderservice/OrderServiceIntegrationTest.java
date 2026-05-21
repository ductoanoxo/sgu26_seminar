package vn.hdbank.intern.orderservice;

import io.restassured.RestAssured;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.web.client.RestTemplate;
import vn.hdbank.intern.orderservice.dto.BaseResponse;
import vn.hdbank.intern.orderservice.listener.OrderEventProducer;
import vn.hdbank.intern.orderservice.repository.OrderRepo;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ActiveProfiles("test")
@SpringBootTest(
        webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
        properties = {
                "spring.datasource.url=jdbc:h2:mem:order-service-test;MODE=PostgreSQL;DB_CLOSE_DELAY=-1;DATABASE_TO_LOWER=TRUE",
                "spring.datasource.driverClassName=org.h2.Driver",
                "spring.datasource.username=sa",
                "spring.datasource.password=",
                "spring.jpa.hibernate.ddl-auto=create-drop",
                "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
                "spring.cloud.discovery.enabled=false",
                "eureka.client.enabled=false",
                "spring.kafka.bootstrap-servers=localhost:9092",
                "app.inventory-service.base-url=http://INVENTORY-SERVICE/v1/api/inventory"
        }
)
class OrderServiceIntegrationTest {

    @LocalServerPort
    private int port;

    @MockBean
    private RestTemplate restTemplate;

    @MockBean
    private OrderEventProducer orderEventProducer;

    @Autowired
    private OrderRepo orderRepo;

    @BeforeEach
    void setUp() {
        RestAssured.baseURI = "http://localhost";
        RestAssured.port = port;
        orderRepo.deleteAll();
    }

    @Test
    void placeOrderReturnsCreatedWhenInventoryIsAvailable() {
        when(restTemplate.getForObject("http://INVENTORY-SERVICE/v1/api/inventory?skuCode={skuCode}", BaseResponse.class, "iphone_13"))
                .thenReturn(BaseResponse.builder()
                        .skuCode("iphone_13")
                        .isInStock(true)
                        .quantity(10)
                        .build());

        String requestBody = """
                {
                  "orderLineItemsDtoList": [
                    {
                      "skuCode": "iphone_13",
                      "price": 1200,
                      "quantity": 1
                    }
                  ]
                }
                """;

        RestAssured.given()
                .contentType("application/json")
                .body(requestBody)
                .when()
                .post("/api/order")
                .then()
                .statusCode(201)
                .body(Matchers.equalTo("Order Placed"));

        verify(orderEventProducer, times(1)).sendOrderEvent(Mockito.contains("has been placed successfully"));
        org.assertj.core.api.Assertions.assertThat(orderRepo.count()).isEqualTo(1);
    }

    @Test
    void placeOrderReturnsBadRequestWhenInventoryIsUnavailable() {
        when(restTemplate.getForObject("http://INVENTORY-SERVICE/v1/api/inventory?skuCode={skuCode}", BaseResponse.class, "iphone_17"))
                .thenReturn(BaseResponse.builder()
                        .skuCode("iphone_17")
                        .isInStock(false)
                        .quantity(0)
                        .build());

        String requestBody = """
                {
                  "orderLineItemsDtoList": [
                    {
                      "skuCode": "iphone_17",
                      "price": 1200,
                      "quantity": 1
                    }
                  ]
                }
                """;

        RestAssured.given()
                .contentType("application/json")
                .body(requestBody)
                .when()
                .post("/api/order")
                .then()
                .statusCode(400)
                .body(Matchers.equalTo("Failed to Place Order"));

        verify(orderEventProducer, times(1)).sendOrderEvent("Order failed due to insufficient stock");
        org.assertj.core.api.Assertions.assertThat(orderRepo.count()).isZero();
    }
}
