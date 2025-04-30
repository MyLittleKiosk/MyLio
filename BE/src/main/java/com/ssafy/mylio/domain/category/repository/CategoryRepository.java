package com.ssafy.mylio.domain.category.repository;

import com.ssafy.mylio.domain.category.entity.Category;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CategoryRepository extends JpaRepository<Category, Integer> {
}
