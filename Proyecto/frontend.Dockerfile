FROM node:22-alpine3.19

WORKDIR /app

COPY frondmuestraproyecto/ .
RUN npm install
RUN npm install axios

EXPOSE 3000

CMD ["npm", "start"]

