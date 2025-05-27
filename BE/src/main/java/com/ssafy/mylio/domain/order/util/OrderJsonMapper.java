package com.ssafy.mylio.domain.order.util;

import com.ssafy.mylio.domain.order.dto.common.NutritionInfoDto;
import com.ssafy.mylio.global.error.code.ErrorCode;
import com.ssafy.mylio.global.error.exception.CustomException;
import com.ssafy.mylio.global.security.auth.UserPrincipal;
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

    public OrderResponseDto parse(String json, UserPrincipal user) {
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
            Integer storeId = data.path("store_id").asInt();

            List<ContentsResponseDto> contents = new ArrayList<>();
            JsonNode contentsNode = data.path("contents");

            if (contentsNode.isArray()) {
                for (JsonNode m : contentsNode) {
                    contents.add(toContentsDto(m));
                }
            } else if (!contentsNode.isMissingNode() && !contentsNode.isNull() && contentsNode.isObject()) {
                contents.add(toContentsDto(contentsNode));
            }


            List<CartResponseDto> cart = new ArrayList<>();
            if (data.has("cart") && data.get("cart").isArray()) {
                for (JsonNode c : data.path("cart")) {
                    cart.add(toCartDto(c));
                }
            }

            return OrderResponseDto.builder()
                    .storeId(storeId)
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
        int menuId = altInt(m, "menu_id", "id");
        Integer quantity = m.path("quantity").asInt();
        String name = altText(m, "name", "name_kr", "name_en");
        String desc = m.path("description").asText(null);
        Integer price = m.path("price").asInt(0);
        Integer base = m.path("base_price").asInt(price);
        Integer total = m.path("total_price").asInt(price);
        String img = m.path("image_url").asText(null);

        List<OptionsDto> options = new ArrayList<>();
        for (JsonNode o : m.path("options")) options.add(toOptionsDto(o));

        List<OptionsDto> selected = new ArrayList<>();
        for (JsonNode so : m.path("selected_options")) {
            OptionsDto dto = toOptionsDto(so);
            Integer selId = so.path("option_details").isEmpty() ? null : so.path("option_details").get(0).path("id").asInt();
            selected.add(dto.toBuilder().isSelected(true).selectedId(selId).build());
        }

        List<NutritionInfoDto> nutritionInfo = toNutritionList(m.path("nutrition"));

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
                .nutritionInfo(nutritionInfo)
                .build();
    }


    private CartResponseDto toCartDto(JsonNode c) {
        String cartId = c.path("cart_id").asText();
        Integer menuId = altInt(c, "menu_id", "id");
        Integer qty      = c.path("quantity").asInt();
        String name = altText(c, "name", "name_kr", "name_en");
        String desc      = c.path("description").asText(null);
        Integer price = c.path("price").asInt(0);
        Integer base     = c.path("base_price").asInt(price);
        Integer total    = c.path("total_price").asInt(price);
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

    private List<NutritionInfoDto> toNutritionList(JsonNode arr) {
        List<NutritionInfoDto> list = new ArrayList<>();
        if (arr.isMissingNode() || !arr.isArray()) return list;
        for (JsonNode n : arr) {
            list.add(NutritionInfoDto.builder()
                    .nutritionId(n.path("id").asInt())
                    .nutritionName(altText(n, "name", "name_en"))
                    .nutritionValue(n.path("value").asInt())
                    .nutritionType(n.path("unit").asText(null))
                    .build());
        }
        return list;
    }

    private String altText(JsonNode node, String... keys) {
        for (String k : keys) if (node.has(k)) return node.path(k).asText(null);
        return null;
    }

    private int altInt(JsonNode node, String primary, String alt) {
        return node.has(primary) ? node.path(primary).asInt() : node.path(alt).asInt();
    }
}
