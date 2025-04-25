import click
import logging
from urllib.parse import urlparse
from .dns_checker import check_dns
from .ssl_checker import check_ssl
from .http_checker import make_request_with_different_configs

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_domain(value):
    parsed = urlparse(value)
    return parsed.netloc or parsed.path  # Handles both full URLs and plain domains

@click.group()
def cli():
    """API Diagnostic CLI Tool"""
    pass

@cli.command(name="check-dns")
@click.argument('target')
def check_dns_cli(target):
    """Check DNS resolution"""
    domain = extract_domain(target)
    click.echo(check_dns(domain))

@cli.command(name="check-ssl")
@click.argument('target')
def check_ssl_cli(target):
    """Check SSL/TLS handshake"""
    domain = extract_domain(target)
    click.echo(check_ssl(domain))

@cli.command(name="check-http")
@click.argument('url')
def check_http_cli(url):
    """Make HTTP requests with different configurations"""
    results = make_request_with_different_configs(url)
    for config, result in results.items():
        click.echo(f"{config}: {result}")

@cli.command(name="run-all")
@click.argument('url')
def run_all(url):
    """Run DNS, SSL, and HTTP checks"""
    domain = extract_domain(url)
    click.echo("DNS Check:")
    click.echo(check_dns(domain))
    click.echo("\nSSL Check:")
    click.echo(check_ssl(domain))
    click.echo("\nHTTP Checks:")
    results = make_request_with_different_configs(url)
    for config, result in results.items():
        click.echo(f"{config}: {result}")

if __name__ == '__main__':
    cli()
