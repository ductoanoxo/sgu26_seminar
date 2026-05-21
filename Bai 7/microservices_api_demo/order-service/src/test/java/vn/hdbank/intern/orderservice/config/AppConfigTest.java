package vn.hdbank.intern.orderservice.config;

import org.junit.jupiter.api.Test;
import org.springframework.web.client.RestTemplate;

import static org.assertj.core.api.Assertions.assertThat;

class AppConfigTest {

    @Test
    void restTemplateBeanShouldBeCreated() {
        AppConfig config = new AppConfig();

        RestTemplate restTemplate = config.restTemplate();

        assertThat(restTemplate).isNotNull();
    }
}
