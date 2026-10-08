# Change this to match your project id
GCP_PROJECT_ID=<your_gcp_project_id>
# Change this for your relevant region - e.g. europe-west1
GCP_REGION=<your_gcp_region>

# Optionally change these values
DOCKER_IMAGE=counter-app
DOCKER_REPO=counter-repo
DOCKER_REPO_DESCRIPTION=lecture repo
VERSION=0.3

ARTIFACT_IMAGE=${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${DOCKER_REPO}/${DOCKER_IMAGE}:${VERSION}

### Local ###

build:
	docker build -t ${DOCKER_IMAGE} .

explore:
	docker run -it ${DOCKER_IMAGE} sh

run:
	docker run -p 8080:8080 ${DOCKER_IMAGE}

create_artifact_repo:
	gcloud artifacts repositories create ${DOCKER_REPO} \
		--repository-format=docker \
		--location=${GCP_REGION} \
		--description="${DOCKER_REPO_DESCRIPTION}"

print_artifact_uri:
	@echo "${ARTIFACT_IMAGE}"

### Cloud ###

build_artifact:
	docker build -t ${ARTIFACT_IMAGE} .

run_artifact:
	docker run -p 8080:8080 ${ARTIFACT_IMAGE}

push_artifact:
	docker push ${ARTIFACT_IMAGE}
