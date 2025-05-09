package com.ssafy.mylio.domain.order.util;

import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.ssafy.mylio.domain.order.dto.common.OptionDetailsDto;
import com.ssafy.mylio.domain.order.dto.common.OptionsDto;
import com.ssafy.mylio.domain.order.dto.response.CartResponseDto;
import com.ssafy.mylio.domain.order.dto.response.ContentsResponseDto;
import com.ssafy.mylio.domain.order.dto.response.OrderResponseDto;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Component
@RequiredArgsConstructor
public class OrderJsonMapper {

    private final ObjectMapper snakeMapper = new ObjectMapper()
            .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

    public OrderResponseDto parse(String json) {
        try {
            JsonNode root = snakeMapper.readTree(json);
            JsonNode data = root.path("data");

            // root-level
            String screen   = root.path("screen_state").asText(null);
            String payment  = root.path("payment_method").isNull() ? null : root.path("payment_method").asText();

            // data-level
            String preText  = data.path("pre_text").asText(null);
            String postText = data.path("post_text").asText(null);
            String reply    = data.path("reply").isNull() ? null : data.path("reply").asText(null);
            String session  = data.path("session_id").asText(null);
            String lang     = data.path("language").asText(null);

            List<ContentsResponseDto> contents = new ArrayList<>();
            for (JsonNode m : (ArrayNode) data.path("contents")) contents.add(toContentsDto(m));

            List<CartResponseDto> cart = new ArrayList<>();
            for (JsonNode c : (ArrayNode) data.path("cart")) cart.add(toCartDto(c));

            return OrderResponseDto.builder()
                    .preText(preText)
                    .postText(postText)
                    .reply(reply)
                    .screenState(screen)
                    .language(lang)
                    .sessionId(session)
                    .payment(payment)
                    .cart(cart)
                    .contents(contents)
                    .build();
        } catch (IOException e) {
            throw new CustomException(ErrorCode.INTERNAL_SERVER_ERROR, "json Parse Error");
        }
    }

    private ContentsResponseDto toContentsDto(JsonNode m) {
        Integer menuId = m.path("menu_id").asInt();
        Integer quantity = m.path("quantity").asInt();
        String name = m.path("name").asText(null);
        String desc = m.path("description").asText(null);
        Integer base = m.path("base_price").asInt();
        Integer total = m.path("total_price").asInt();
        String img = m.path("image_url").asText(null);

        List<OptionsDto> options = new ArrayList<>();
        for (JsonNode o : m.path("options")) options.add(toOptionsDto(o));

        List<OptionsDto> selected = new ArrayList<>();
        for (JsonNode so : m.path("selected_options")) {
            OptionsDto dto = toOptionsDto(so);
            Integer selId = so.path("option_details").isEmpty() ? null : so.path("option_details").get(0).path("id").asInt();
            selected.add(dto.toBuilder().isSelected(true).selectedId(selId).build());
        }

        return ContentsResponseDto.builder()
                .menuId(menuId)
                .quantity(quantity)
                .name(name)
                .description(desc)
                .basePrice(base)
                .totalPrice(total)
                .imageUrl(img)
                .options(options)
                .selectedOption(selected)
                .build();
    }

    private CartResponseDto toCartDto(JsonNode c) {
        String cartId = c.path("cart_id").asText();
        Integer menuId   = c.path("menu_id").asInt();
        Integer qty      = c.path("quantity").asInt();
        String name      = c.path("name").asText(null);
        String desc      = c.path("description").asText(null);
        Integer base     = c.path("base_price").asInt();
        Integer total    = c.path("total_price").asInt();
        String imageUrl  = c.path("image_url").asText(null);

        List<OptionsDto> selected = new ArrayList<>();
        for (JsonNode so : c.path("selected_options")) selected.add(toOptionsDto(so));

        return CartResponseDto.builder()
                .cartId(cartId)
                .menuId(menuId)
                .quantity(qty)
                .name(name)
                .description(desc)
                .basePrice(base)
                .totalPrice(total)
                .imageUrl(imageUrl)
                .selectedOptions(selected)
                .build();
    }

    private OptionsDto toOptionsDto(JsonNode o) {
        Integer optionId = o.path("option_id").asInt();
        String optionName = o.path("option_name").asText(null);
        boolean required = o.path("required").asBoolean(false);
        boolean isSelected = o.path("is_selected").asBoolean(false);
        Integer selectedId = o.path("selected_id").isNull() ? null : o.path("selected_id").asInt();

        List<OptionDetailsDto> detailDtos = new ArrayList<>();
        for (JsonNode d : o.path("option_details")) {
            detailDtos.add(
                    OptionDetailsDto.builder()
                            .optionDetailId(d.path("id").asInt())
                            .optionDetailValue(d.path("value").asText())
                            .additionalPrice(d.path("additional_price").asInt())
                            .build());
        }

        return OptionsDto.builder()
                .optionId(optionId)
                .optionName(optionName)
                .required(required)
                .isSelected(isSelected)
                .selectedId(selectedId)
                .optionDetails(detailDtos)
                .build();
    }
}
