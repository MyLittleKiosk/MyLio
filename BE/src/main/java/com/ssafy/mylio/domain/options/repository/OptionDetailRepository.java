package com.ssafy.mylio.domain.options.repository;

import com.ssafy.mylio.domain.options.entity.OptionDetail;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OptionDetailRepository extends JpaRepository<OptionDetail, Integer> {
    List<OptionDetail> findAllByOptionsIdIn(List<Integer> optionsIds);
    List<OptionDetail> findAllByOptionsId(Integer optionsId);
}
