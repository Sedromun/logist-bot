up:
	docker compose -f docker-compose.yml up --build -d pallets-bot
down:
	docker compose -f docker-compose.yml down
restart:
	docker compose -f docker-compose.yml restart
bot:
	docker exec -it pallets-bot bash
db:
	docker exec -it pallets-database bash
