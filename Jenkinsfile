pipeline {
	agent  { label 'main' }
	stages {
		stage('Run ASV') {
			steps {
				sh './benchmarks/asv_run_script.sh'
			}
		}
	}
}
