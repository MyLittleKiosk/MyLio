pipeline {
  agent any

  environment {
    PREVIEW_TAG    = "${env.BRANCH_NAME.replaceAll('/', '-')}"
    PREVIEW_DOMAIN = "mr-${env.PREVIEW_TAG}.preview.example.com"
    // FE_APP 은 Detect stage 에서 결정
  }

  stages {
    stage('Detect FE target') {
      steps {
        script {
          /* Merge Request 빌드일 땐 CHANGE_BRANCH가
             원본 브랜치(ex. FE/admin/feat/..)를 들고 있음          */
          def ref = env.CHANGE_BRANCH ?: env.BRANCH_NAME
          def tokens = ref.tokenize('/')
          if (tokens.size() < 2) {
            error "브랜치명에서 FE 앱을 찾지 못했습니다. (ref=${ref})"
          }
          env.FE_APP = tokens[1]    // admin 또는 service
          echo "▶ FE_APP = ${env.FE_APP}"
        }
      }
    }

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

  post {
    cleanup {
      sh """
        docker-compose -f docker-compose.preview.yml \\
          --project-name fe-preview-${PREVIEW_TAG} down -v || true
        docker image rm -f fe-preview:${PREVIEW_TAG} || true
      """
    }
  }
}
