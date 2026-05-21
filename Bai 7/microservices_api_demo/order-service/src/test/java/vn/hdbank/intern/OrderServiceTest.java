package vn.hdbank.intern;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.web.client.RestTemplate;
import vn.hdbank.intern.orderservice.OrderServiceApplication;
import vn.hdbank.intern.orderservice.dto.BaseResponse;
import vn.hdbank.intern.orderservice.listener.OrderEventProducer;
import vn.hdbank.intern.orderservice.repository.OrderRepo;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.when;

@ActiveProfiles("test")
@SpringBootTest(
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT,
    classes = OrderServiceApplication.class
)
class OrderServiceTest {

    @LocalServerPort
    private int port;

    @MockBean
    private OrderEventProducer orderEventProducer;

    @MockBean
    private RestTemplate restTemplate;

    @Autowired
    private OrderRepo orderRepo;

    @BeforeEach
    void setUp() {
    RestAssured.baseURI = "http://localhost";
    RestAssured.port = port;
    orderRepo.deleteAll();
    }

    @Test
    void isSubmitOrder() {
      when(restTemplate.getForObject(
        eq("http://INVENTORY-SERVICE/v1/api/inventory?skuCode=iPhone_13"),
        eq(BaseResponse.class)))
        .thenReturn(BaseResponse.builder()
          .skuCode("iPhone_13")
          .isInStock(true)
          .quantity(10)
          .build());

      doNothing().when(restTemplate).put(contains("/v1/api/inventory/updateStock?skuCode=iPhone_13&quantity=1"), eq(null));

    String submitOrderJson = """
        {
          "orderLineItemsDtoList": [
            {
              "skuCode": "iPhone_13",
              "price": 1200,
              "quantity": 1
            }
          ]
        }
        """;

    String responseBodyString = RestAssured.given()
        .contentType("application/json")
        .body(submitOrderJson)
        .when()
        .post("/api/order")
        .then()
        .statusCode(201)
        .extract()
        .body().asString();

    assertThat(responseBodyString).isEqualTo("Order Placed");
    assertThat(orderRepo.count()).isEqualTo(1);
    }

    @Test
    void isNotSubmitOrder() {
      when(restTemplate.getForObject(
        eq("http://INVENTORY-SERVICE/v1/api/inventory?skuCode=iPhone_17"),
        eq(BaseResponse.class)))
        .thenReturn(BaseResponse.builder()
          .skuCode("iPhone_17")
          .isInStock(true)
          .quantity(0)
          .build());

    String submitOrderJson = """
        {
          "orderLineItemsDtoList": [
            {
              "skuCode": "iPhone_17",
              "price": 1200,
              "quantity": 1
            }
          ]
        }
        """;

    String responseBodyString = RestAssured.given()
        .contentType("application/json")
        .body(submitOrderJson)
        .when()
        .post("/api/order")
        .then()
        .statusCode(400)
        .extract()
        .body().asString();

    assertThat(responseBodyString).isEqualTo("Failed to Place Order");
    assertThat(orderRepo.count()).isEqualTo(0);
    }
}
