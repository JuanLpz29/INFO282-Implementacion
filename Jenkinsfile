pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {pipeline {
  agent any
  stages {
    stage('Build') {
      parallel {
        stage('Build') {
          steps {
            sh 'pip3 install -r requirements.txt'
          }
        }
      }
    }
    
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
        sh "sudo nohup python3 app.py > log.txt 2>&1 &"
      }
    }
  }
  
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}
        stage('Build') {
          steps {
            sh 'echo "building the repo"'
          }
        }
      }
    }
    
    stage('Deploy')
    {
      steps {
        echo "deploying the application"
        sh "sudo nohup python3 app.py > log.txt 2>&1 &"
      }
    }
  }
  
  post {
        always {
            echo 'The pipeline completed'
            junit allowEmptyResults: true, testResults:'**/test_reports/*.xml'
        }
        success {                   
            echo "Flask Application Up and running!!"
        }
        failure {
            echo 'Build stage failed'
            error('Stopping early…')
        }
      }
}