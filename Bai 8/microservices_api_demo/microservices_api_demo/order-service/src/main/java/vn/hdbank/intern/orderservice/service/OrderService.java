package vn.hdbank.intern.orderservice.service;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import io.github.resilience4j.timelimiter.annotation.TimeLimiter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import vn.hdbank.intern.orderservice.dto.BaseResponse;
import vn.hdbank.intern.orderservice.dto.OrderDTO;
import vn.hdbank.intern.orderservice.dto.OrderLineItemsDTO;
import vn.hdbank.intern.orderservice.listener.OrderEventProducer;
import vn.hdbank.intern.orderservice.model.Order;
import vn.hdbank.intern.orderservice.model.OrderLineItems;
import vn.hdbank.intern.orderservice.repository.OrderRepo;

import java.util.List;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Slf4j
@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepo orderRepo;
    private final RestTemplate restTemplate;
    private final OrderEventProducer orderEventProducer;

    @Value("${app.inventory-service.base-url:http://INVENTORY-SERVICE/v1/api/inventory}")
    private String inventoryServiceBaseUrl;

    @CircuitBreaker(name = "inventory-service", fallbackMethod = "fallbackPlaceOrder")
    @Retry(name = "inventory-service")
    @TimeLimiter(name = "inventory-service")
    public CompletableFuture<Boolean> placeOrder(OrderDTO orderDTO) {
        return CompletableFuture.supplyAsync(() -> {
            boolean allInStock = orderDTO.getOrderLineItemsDtoList().stream()
                    .allMatch(this::isItemAvailable);

            if (!allInStock) {
                orderEventProducer.sendOrderEvent("Order failed due to insufficient stock");
                return false;
            }

            Order order = Order.builder()
                    .orderNumber(UUID.randomUUID().toString())
                    .build();

            List<OrderLineItems> orderLineItems = orderDTO.getOrderLineItemsDtoList().stream()
                    .map(item -> mapToOrderLineItem(item, order))
                    .toList();

            order.setOrderLineItems(orderLineItems);

            orderLineItems.forEach(item -> updateInventoryStock(item.getSkuCode(), item.getQuantity()));
            orderRepo.save(order);
            orderEventProducer.sendOrderEvent("Order " + order.getOrderNumber() + " has been placed successfully");
            return true;
        });
    }

    public CompletableFuture<Boolean> fallbackPlaceOrder(OrderDTO orderDTO, Throwable throwable) {
        log.error("Inventory Service is unavailable while placing an order: {}", throwable.getMessage());
        orderEventProducer.sendOrderEvent("Order failed due to inventory service issue");
        return CompletableFuture.completedFuture(false);
    }

    private boolean isItemAvailable(OrderLineItemsDTO orderLineItemsDTO) {
        BaseResponse response = restTemplate.getForObject(
                inventoryServiceBaseUrl + "?skuCode={skuCode}",
                BaseResponse.class,
                orderLineItemsDTO.getSkuCode()
        );

        return response != null
                && response.isInStock()
                && response.getQuantity() >= orderLineItemsDTO.getQuantity();
    }

    private void updateInventoryStock(String skuCode, int quantity) {
        restTemplate.put(
                inventoryServiceBaseUrl + "/updateStock?skuCode={skuCode}&quantity={quantity}",
                null,
                skuCode,
                quantity
        );
    }

    private OrderLineItems mapToOrderLineItem(OrderLineItemsDTO orderLineItemsDTO, Order order) {
        return OrderLineItems.builder()
                .skuCode(orderLineItemsDTO.getSkuCode())
                .price(orderLineItemsDTO.getPrice())
                .quantity(orderLineItemsDTO.getQuantity())
                .order(order)
                .build();
    }
}
