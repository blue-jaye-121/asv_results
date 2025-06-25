pipeline {
	agent { dockerfile true } //Will build container based on Dockerfile at root of dir
	stages {
		stage('Run ASV') {
			sh './benchmarks/asv_run_script.sh'
		}
	}
}