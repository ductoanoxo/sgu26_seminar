package vn.hdbank.intern.productservice.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import vn.hdbank.intern.productservice.model.Product;

public interface ProductRepository extends MongoRepository<Product, String> {
}
