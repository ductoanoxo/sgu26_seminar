package vn.hdbank.intern.apigateway.config;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class GatewayConfig {

    @Bean
    public RouteLocator customRouteLocator(RouteLocatorBuilder builder) {
        return builder.routes()
                // /api/product/** -> product-service:/api/product/**
                .route("product-service", r -> r
                        .path("/api/product/**")
                        .uri("lb://product-service"))
                // /api/order/** -> order-service:/v1/api/order/**
                .route("order-service", r -> r
                        .path("/api/order/**")
                        .filters(f -> f.rewritePath("/api/order(?<segment>.*)", "/v1/api/order${segment}"))
                        .uri("lb://order-service"))
                // /api/inventory/** -> inventory-service:/v1/api/inventory/**
                .route("inventory-service", r -> r
                        .path("/api/inventory/**")
                        .filters(f -> f.rewritePath("/api/inventory(?<segment>.*)", "/v1/api/inventory${segment}"))
                        .uri("lb://inventory-service"))
                .build();
    }
}
