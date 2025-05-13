package com.ssafy.mylio.domain.order.service;

import com.ssafy.mylio.domain.menu.entity.Menu;
import com.ssafy.mylio.domain.menu.repository.MenuRepository;
import com.ssafy.mylio.domain.options.entity.MenuOptionMap;
import com.ssafy.mylio.domain.options.entity.OptionDetail;
import com.ssafy.mylio.domain.options.repository.MenuOptionRepository;
import com.ssafy.mylio.domain.order.dto.common.OptionDetailsDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;
import com.ssafy.mylio.domain.order.util.OrderJsonMapper;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;
import java.util.*;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderValidatorService {

    private final MenuRepository menuRepository;
    private final MenuOptionRepository menuOptionRepository;
    private final GptPromptService gptPromptService;
    private final OrderJsonMapper mapper;

    /** 리액티브 진입점 */
    public Mono<OrderResponseDto> validate(String pyJson, UserPrincipal user) {
        log.info("옵션 검증 로직 진입 : {}", pyJson);
        return Mono.fromCallable(() -> parseAndValidate(mapper.parse(pyJson, user), user))
                .subscribeOn(Schedulers.boundedElastic());
    }

    // 검증 및 누락 옵션 프롬프트 생성
    @Transactional(readOnly = true)
    protected OrderResponseDto parseAndValidate(OrderResponseDto order, UserPrincipal user) {

        List<String> missingOpts = new ArrayList<>();
        List<ContentsResponseDto> fixedContents = order.getContents().stream()
                .map(c -> validateAndCorrect(c, missingOpts))
                .toList();

        if (!missingOpts.isEmpty() && order.getReply() == null) {
            // reply가 없을때 GPT 호출
            String reply = gptPromptService.buildAskRequiredOptionPrompt(missingOpts, order.getLanguage());
            return order.toBuilder()
                    .contents(fixedContents)
                    .reply(reply)
                    .screenState(order.getScreenState())
                    .build();
        }

        return order.toBuilder().contents(fixedContents).build();
    }

    // ---------------- 검증 & 교정 ----------------

    private ContentsResponseDto validateAndCorrect(ContentsResponseDto content, List<String> missingOptNames) {
        Menu menu = menuRepository.findById(content.getMenuId())
                .orElseThrow(() -> new CustomException(ErrorCode.MENU_NOT_FOUND, "menuId", content.getMenuId()));

        List<MenuOptionMap> maps = menuOptionRepository.findAllWithDetailByMenuId(content.getMenuId());
        if (maps.isEmpty()) return content;

        Map<Integer, List<MenuOptionMap>> grouped = maps.stream()
                .collect(Collectors.groupingBy(m -> m.getOptions().getId()));

        List<OptionsDto> canonical = new ArrayList<>();
        for (var entry : grouped.entrySet()) {
            Integer optionId = entry.getKey();
            List<MenuOptionMap> group = entry.getValue();

            String optionNameKr = group.get(0).getOptions().getOptionNameKr();
            boolean required = group.stream().anyMatch(MenuOptionMap::getIsRequired);

            List<OptionDetailsDto> detailDtos = group.stream()
                    .map(MenuOptionMap::getOptionDetail)
                    .map(this::toOptionDetailsDto)
                    .toList();

            Optional<OptionsDto> incoming = content.getOptions().stream()
                    .filter(o -> Objects.equals(o.getOptionId(), optionId))
                    .findFirst();

            boolean isSelected = incoming.map(OptionsDto::isSelected).orElse(false);
            Integer selectedId = incoming.map(OptionsDto::getSelectedId).orElse(null);

            if (required && !isSelected) missingOptNames.add(optionNameKr);

            canonical.add(OptionsDto.builder()
                    .optionId(optionId)
                    .optionName(optionNameKr)
                    .required(required)
                    .isSelected(isSelected)
                    .selectedId(selectedId)
                    .optionDetails(detailDtos)
                    .build());
        }

        List<OptionsDto> selectedOnly = canonical.stream()
                .filter(OptionsDto::isSelected)
                .map(o -> {
                    OptionDetailsDto sel = o.getOptionDetails().stream()
                            .filter(d -> Objects.equals(d.getOptionDetailId(), o.getSelectedId()))
                            .findFirst().orElse(null);
                    return o.toBuilder().optionDetails(sel == null ? List.of() : List.of(sel)).build();
                }).toList();

        // 이미지 URL이 없으면 DB에서 조회해서 넣기
        return content.toBuilder()
                .options(canonical)
                .imageUrl((content.getImageUrl() == null || content.getImageUrl().isEmpty()) ? menu.getImageUrl() : content.getImageUrl())
                .selectedOption(selectedOnly)
                .build();
    }

    private OptionDetailsDto toOptionDetailsDto(OptionDetail d) {
        return OptionDetailsDto.builder()
                .optionDetailId(d.getId())
                .optionDetailValue(d.getValue())
                .additionalPrice(d.getAdditionalPrice())
                .build();
    }
}
