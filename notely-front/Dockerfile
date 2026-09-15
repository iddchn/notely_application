FROM node:26.8 as build
WORKDIR /app

ENV NODE_OPTIONS="--openssl-legacy-provider"

COPY package.json .
RUN npm install

COPY src /app/src
COPY public /app/public
RUN npm run build


FROM nginx:1.27.3-alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]