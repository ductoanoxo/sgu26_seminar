package vn.hdbank.intern.orderservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class OrderLineItemsDTO {

    private Long id;
    @NotBlank(message = "skuCode must not be blank")
    private String skuCode;
    @NotNull(message = "price must not be null")
    @Positive(message = "price must be greater than 0")
    private BigDecimal price;
    @NotNull(message = "quantity must not be null")
    @Positive(message = "quantity must be greater than 0")
    private Integer quantity;
}
