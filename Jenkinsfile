pipeline {
  agent any

  stages {
    /* ─────────── 1) 공통 변수 계산 ─────────── */
    steps {
      script {
        /* ───── 1) 빌드 대상 브랜치·MR 정보 ───── */
        def ref = env.CHANGE_BRANCH ?: env.BRANCH_NAME        // 소스 ref
        def mrId = env.CHANGE_ID                              // MR 번호 (null ⇢ 일반 브랜치 빌드)

        /* ───── 2) FE 앱(admin | service) 추출 ───── */
        def tokens = ref.tokenize('/')
        if (tokens.size() < 2) error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
        env.FE_APP = tokens[1]

        /* ───── 3) 프로젝트·이미지·도메인 네이밍 ───── */
        if (mrId) {                                  // MR 빌드인 경우
          env.PROJECT_NAME  = "fe-preview-${mrId}"   // docker-compose --project-name
          env.IMAGE_TAG     = "mr-${mrId}"           // fe-preview:mr-69
          env.PREVIEW_PATH  = "/test/${mrId}/"       // path-based 프록시용
        } else {                                     // 브랜치 빌드(예: dev, main)
          def safe = ref.replaceAll('/', '-')        // / → -
                        .toLowerCase()                // 소문자
                         .replaceAll('[^a-z0-9_-]', '')// 허용 문자만
          env.PROJECT_NAME  = "fe-preview-${safe}"
          env.IMAGE_TAG     = "${safe}"
          env.PREVIEW_PATH  = "/test/${safe}/"
        }

        echo "▶ FE_APP        = ${env.FE_APP}"
        echo "▶ PROJECT_NAME  = ${env.PROJECT_NAME}"
        echo "▶ IMAGE_TAG     = ${env.IMAGE_TAG}"
        echo "▶ PREVIEW_PATH  = ${env.PREVIEW_PATH}"
      }
    }
  }

    /* ─────────── 2) Preview 앱 빌드·배포 ─────────── */
    stage('Preview up (build+run)') {
      steps {
        sh """
          docker-compose \\
            -f docker-compose.preview.yml \\
            --project-name fe-preview-${PREVIEW_TAG} \\
            up -d --build --remove-orphans
        """
      }
    }
  }

  /* ─────────── 3) MR 종료 시 정리 ─────────── */
  post {
    always {
      script {
        /* gitlabActionType: OPEN | REOPEN | UPDATE | MERGE | CLOSE (GitLab Branch Source) */
        if (env.gitlabActionType in ['CLOSE', 'MERGE']) {
          echo "🧹 MR ${gitlabActionType} → cleaning review app"
          sh """
            docker-compose -f docker-compose.preview.yml \
              --project-name fe-preview-${TAG} down -v || true
            docker image rm -f fe-preview:${TAG} || true
          """
        } else {
          echo "🔖 MR still open (${gitlabActionType}) – keep preview container running"
         }
      }
    }
  }
}
