package com.ssafy.mylio.domain.sales.scheduler;

import com.ssafy.mylio.domain.sales.service.CategorySalesService;
import com.ssafy.mylio.domain.sales.service.PaymentSalesService;
import com.ssafy.mylio.domain.sales.service.TotalSalesService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Slf4j
@Component
@RequiredArgsConstructor
public class SalesScheduler {

    private final CategorySalesService categorySalesService;
    private final PaymentSalesService paymentSalesService;
    private final TotalSalesService totalSalesService;

    @Scheduled(cron = "0 0 0 * * *")
    public void getSalesByCategory (){
        log.info("일별 카테고리 통계 스케쥴러 시작 : {}", LocalDateTime.now());
        LocalDate yesterday = LocalDate.now().minusDays(1);
        try{
            categorySalesService.createCategorySales(yesterday);
            log.info("카테고리 통계 스케줄러 완료: {}", LocalDateTime.now());
        } catch (Exception e){
            log.error("카테고리 통계 생성 중 오류 발생: {}", e.getMessage(), e);
        }
    }

    @Scheduled(cron = "0 0 0 * * *")
    public void getSalesByPayment(){
        log.info("결제방법 통계 스케줄러 시작 : {}", LocalDateTime.now());
        LocalDate yesterday = LocalDate.now().minusDays(1);
        try{
            paymentSalesService.createPaymentSales(yesterday);
            log.info("결제방법 통계 스케줄러 완료: {}", LocalDateTime.now());
        } catch (Exception e){
            log.error("결제방법 통계 생성 중 오류 발생: {}", e.getMessage(), e);
        }
    }

    @Scheduled(cron = "0 0 0 * * *")
    public void getSalesSummary() {
        log.info("일,월,연도 통계 스케줄러 시작 : {}", LocalDateTime.now());
        LocalDate yesterday = LocalDate.now().minusDays(1);
        try{
            totalSalesService.createSalesSummary(yesterday);
            log.info("일,월,연도  통계 스케줄러 완료: {}", LocalDateTime.now());
        } catch (Exception e){
            log.error("일,월,연도  통계 생성 중 오류 발생: {}", e.getMessage(), e);
        }
    }


}
