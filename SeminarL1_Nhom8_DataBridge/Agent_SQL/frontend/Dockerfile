# ==========================================
# STAGE 1: Deps (Install dependencies)
# ==========================================
FROM node:20-alpine AS deps
# Check https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine to understand why libc6-compat might be needed.
RUN --mount=type=cache,target=/var/cache/apk \
    apk add libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci


# ==========================================
# STAGE 2: Builder (Build the application)
# ==========================================
FROM node:20-alpine AS builder
WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
# Copy source code
COPY . .

# Build Next.js app
# NODE_ENV=production is important for build optimizations
ENV NODE_ENV=production
RUN npm run build


# ==========================================
# STAGE 3: Runner (Production image)
# ==========================================
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create a non-root user for security
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

# Copy only necessary files for production execution
# Next.js standalone output is preferred for smallest image size,
# but following the user's specific "Copy only: .next, public, package.json" requirement.
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Set permissions to non-root user
RUN chown -R nextjs:nodejs /app

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Set environment variable for the port
ENV PORT=3000
# Important for Next.js in Docker
ENV HOSTNAME="0.0.0.0"

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000 || exit 1

# Launch the application
CMD ["npm", "run", "start"]

# ==========================================
# STAGE 4: Development
# ==========================================
FROM deps AS dev
WORKDIR /app
ENV NODE_ENV=development
CMD ["npm", "run", "dev"]
