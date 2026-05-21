package vn.hdbank.intern.productservice.controller;

import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import vn.hdbank.intern.productservice.dto.BaseResponse;
import vn.hdbank.intern.productservice.dto.ProductDTO;
import vn.hdbank.intern.productservice.service.ProductService;

import java.util.List;

@RestController
@RequestMapping("/api/product")
@AllArgsConstructor
public class ProductController {

    private final ProductService productService;

    @PostMapping
    public ResponseEntity<BaseResponse> createProduct(@RequestBody ProductDTO product) {
        productService.createProduct(product);
        return ResponseEntity.status(HttpStatus.CREATED).body(BaseResponse.builder()
                .status("success")
                .message("Add Product success")
                .build());
    }

    @GetMapping
    public ResponseEntity<Object> getAllProducts(
            @RequestParam(name = "page", required = false) Integer page,
            @RequestParam(name = "size", required = false) Integer size) {
        
        if (page == null || size == null) {
            return ResponseEntity.ok().body(productService.getAllProducts());
        }
        
        return ResponseEntity.ok().body(productService.getAllProducts(org.springframework.data.domain.PageRequest.of(page, size)));
    }
}
