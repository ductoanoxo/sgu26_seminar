package vn.hdbank.intern.orderservice.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.client.RestTemplate;
import vn.hdbank.intern.orderservice.dto.BaseResponse;
import vn.hdbank.intern.orderservice.dto.OrderDTO;
import vn.hdbank.intern.orderservice.dto.OrderLineItemsDTO;
import vn.hdbank.intern.orderservice.listener.OrderEventProducer;
import vn.hdbank.intern.orderservice.model.Order;
import vn.hdbank.intern.orderservice.repository.OrderRepo;

import java.math.BigDecimal;
import java.util.List;
import java.util.concurrent.CompletableFuture;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.contains;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceUnitTest {

    @Mock
    private OrderRepo orderRepo;

    @Mock
    private RestTemplate restTemplate;

    @Mock
    private OrderEventProducer orderEventProducer;

    @InjectMocks
    private OrderService orderService;

    @Test
    void placeOrderShouldSucceedWhenItemsAreInStock() {
        OrderLineItemsDTO item = OrderLineItemsDTO.builder()
                .skuCode("iphone_13")
                .price(BigDecimal.valueOf(1200))
                .quantity(1)
                .build();

        OrderDTO request = OrderDTO.builder()
                .orderLineItemsDtoList(List.of(item))
                .build();

        when(restTemplate.getForObject(
                eq("http://INVENTORY-SERVICE/v1/api/inventory?skuCode=iphone_13"),
                eq(BaseResponse.class)))
                .thenReturn(BaseResponse.builder()
                        .skuCode("iphone_13")
                        .isInStock(true)
                        .quantity(10)
                        .build());

        when(orderRepo.save(any(Order.class))).thenAnswer(invocation -> invocation.getArgument(0));

        CompletableFuture<Boolean> result = orderService.placeOrder(request);

        assertThat(result.join()).isTrue();
        verify(orderRepo).save(any(Order.class));
        verify(restTemplate).put(contains("/v1/api/inventory/updateStock?skuCode=iphone_13&quantity=1"), eq(null));
        verify(orderEventProducer).sendOrderEvent(contains("has been placed successfully"));
    }

    @Test
    void placeOrderShouldFailWhenItemOutOfStock() {
        OrderLineItemsDTO item = OrderLineItemsDTO.builder()
                .skuCode("iphone_17")
                .price(BigDecimal.valueOf(1200))
                .quantity(1)
                .build();

        OrderDTO request = OrderDTO.builder()
                .orderLineItemsDtoList(List.of(item))
                .build();

        when(restTemplate.getForObject(
                eq("http://INVENTORY-SERVICE/v1/api/inventory?skuCode=iphone_17"),
                eq(BaseResponse.class)))
                .thenReturn(BaseResponse.builder()
                        .skuCode("iphone_17")
                        .isInStock(false)
                        .quantity(0)
                        .build());

        CompletableFuture<Boolean> result = orderService.placeOrder(request);

        assertThat(result.join()).isFalse();
        verify(orderRepo, never()).save(any(Order.class));
        verify(orderEventProducer, never()).sendOrderEvent(contains("has been placed successfully"));
    }
}
