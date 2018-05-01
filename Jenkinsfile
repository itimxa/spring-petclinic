pipeline{
	agent any
	tools {
		maven 'mvn 3.5'
	}
	stages{
		stage('git clone'){
			steps{
			 checkoit scm
			}
			}
		stage('build'){
			steps{
			sh 'mvn mvnm  package'
			}
			}
		}
}
