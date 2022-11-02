package:
	docker build -t fusion-api-environment -f image/Dockerfile .

run:
	docker run -it -v `pwd`:/fusion-client-setup fusion-api-environment /bin/bash
clean:
	docker rmi -f fusion-api-environment
