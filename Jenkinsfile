pipeline{
	agent {label 'wrkr'}
	tools {
		maven 'mvn 3.5'
	}
	stages{
		stage('git clone'){
			steps{
			 checkout scm
			}
			}
		stage('build'){
			steps{
			sh 'mvn package'
			}
			}
		}
}
