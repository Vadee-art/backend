# Vadee backend using Django with Postgres, Gunicorn, and Nginx

### Development

Get the `dapp` submodule:

```sh
git submodule init
```

Uses the default Django development server.

1. Rename `.env.dev-sample` to `.env`.
2. Update the environment variables in the and _.env.dev_ files.
3. Build the images and run the containers:

   ```sh
   docker-compose up -d --build
   ```

   Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

**Note**: You need up and running containers to run next commands otherwise you will get `ERROR: No container found for web_1`!

4. You need to make migrations?

   ```sh
   ./scripts/makemigrations.sh
   ```

5. You need to apply migrations?

   ```sh
   ./scripts/migrate.sh
   ```

6. You need a shell inside container?

   ```sh
   ./scripts/shell.sh
   ```

7. You wand direct db shell?

   ```sh
   ./scripts/psql.sh
   ```

8. Anything else?

   ```sh
   docker-compose exec <SERVICE> <COMMAND>
   ```

### Production

Uses gunicorn + nginx.

Follow https://dockerswarm.rocks/ till the end of Portainer section.

1. Rename _.env.prod-sample_ to _.env_. Update the environment variables.
2. Build the images and run the containers:

   ```sh
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

Test it out at [http://localhost:1818](http://localhost:1818). No mounted folders. To apply changes, the image must be re-built.

---

Docker files inspired from https://github.com/testdrivenio/django-on-docker/
