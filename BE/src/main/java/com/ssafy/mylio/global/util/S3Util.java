package com.ssafy.mylio.global.util;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.GetUrlRequest;
import software.amazon.awssdk.services.s3.model.ObjectCannedACL;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;

import java.io.IOException;
import java.io.InputStream;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class S3Util {

    private final S3Client s3Client;
    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    public String uploadFile(MultipartFile imageFile) throws IOException {
        if(imageFile == null) return null;

        // 키 생성 (중복 방지 및 디렉터리 관리)
        String key = generateKey(imageFile.getOriginalFilename());

        PutObjectRequest putReq = PutObjectRequest.builder()
                .bucket(bucket)
                .key(key)
                .contentType(imageFile.getContentType())
                .contentLength(imageFile.getSize())
                .acl(ObjectCannedACL.PRIVATE)
                .build();

        // 3) 스트림과 함께 업로드
        try (InputStream is = imageFile.getInputStream()) {
            s3Client.putObject(putReq,
                    RequestBody.fromInputStream(is, imageFile.getSize()));
        }

        // 4) 업로드된 객체의 URL 생성
        GetUrlRequest urlReq = GetUrlRequest.builder()
                .bucket(bucket)
                .key(key)
                .build();


        return s3Client.utilities().getUrl(urlReq).toString();
    }

    private String generateKey(String filename){
        String ext = StringUtils.getFilenameExtension(filename);
        return "menu" +"/" + UUID.randomUUID() + "." + ext;
    }

}
