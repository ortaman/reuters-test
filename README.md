
## Requirements

- [Docker](https://www.docker.com/community-edition)
- [Docker Compose](https://docs.docker.com/compose/install/)


### Set up and run the project:
- Clone the repository to your local machine:
```bash
git clone https://github.com/ortaman/reuters-test.git
```

- Open a terminal and run in the app directory:
```bash
docker-compose up
```
- Open another terminal and run to test:
```bash
curl "http://127.0.0.1:8000/casetext_sync/?start_date=2023-05-15&end_date=2023-05-16"
```

### Tests
-  In the app directory run:
```bash
python -m pytest

```
