#!/bin/bash
copilot app init --domain lmonn.com arkham-us-west2-test
copilot init --app arkham-us-west2-test                   \
  --name api                                 \
  --type 'Load Balanced Web Service'         \
  --dockerfile './services/blocks/Dockerfile'\
  --port 80                             \
  --deploy