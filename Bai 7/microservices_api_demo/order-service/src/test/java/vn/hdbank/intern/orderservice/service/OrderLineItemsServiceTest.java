package vn.hdbank.intern.orderservice.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import vn.hdbank.intern.orderservice.dto.OrderLineItemsDTO;
import vn.hdbank.intern.orderservice.mapper.OrderLineItemsMapper;
import vn.hdbank.intern.orderservice.model.OrderLineItems;
import vn.hdbank.intern.orderservice.repository.OrderLineItemsRepo;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderLineItemsServiceTest {

    @Mock
    private OrderLineItemsRepo orderLineItemsRepo;

    @Mock
    private OrderLineItemsMapper orderLineItemsMapper;

    @InjectMocks
    private OrderLineItemsService orderLineItemsService;

    @Test
    void saveOrderLineItemsShouldReturnMappedDto() {
        OrderLineItemsDTO input = OrderLineItemsDTO.builder()
                .skuCode("iphone_13")
                .price(BigDecimal.valueOf(1200))
                .quantity(1)
                .build();

        OrderLineItems entity = OrderLineItems.builder()
                .skuCode("iphone_13")
                .price(BigDecimal.valueOf(1200))
                .quantity(1)
                .build();

        OrderLineItemsDTO output = OrderLineItemsDTO.builder()
                .id(10L)
                .skuCode("iphone_13")
                .price(BigDecimal.valueOf(1200))
                .quantity(1)
                .build();

        when(orderLineItemsMapper.toEntity(input)).thenReturn(entity);
        when(orderLineItemsRepo.save(entity)).thenReturn(entity);
        when(orderLineItemsMapper.toDTO(entity)).thenReturn(output);

        OrderLineItemsDTO result = orderLineItemsService.saveOrderLineItems(input);

        assertThat(result.getId()).isEqualTo(10L);
        assertThat(result.getSkuCode()).isEqualTo("iphone_13");
    }
}
