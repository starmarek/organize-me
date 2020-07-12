FROM node:lts-buster-slim

WORKDIR /usr/src/app

COPY vue.config.js .
COPY package.json .
COPY yarn.lock .

RUN yarn install
