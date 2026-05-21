package vn.hdbank.intern.orderservice.mapper;

import org.junit.jupiter.api.Test;
import vn.hdbank.intern.orderservice.dto.OrderLineItemsDTO;
import vn.hdbank.intern.orderservice.model.OrderLineItems;

import java.math.BigDecimal;

import static org.assertj.core.api.Assertions.assertThat;

class OrderLineItemsMapperTest {

    private final OrderLineItemsMapper mapper = new OrderLineItemsMapper();

    @Test
    void toEntityShouldMapAllFields() {
        OrderLineItemsDTO dto = OrderLineItemsDTO.builder()
                .id(1L)
                .skuCode("iphone_13")
                .price(BigDecimal.valueOf(1200))
                .quantity(2)
                .build();

        OrderLineItems entity = mapper.toEntity(dto);

        assertThat(entity).isNotNull();
        assertThat(entity.getId()).isEqualTo(1L);
        assertThat(entity.getSkuCode()).isEqualTo("iphone_13");
        assertThat(entity.getPrice()).isEqualByComparingTo("1200");
        assertThat(entity.getQuantity()).isEqualTo(2);
    }

    @Test
    void toDtoShouldMapAllFields() {
        OrderLineItems entity = OrderLineItems.builder()
                .id(2L)
                .skuCode("iphone_15")
                .price(BigDecimal.valueOf(1500))
                .quantity(1)
                .build();

        OrderLineItemsDTO dto = mapper.toDTO(entity);

        assertThat(dto).isNotNull();
        assertThat(dto.getId()).isEqualTo(2L);
        assertThat(dto.getSkuCode()).isEqualTo("iphone_15");
        assertThat(dto.getPrice()).isEqualByComparingTo("1500");
        assertThat(dto.getQuantity()).isEqualTo(1);
    }

    @Test
    void shouldReturnNullWhenInputIsNull() {
        assertThat(mapper.toDTO(null)).isNull();
        assertThat(mapper.toEntity(null)).isNull();
    }
}
