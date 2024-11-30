FROM node:lts
RUN apt-get update --yes
COPY . /postgres
WORKDIR /postgres
RUN npm install
EXPOSE 3000
CMD ["node", "client.js"]
