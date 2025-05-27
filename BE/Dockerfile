# ───────── 1단계 : Build ─────────
FROM eclipse-temurin:17-jdk-alpine AS builder
WORKDIR /app

# bash 설치 + gradlew 실행권한
RUN apk add --no-cache bash
COPY gradlew settings.gradle* build.gradle* gradle/ /app/
COPY gradle /app/gradle
RUN chmod +x gradlew

# 의존성 레이어 (캐시 목적)
RUN ./gradlew dependencies --no-daemon

# 소스 복사 후 실제 빌드
COPY src /app/src
RUN ./gradlew clean bootJar --no-daemon -x test

# ───────── 2단계 : Runtime ─────────
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080
ENTRYPOINT ["java","-XX:+UseContainerSupport","-jar","/app/app.jar"]
