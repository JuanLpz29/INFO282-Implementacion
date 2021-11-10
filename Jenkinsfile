pipeline {
  agent {
    docker {image 'srittau/wsgi-base:latest'}
  }
  stages {
    stage('build') {
      steps {
        sh 'pip3 install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python3 test.py'
      }   
    }
    stage('Deploy') {
      options {
        skipDefaultCheckout()
      }
      steps {
        sh 'rm -rf /var/www/tent'
        sh 'mkdir /var/www/tent'
        sh 'cp -Rp build/** /var/www/tent'
        sh 'docker stop  || true && docker rm tent || true'
        sh 'docker run -dit --name tent -p 8008:80 -v /var/www/tent/:/usr/local/apache2/htdocs/ httpd:2.4'
      }
  }
}
}