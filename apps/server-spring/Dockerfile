FROM openjdk:8-jdk-alpine
VOLUME /tmp
ARG JAR_FILE=target/qiyun-admin.jar
COPY ${JAR_FILE} app.jar
COPY upload /app/upload
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/app.jar"]