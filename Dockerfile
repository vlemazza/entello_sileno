ARG PYTHON_VERSION=3.14.3
ARG DEBIAN_CODENAME=trixie
FROM python:${PYTHON_VERSION}-${DEBIAN_CODENAME}

ARG DEBIAN_CODENAME

RUN printf "deb http://deb.debian.org/debian %s main contrib non-free non-free-firmware\n" "${DEBIAN_CODENAME}" > /etc/apt/sources.list \
    && apt-get update \
    && apt-get install --no-install-recommends -y ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && adduser entello

COPY --chown=entello:entello src /bot
COPY waiting_messages.json /bot/

WORKDIR /bot

USER entello
WORKDIR /bot

ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
