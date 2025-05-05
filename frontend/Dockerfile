# Stage 1: Build the application
FROM node:lts-alpine AS builder
WORKDIR /app

# Enable pnpm (no need for global install)
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy package files first for better caching
COPY package.json pnpm-lock.yaml .npmrc ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the files
COPY . .

# Build the app (adjust if using a different adapter)
RUN pnpm run build

# --- Production Stage ---
FROM node:lts-alpine AS production
WORKDIR /app

# Enable pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy only necessary files from builder
COPY --from=builder /app/package.json /app/pnpm-lock.yaml ./
COPY --from=builder /app/node_modules ./node_modules

# IMPORTANT: Copy the correct build output based on your adapter
# For Node adapter (default output location):
COPY --from=builder /app/build ./build

# For static adapter (if using):
# COPY --from=builder /app/build ./build

# For other adapters (check your svelte.config.js):
# COPY --from=builder /app/.svelte-kit ./build

EXPOSE 3000
ENV NODE_ENV=production

# Command depends on your adapter:
# For Node adapter:
CMD ["node", "build/index.js"]

# For static sites (serve with a web server):
# RUN npm install -g serve
# CMD ["serve", "-s", "build"]