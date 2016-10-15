FROM ruby:2.3
RUN apt-get update -qq && apt-get install -y build-essential libpq-dev nodejs

ENV app /skillsort/skillsort
RUN mkdir -p $app
WORKDIR $app

ENV BUNDLE_PATH /box
ADD . $app

EXPOSE 5555

