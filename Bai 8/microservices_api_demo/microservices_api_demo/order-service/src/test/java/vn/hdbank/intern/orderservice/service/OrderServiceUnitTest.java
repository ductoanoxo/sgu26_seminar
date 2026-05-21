package vn.hdbank.intern.orderservice.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentMatchers;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestTemplate;
import vn.hdbank.intern.orderservice.dto.BaseResponse;
import vn.hdbank.intern.orderservice.dto.OrderDTO;
import vn.hdbank.intern.orderservice.dto.OrderLineItemsDTO;
import vn.hdbank.intern.orderservice.listener.OrderEventProducer;
import vn.hdbank.intern.orderservice.repository.OrderRepo;

import java.math.BigDecimal;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceUnitTest {

    private static final String INVENTORY_URL = "http://INVENTORY-SERVICE/v1/api/inventory";

    @Mock
    private OrderRepo orderRepo;

    @Mock
    private RestTemplate restTemplate;

    @Mock
    private OrderEventProducer orderEventProducer;

    @InjectMocks
    private OrderService orderService;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(orderService, "inventoryServiceBaseUrl", INVENTORY_URL);
    }

    @Test
    void placeOrderReturnsTrueWhenAllItemsAreInStock() {
        OrderDTO orderDTO = buildOrderDTO("iphone_13", 2);
        BaseResponse inventoryResponse = BaseResponse.builder()
                .skuCode("iphone_13")
                .isInStock(true)
                .quantity(5)
                .build();

        when(restTemplate.getForObject(INVENTORY_URL + "?skuCode={skuCode}", BaseResponse.class, "iphone_13"))
                .thenReturn(inventoryResponse);

        boolean result = orderService.placeOrder(orderDTO).join();

        assertThat(result).isTrue();
        verify(orderRepo).save(any());
        verify(restTemplate).put(INVENTORY_URL + "/updateStock?skuCode={skuCode}&quantity={quantity}", null, "iphone_13", 2);
        verify(orderEventProducer).sendOrderEvent(ArgumentMatchers.contains("has been placed successfully"));
    }

    @Test
    void placeOrderReturnsFalseWhenAnyItemIsOutOfStock() {
        OrderDTO orderDTO = buildOrderDTO("iphone_17", 1);
        BaseResponse inventoryResponse = BaseResponse.builder()
                .skuCode("iphone_17")
                .isInStock(false)
                .quantity(0)
                .build();

        when(restTemplate.getForObject(INVENTORY_URL + "?skuCode={skuCode}", BaseResponse.class, "iphone_17"))
                .thenReturn(inventoryResponse);

        boolean result = orderService.placeOrder(orderDTO).join();

        assertThat(result).isFalse();
        verify(orderRepo, never()).save(any());
        verify(restTemplate, never()).put(any(), any(), any(), any());
        verify(orderEventProducer).sendOrderEvent("Order failed due to insufficient stock");
    }

    @Test
    void fallbackPlaceOrderReturnsFalseWhenInventoryServiceIsUnavailable() {
        OrderDTO orderDTO = buildOrderDTO("iphone_13", 1);

        boolean result = orderService.fallbackPlaceOrder(orderDTO, new RuntimeException("inventory down")).join();

        assertThat(result).isFalse();
        verify(orderRepo, never()).save(any());
        verify(orderEventProducer, times(1)).sendOrderEvent("Order failed due to inventory service issue");
    }

    private OrderDTO buildOrderDTO(String skuCode, int quantity) {
        return OrderDTO.builder()
                .orderLineItemsDtoList(List.of(
                        OrderLineItemsDTO.builder()
                                .skuCode(skuCode)
                                .price(BigDecimal.valueOf(1200))
                                .quantity(quantity)
                                .build()
                ))
                .build();
    }
}
