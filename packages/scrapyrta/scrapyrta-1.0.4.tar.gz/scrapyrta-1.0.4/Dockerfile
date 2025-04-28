#######################################################
#   ScrapyrtA - Asynchronous Scrapy Runtime Service
#######################################################
#
# Build the image:
#   docker build -t scrapyrta .
#
# Run as a daemon:
#   docker run -d --name scrapyrta \
#     -p 9080:9080 \
#     -v /path/to/your/project:/scrapyrta/project \  # (optional)
#     scrapyrta
#
# Access the service at http://localhost:9080
#

FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN mkdir -p /scrapyrta/src /scrapyrta/project

COPY . /scrapyrta/src/
RUN pip install --no-cache-dir /scrapyrta/src

WORKDIR /scrapyrta/project

# Run as non-root user for better security
RUN groupadd -r scrapyrta &&
    useradd -r -g scrapyrta scrapyrta &&
    chown -R scrapyrta:scrapyrta /scrapyrta /var/log/scrapyrta
USER scrapyrta

EXPOSE 9080

ENTRYPOINT ["scrapyrta", "-i", "0.0.0.0"]
