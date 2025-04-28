# DataBloom SDK Client

A Python SDK client for data integration with PostgreSQL, MySQL, Nessie, and S3.

## Quick Start

```bash
# Setup environment
conda create -n data_bloom python=3.11
conda activate data_bloom

# Install
pip install -e ".[dev]"
```

## Configuration

Create `.env` file with your credentials:

## Testing

```bash
# Run all tests
make test
```

## Development

```bash
make format          # Format code
make lint           # Run linter
make doc            # Build docs
```

## License

VNG License


```sh
curl -v lighter.namvq.svc.cluster.local:8080 
ping lighter.namvq.svc.cluster.local
nslookup lighter.namvq.svc.cluster.local 8080
curl -v http://lighter.namvq.svc.cluster.local:8080/health
curl http://lighter.namvq.svc.cluster.local:8080/lighter/api/sessions
curl http://lighter.namvq.svc.cluster.local:8080/lighter/sessions
```