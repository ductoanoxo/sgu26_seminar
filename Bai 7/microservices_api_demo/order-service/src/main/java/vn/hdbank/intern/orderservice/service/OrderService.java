package vn.hdbank.intern.orderservice.service;

import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import io.github.resilience4j.retry.annotation.Retry;
import io.github.resilience4j.timelimiter.annotation.TimeLimiter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
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

    private static final String INVENTORY_SERVICE_URL = "http://INVENTORY-SERVICE/v1/api/inventory?skuCode=";
    private static final String INVENTORY_UPDATE_URL = "http://INVENTORY-SERVICE/v1/api/inventory/updateStock?skuCode=%s&quantity=%d";

    @CircuitBreaker(name = "inventory-service", fallbackMethod = "fallbackPlaceOrder")
    @Retry(name = "inventory-service")
    @TimeLimiter(name = "inventory-service")
    public CompletableFuture<Boolean> placeOrder(OrderDTO orderDTO) {
        return CompletableFuture.supplyAsync(() -> placeOrderSync(orderDTO));
    }

    private boolean placeOrderSync(OrderDTO orderDTO) {
        if (orderDTO == null || orderDTO.getOrderLineItemsDtoList() == null || orderDTO.getOrderLineItemsDtoList().isEmpty()) {
            log.warn("Order request is empty");
            return false;
        }

        List<OrderLineItemsDTO> orderItems = orderDTO.getOrderLineItemsDtoList();
        boolean allInStock = orderItems.stream().allMatch(this::isInStock);

        if (!allInStock) {
            log.warn("Order not placed because at least one item is out of stock");
            return false;
        }

        Order order = Order.builder()
                .orderNumber(UUID.randomUUID().toString())
                .build();

        List<OrderLineItems> orderLineItems = orderItems.stream()
                .map(item -> OrderLineItems.builder()
                        .skuCode(item.getSkuCode())
                        .price(item.getPrice())
                        .quantity(item.getQuantity())
                        .order(order)
                        .build())
                .toList();

        order.setOrderLineItemsList(orderLineItems);
        orderRepo.save(order);
        orderItems.forEach(item -> updateInventoryStock(item.getSkuCode(), item.getQuantity()));

        orderEventProducer.sendOrderEvent("Order " + order.getOrderNumber() + " has been placed successfully");
        return true;
    }

    private boolean isInStock(OrderLineItemsDTO orderLineItemsDTO) {
        BaseResponse response = restTemplate.getForObject(INVENTORY_SERVICE_URL + orderLineItemsDTO.getSkuCode(), BaseResponse.class);
        return response != null
                && response.isInStock()
                && response.getQuantity() >= orderLineItemsDTO.getQuantity();
    }

    private CompletableFuture<Boolean> fallbackPlaceOrder(OrderDTO orderDTO, Throwable throwable) {
        log.error("Inventory service is unavailable: {}", throwable.getMessage());
        orderEventProducer.sendOrderEvent("Order failed due to inventory service issue");
        return CompletableFuture.completedFuture(false);
    }

    private void updateInventoryStock(String skuCode, int quantity) {
        String url = String.format(INVENTORY_UPDATE_URL, skuCode, quantity);
        restTemplate.put(url, null);
    }

}
