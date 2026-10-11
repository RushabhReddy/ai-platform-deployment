run-docker-compose:
	uv sync
	docker compose up --build

clean-noterbook-outputs:
	jupyter nbconvert --clear-output --inplace notebooks/*/*.ipynb
