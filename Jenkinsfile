pipeline {
  agent any
  environment {
    DOCKER_HUB_CREDS = credentials('docker-hub-id')
    BACKEND_IMG = 'bambain/bmi-backend'
    FRONTEND_IMG = 'bambain/bmi-frontend'
  }

  stages {
    stage('Cloner le dépôt') {
      steps {
        git 'https://github.com/bams-dev/bmi-app.git'
      }
    }

    stage('Build des images') {
      steps {
        script {
          docker.build("${BACKEND_IMG}", "./backend")
          docker.build("${FRONTEND_IMG}", "./frontend")
        }
      }
    }

    stage('Push sur Docker Hub') {
      steps {
        script {
          docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-id') {
            docker.image("${BACKEND_IMG}").push()
            docker.image("${FRONTEND_IMG}").push()
          }
        }
      }
    }

    stage('Déploiement') {
      steps {
        sh 'docker-compose up -d'
      }
    }

    stage('Notification') {
      steps {
        mail to: 'itbambainza@yahoo.com',
             subject: '✅ Déploiement Réussi',
             body: 'Le projet IMC a été déployé avec succès avec Jenkins.'
      }
    }
  }
}
