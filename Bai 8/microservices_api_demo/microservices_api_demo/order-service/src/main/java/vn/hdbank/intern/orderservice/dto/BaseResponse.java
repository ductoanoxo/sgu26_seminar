package vn.hdbank.intern.orderservice.dto;


import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class BaseResponse {
    private String skuCode;
    private boolean isInStock;
    private int quantity;
}
