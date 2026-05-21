package vn.hdbank.intern.orderservice.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import vn.hdbank.intern.orderservice.dto.OrderDTO;
import vn.hdbank.intern.orderservice.service.OrderService;

import java.util.concurrent.CompletableFuture;

@Slf4j
@RestController
@RequestMapping({"/api/order", "/v1/api/order"})
@RequiredArgsConstructor
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    public CompletableFuture<ResponseEntity<String>> placeOrder(@Valid @RequestBody OrderDTO orderDTO) {
        return orderService.placeOrder(orderDTO)
                .thenApply(orderPlaced -> {
                    if (orderPlaced) {
                        log.info("Order placed successfully");
                        return ResponseEntity.status(HttpStatus.CREATED).body("Order Placed");
                    }

                    log.info("Order placement failed");
                    return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Failed to Place Order");
                });
    }
}
