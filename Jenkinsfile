pipeline {
    agent {
        docker {
            image 'srittau/wsgi-base:latest'
            args '-u root:root'
            }
            }
    stages {
          stage('Install') {
            steps {
                sh 'pip3 install --user -r requirements.txt'
            }
          }
          stage('Archive') {
            steps {
              archiveArtifacts '**'
            }
          }
    stage('Deploy') {
      options {
        skipDefaultCheckout()
      }
      steps {
        sh 'rm -rf /var/www/tent'
        sh 'mkdir /var/www/tent'
        sh 'cp -Rp ** /var/www/tent'
        sh 'docker stop tent'
        sh 'docker run -dit --name tent -p 8008:80 -v /var/www/tent/:/var/www/tent srittau/wsgi-base:latest'
        sh 'docker exec tent a2ensite tent.conf'
        sh 'docker exec tent service apache2 restart'
      }
  }
}
}