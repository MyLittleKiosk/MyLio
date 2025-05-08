package com.ssafy.mylio.global.util;

import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.model.CannedAccessControlList;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.PutObjectRequest;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStream;
import java.time.LocalDate;
import java.util.UUID;

@Component
@RequiredArgsConstructor
public class S3Util {

    private final AmazonS3 amazonS3;
    @Value("${cloud.aws.s3.bucket}")
    private String bucket;

    public String uploadFile(MultipartFile imageFile) throws IOException {
        if(imageFile == null) return null;

        // 키 생성 (중복 방지 및 디렉터리 관리)
        String key = generateKey(imageFile.getOriginalFilename());

        // 메타데이터 설정
        ObjectMetadata metadata = new ObjectMetadata();
        metadata.setContentType(imageFile.getContentType());
        metadata.setContentLength(imageFile.getSize());

        // 4) 업로드 요청 (InputStream 스트리밍)
        try (InputStream is = imageFile.getInputStream()) {
            PutObjectRequest request = new PutObjectRequest(bucket, key, is, metadata)
                    .withCannedAcl(CannedAccessControlList.Private);  // 기본 비공개
            amazonS3.putObject(request);
        }

        return amazonS3.getUrl(bucket, key).toString();
    }

    private String generateKey(String filename){
        String ext = StringUtils.getFilenameExtension(filename);
        return LocalDate.now() +"/" + UUID.randomUUID() + "." + ext;
    }

}
