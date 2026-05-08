# ProductService

ProductService is a Spring Boot REST API microservice for managing products in an e-commerce website.

## Features

- Add, retrieve, update, and delete product records
- RESTful interface with JSON payloads
- Built using Spring Boot, JPA (Hibernate), MySQL, and Flyway for database migrations
- Redis integration for caching
- Includes testing setup with JUnit

## Stack

- Java 21
- Spring Boot 3.3.x
- Maven
- MySQL
- JPA (Hibernate)
- Redis
- Flyway
- Lombok

## Getting Started

### Prerequisites

- Java 21
- Maven
- MySQL database running and accessible
- Redis server (for caching, optional but recommended)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hkForData/ProductService.git
   cd ProductService
   ```

2. **Configure the Database:**

   Update your `src/main/resources/application.properties` with MySQL and Redis configuration details.

3. **Run Flyway migrations (optional):**
   Flyway will migrate your database schema automatically on startup if enabled.

4. **Build the app:**
   ```bash
   mvn clean install
   ```

5. **Run the app:**
   ```bash
   mvn spring-boot:run
   ```

   The app runs at: [http://localhost:8080](http://localhost:8080)

## REST API Endpoints

| Method | Endpoint           | Description                       |
|--------|--------------------|-----------------------------------|
| POST   | `/products`        | Create a new product              |
| GET    | `/products`        | List all products                 |
| GET    | `/products/{id}`   | Get details of a single product   |
| PATCH  | `/products/{id}`   | Partially update a product        |
| DELETE | `/products/{id}`   | Delete a product                  |
| PUT    | `/products/{id}`   | Replace a product                 |

**Sample cURL:**
```bash
# Create Product
curl -X POST -H "Content-Type: application/json" \
  -d '{"title":"Chair","description":"A comfy chair"}' \
  http://localhost:8080/products

# Get All Products
curl http://localhost:8080/products

# Update Product
curl -X PATCH -H "Content-Type: application/json" \
  -d '{"title":"Updated Chair"}' \
  http://localhost:8080/products/1
```

## Testing

Run the test suite with:

```bash
mvn test
```

## Project Structure

- `src/main/java/com/scaler/productservice2402/` - application source code
- `controllers/` - REST API endpoints
- `models/` - JPA entities
- `services/` - business logic
- `repositories/` - data access layer

## Contributing

1. Create an issue or fork the repository
2. Work your feature/fix in a branch
3. Open a pull request

## License

[Specify license here, e.g. MIT, Apache 2.0, etc.]

## Maintainer

hkForData
