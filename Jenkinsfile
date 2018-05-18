pipeline{
	agent {label 'wrkr'}
	tools {
		maven 'mvn 3.5'
	}
	parameters {
    	string(name: 'quantity', defaultValue: '1', description: 'Quantity of app instances')
		string(name: 'filter', defaultValue: 'vadim*', description: 'Filter keyword for security groups')
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
		stage('up instances') {
    		steps {
        		withCredentials([[
            	$class: 'AmazonWebServicesCredentialsBinding',
            	credentialsId: 'aws_credent',
            	accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        		]]) {
            	sh "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/app_instances.py ${params.quantity} ${params.filter}"
        		}
    		}
    	}
		stage('provision'){
       		steps{
				parallel(
				db_provision : {
					withCredentials([sshUserPrivateKey(credentialsId: "ssh_key", keyFileVariable: 'keyfile'), file(credentialsId: 'vars', variable: 'vars')]){		 
					sh 'ansible-playbook ./scripts/playbookDB.yml -e "@${vars}" -i ./hosts --private-key=${keyfile} --ssh-common-args="-o StrictHostKeyChecking=no"'
					}
				},
				app_provision : {
					withCredentials([sshUserPrivateKey(credentialsId: "ssh_key", keyFileVariable: 'keyfile'), file(credentialsId: 'vars', variable: 'vars')]){	
					sh 'ansible-playbook ./scripts/playbookAPPv2.yml -e "@${vars}" -i ./hosts --private-key=${keyfile} --ssh-common-args="-o StrictHostKeyChecking=no"'
					}	
				}
				)
        	}
		}
		stage('health check'){
			steps{
				withCredentials([[
            	$class: 'AmazonWebServicesCredentialsBinding',
            	credentialsId: 'aws_credent',
            	accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        		]]) {
				sh "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/check.py"
				}
			}
		}
	}
	post { 
    	failure { 
            withCredentials([[
            	$class: 'AmazonWebServicesCredentialsBinding',
            	credentialsId: 'aws_credent',
            	accessKeyVariable: 'AWS_ACCESS_KEY_ID',
            	secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        		]]) {
            	sh "AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} AWS_DEFAULT_REGION=eu-central-1 python3 ./scripts/terminate_instances.py"
        		}
		}
	}
}
