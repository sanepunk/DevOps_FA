pipeline {
    agent any

    environment {
        APP_NAME = "DevOps_FA"
        BUILD_DIR = "${WORKSPACE}/build"
        TEST_REPORTS_DIR = "${WORKSPACE}/test-reports"
        DEPLOY_DIR = "${WORKSPACE}/deploy"
    }

    stages {
        stage('Build') {
            steps {
                echo "🚀 Starting build stage..."
                sh '''
                    chmod +x ./build.sh
                    ./build.sh
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Starting test stage..."
                sh '''
                    chmod +x ./test.sh
                    ./test.sh
                '''
            }
            post {
                always {
                    junit '**/test-reports/*.xml'
                }
            }
        }

        stage('Deploy to Production') {
            when {
                branch 'master'  // Only deploy from master branch
            }
            steps {
                echo "📦 Starting production deployment..."
                sh '''
                    chmod +x ./production.sh
                    ./production.sh
                '''
            }
        }
    }

    post {
        always {
            echo "📄 Cleaning up workspace..."
            cleanWs()
        }
        success {
            echo "🎉 Pipeline completed successfully!"
            // You could add notifications here
            // slackSend channel: '#deployments', color: 'good', message: "Pipeline succeeded!"
        }
        failure {
            echo "❌ Pipeline failed!"
            // You could add notifications here
            // slackSend channel: '#deployments', color: 'danger', message: "Pipeline failed!"
        }
    }
}
