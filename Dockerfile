FROM jinaai/jina:3.19.0-py310-standard

RUN apt-get update && apt-get install --no-install-recommends -y git pip nginx && rm -rf /var/lib/apt/lists/*

# setup the workspace
COPY . /workdir/
WORKDIR /workdir

RUN pip install -e . && pip install --compile -r requirements.txt

ENTRYPOINT ["jina", "-v"]