package vn.hdbank.intern.orderservice.dto;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class OrderDTO {
    private Long id;
    private String orderNumber;
    @Valid
    @NotEmpty(message = "orderLineItemsDtoList must not be empty")
    private List<OrderLineItemsDTO> orderLineItemsDtoList;

}
