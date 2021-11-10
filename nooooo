pipeline {
    agent none
    stage('Install') {
        agent {   
            docker {
                    image 'srittau/wsgi-base:latest'
                    args '-u root:root'
                    }
            }
            steps {
                sh 'pip3 install -r requirements.txt'
            }
    }
    stage('Archive') {
        agent {
            label 'master'
        }
            steps {
                archiveArtifacts '**'
            }
    }
    stage('Deploy') {
        agent {
            label 'master'
        }
        options {
            skipDefaultCheckout()
        }
        steps {
            sh 'rm -rf /var/www/tent'
            sh 'mkdir /var/www/tent'
            sh 'cp -Rp ** /var/www/tent'
            sh 'docker stop tent || true'
            sh 'docker run -dit --name tent -p 8008:80 -v /var/www/tent/:/var/www/tent srittau/wsgi-base:latest'
            sh 'docker exec tent a2ensite tent.conf'
            sh 'docker exec tent service apache2 restart'
        }
    }
}