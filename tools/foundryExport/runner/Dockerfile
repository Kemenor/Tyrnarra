# The Foundry runner: Debian's Chromium driven by playwright-core (no bundled browser download).
FROM node:24-bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends chromium fonts-dejavu-core ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev --no-audit --no-fund
COPY runner.mjs run.mjs ./
USER 1000:1000
CMD ["node", "/app/runner.mjs"]
