RUN apt-get update

# ADD YOUR DOCKERFILE CONFIGS

ENTRYPOINT [ "python", "-m", "leotest", "--test-config", "/artifacts/experiment-config.yaml" ]







