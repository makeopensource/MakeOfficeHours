# MakeOfficeHours

## Getting Started 

See the relevant documentation for each component for development.

We have two Docker configurations that simulate a production sort of environment. The production setup will expect TLS certificates in the nginx directory. There's a shell script named `generate_testing_keys.sh` that can generate self-signed certificates. 

The production setup will run the application on port 443.

To run the project in production:
```bash
docker compose up --build
```

The testing setup will run the application on port 3000.

To run the project in testing:
```bash
docker compose -f compose-testing.yaml up --build
```

These will use the respective environment files (`.env-api-prod` and `.env-testing`) for Autolab credentials and for creating the initial administrator account. Currently in production mode, accessing any user account (including the administrator account) require authentication via Autolab. Thus, you should probably only develop using either the testing configuration or by running everything locally. Testing exposes some additional endpoints (which are accessible from the frontend at `/dev-login`) with simple password authentication. This is not safe to use in production; anyone can claim any unclaimed user in the roster without proof.

The `THE_OG_UBIT` and `THE_OG_PN` fields will add this account to the roster but will not create an account. You can create an account by logging into an Autolab account with a matching UBIT, or in testing hit the `/signup` endpoint (accessible from the frontend's `/dev-login` page).

Autolab integration is currently only used for authentication purposes. Since there isn't much need for further development on this front and since we have alternate authentication for testing purposes, testing API keys will generally not be distributed. Don't let this discourage you if you have ideas for further Autolab integration though, please talk to us on our Discord if you're interested!

## Project Structure

### `/api`
A Flask API server and some utilities to run it locally and such. 

### `/client`
A Vue frontend for the site. 

### `/hardware`
Currently, a Python script for reading a specific card format to identify users and an example of a card payload. We may separate the card swipe hardware from the web application in the future. In that case, the relevant project will live here.

### `/nginx`
Some utilities for nginx, mainly the aforementioned shell script to generate testing keys for the Docker setup.

### `/tests`
Tests for the API server, which are not up to date.

## License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

