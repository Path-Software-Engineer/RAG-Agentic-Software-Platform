FROM node:22-alpine AS build
WORKDIR /workspace
ARG PUBLIC_API_BASE_URL=http://localhost:5300
ENV PUBLIC_API_BASE_URL=$PUBLIC_API_BASE_URL
COPY package.json package-lock.json ./
COPY backend/nestjs-api/package.json backend/nestjs-api/package.json
COPY frontend/sveltekit-app/package.json frontend/sveltekit-app/package.json
RUN npm ci --workspace @rag-platform/web --include-workspace-root
COPY frontend/sveltekit-app frontend/sveltekit-app
RUN npm run build --workspace @rag-platform/web

FROM nginx:1.29-alpine
COPY frontend/sveltekit-app/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /workspace/frontend/sveltekit-app/build /usr/share/nginx/html
EXPOSE 8080
