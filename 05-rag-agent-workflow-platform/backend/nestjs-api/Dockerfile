FROM node:22-alpine AS build
WORKDIR /workspace
COPY package.json package-lock.json ./
COPY backend/nestjs-api/package.json backend/nestjs-api/package.json
COPY frontend/sveltekit-app/package.json frontend/sveltekit-app/package.json
RUN npm ci --workspace @rag-platform/api --include-workspace-root
COPY backend/nestjs-api backend/nestjs-api
RUN npm run build --workspace @rag-platform/api

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /workspace/node_modules ./node_modules
COPY --from=build /workspace/backend/nestjs-api/dist ./dist
COPY --from=build /workspace/backend/nestjs-api/package.json ./package.json
RUN addgroup -S app && adduser -S app -G app
USER app
EXPOSE 3000
CMD ["node", "dist/main.js"]
